import logging
import warnings
from typing import Any, TYPE_CHECKING

from prometheus_client import Counter, generate_latest, REGISTRY

from .config import (
    MetricListConfig,
    MetricsHTTPWatcherConfig,
    MetricsRedisWatcherConfig,
)
from .logger import setup_logger

if TYPE_CHECKING:
    from dgmetrics.watchers.redis import RedisWatcher


class Metrics:
    def __init__(self, metrics_config: MetricListConfig | None = None, watcher_config: MetricsHTTPWatcherConfig | MetricsRedisWatcherConfig | None = None):
        self.metrics: dict[str, Counter | dict[str, Counter]] | None = None
        self.metrics_config = metrics_config
        self.labels: dict[str, dict[str, Any]] | None = None
        self.watcher_config = watcher_config
        self.log = setup_logger(name=self.__class__.__name__, level=logging.INFO)


        if metrics_config is not None or watcher_config is not None:
            warnings.warn(
                "Прямое использование __init__() устарело. "
                "Используйте Metrics.from_config() или Metrics.from_watcher(). "
                "Этот способ будет удален в будущих версиях.",
                DeprecationWarning,
                stacklevel=2
            )

        if metrics_config:
            self.init_metrics(self.metrics_config)

    @classmethod
    def from_config(cls, metrics_config: MetricListConfig) -> 'Metrics':
        """
        Инициализация метрик из конфига
        """
        instance = cls()
        instance.metrics_config = metrics_config
        instance.init_metrics(metrics_config)
        return instance

    @classmethod
    def from_watcher(cls, watcher_config: MetricsHTTPWatcherConfig | MetricsRedisWatcherConfig) -> 'Metrics':
        """
        Инициализирует метрики из указанного способа слежения и продолжает следить за изменениями
        """
        instance = cls()
        instance.watcher_config = watcher_config
        instance._init_watcher()
        return instance

    @staticmethod
    def _get_label_names(**labels):
        return ('type', 'process') + tuple(list(labels.keys()))

    @staticmethod
    def _get_label_type_process(process):
        type_, process_ = process.split('.')
        return {'type': type_, 'process': process_}

    def _get_labels(self, name, process):
        try:
            labels = self.labels.get(name).get(process)
            if labels is None:
                return None
            result = dict(labels)
            result.update(self._get_label_type_process(process))
            return result
        except AttributeError:
            return None

    def add_metric(self, name, documentation: str | None = None, labels: dict[str, dict[str, Any]] | None = None):
        """
        Add metric to processing
        :param name: Metrics name
        :param documentation: Description of metric
        :param labels: Additional arguments. E.g. {'service.run': {'trigger_count': 0, 'trigger_time': '0m'}}
        :return: None
        """
        documentation = documentation or ""
        if not self.metrics:
            self.metrics = {}
        if not self.labels:
            self.labels = {}

        if labels:
            labelnames = self._get_label_names(**(list(labels.values())[0]))

            counter = Counter(name, documentation, labelnames=labelnames)
            self.metrics.update({name: counter})
            self.labels.update({name: labels})

            for process in labels.keys():
                self.increment_metric(name, 0.0, process=process)  # init metrics with 0 value
        else:
            self.metrics[name] = Counter(name, documentation, labelnames=())
            self.increment_metric(name, 0.0)  # init metric with 0 value

    def get_metric(self, name) -> Counter | None:
        """
        Get metric by name
        :param name: Metric name
        :return: Counter | None
        """
        try:
            return self.metrics.get(name)
        except AttributeError:
            return None

    def increment_metric(self, name, value: float | None = None, process: str | None=None):
        """
        Increment metric by name for value
        :param name: Metric name
        :param value: Increment value. 1.0 by default if None
        :param process: Process name if you use labels
        :return: None
        """
        value = value if value is not None else 1.0
        metric = self.get_metric(name)
        assert metric, f"Metric {name} not set. Add it by calling {self.__class__.__name__}.add_metric('{name}', 'Description')"

        labels_ = self._get_labels(name, process)
        assert labels_ and process or not labels_, "Add process name for increment for this metric"
        label = metric.labels(**labels_) if labels_ else None
        label.inc(value) if label else metric.inc(value)

    @staticmethod
    def collect_metrics():
        return generate_latest().decode()

    def init_metrics(self, metrics_conf: MetricListConfig):
        for metric in metrics_conf.root:
            self.add_metric(**metric.model_dump(exclude={"last_update"}))

    def _update_metrics(self, new_metrics: MetricListConfig) -> None:
        """
        Обновляет метрики при получении новых данных от наблюдателя
        """

        if not self.metrics:
            self.init_metrics(new_metrics)
            return

        existing_metrics = set(self.metrics.keys())
        new_metrics_names = {m.name for m in new_metrics.root}

        for metric_name in existing_metrics - new_metrics_names:
            try:
                REGISTRY.unregister(self.metrics[metric_name])
                del self.metrics[metric_name]
                if self.labels and metric_name in self.labels:
                    del self.labels[metric_name]
            except Exception as e:
                self.log.warning(f"Ошибка при удалении метрики '{metric_name}': {e}")

        for metric in new_metrics.root:
            metric_name = metric.name
            new_labels = metric.labels if metric.labels else {}
            current_labels = self.labels.get(metric_name, {}) if self.labels else {}

            if metric_name not in self.metrics:
                self.add_metric(**metric.model_dump(exclude={"last_update"}))
            else:
                if current_labels == new_labels:
                    self.log.debug(f"Метрика '{metric_name}' не изменилась")
                    continue

                current_processes = set(current_labels.keys())
                new_processes = set(new_labels.keys())
                common_processes = current_processes & new_processes
                saved_values = self._save_metric_values(metric_name, common_processes)

                try:
                    REGISTRY.unregister(self.metrics[metric_name])
                except Exception as e:
                    self.log.warning(f"Ошибка при удалении метрики '{metric_name}': {e}")

                del self.metrics[metric_name]
                if self.labels and metric_name in self.labels:
                    del self.labels[metric_name]

                self.add_metric(**metric.model_dump(exclude={"last_update"}))
                self._restore_metric_values(metric_name, saved_values)

    def _save_metric_values(self, metric_name: str, labels_to_save: set[str]) -> dict:
        """Сохраняет текущие значения метрики для указанных лейблов."""
        saved = {}
        metric = self.metrics.get(metric_name)
        if not metric or not labels_to_save:
            return saved

        for process in labels_to_save:
            try:
                labels = self._get_labels(metric_name, process)
                if labels:
                    counter = metric.labels(**labels)
                    saved[process] = counter._value.get()
            except Exception as e:
                self.log.warning(f"Не удалось сохранить значение для {metric_name}[{process}]: {e}")

        self.log.debug(f"Сохранены значения для метрики '{metric_name}': {saved}")
        return saved

    def _restore_metric_values(self, metric_name: str, saved_values: dict) -> None:
        """Восстанавливает сохранённые значения метрики."""
        metric = self.metrics.get(metric_name)
        if not metric or not saved_values:
            return

        for process, value in saved_values.items():
            if value > 0:
                try:
                    labels = self._get_labels(metric_name, process)
                    if labels:
                        metric.labels(**labels)._value.set(value)
                        self.log.debug(f"Восстановлено значение {value} для {metric_name}[{process}]")
                except Exception as e:
                    self.log.warning(f"Не удалось восстановить значение для {metric_name}[{process}]: {e}")






    def _init_watcher(self):
        """
        Инициализирует наблюдателя за изменениями метрик
        """
        if isinstance(self.watcher_config, MetricsHTTPWatcherConfig):
            # todo: когда-то это может быть будет...
            pass
        elif isinstance(self.watcher_config, MetricsRedisWatcherConfig):
            try:
                from dgmetrics.watchers.redis import RedisWatcher
            except ImportError as err:
                raise ImportError(
                    "Для использования RedisWatcher установите зависимости: "
                    "pip install dgmetrics[redis]"
                ) from err

            self.redis_watcher = RedisWatcher(self.watcher_config, on_update=self._update_metrics)
            self.redis_watcher.check_metrics()
            self.redis_watcher.start()
            self.log.debug("Запущен наблюдатель за метриками в Redis")
