import logging
from datetime import datetime
from typing import Callable, TYPE_CHECKING

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    HAS_APSCHEDULER = True
except ImportError:
    HAS_APSCHEDULER = False
    if not TYPE_CHECKING:
        BackgroundScheduler = None

try:
    from dgredis import RedisClient
    HAS_DGREDIS = True
except ImportError:
    HAS_DGREDIS = False
    if not TYPE_CHECKING:
        RedisClient = None

from dgmetrics.config import MetricsRedisWatcherConfig, MetricListConfig
from dgmetrics.logger import setup_logger


class RedisWatcher:
    """
    Следит за изменениями метрик в Redis
    """
    def __init__(self, config: MetricsRedisWatcherConfig, on_update: Callable[[MetricListConfig], None] | None = None):
        missing_deps = []
        if not HAS_APSCHEDULER:
            missing_deps.append("apscheduler")
        if not HAS_DGREDIS:
            missing_deps.append("dgredis")

        if missing_deps:
            raise ImportError(
                f"Для использования RedisWatcher требуются зависимости: {', '.join(missing_deps)}. "
                f"Установите их: pip install dgmetrics[redis]"
            )

        self.config = config
        self.on_update = on_update
        self.log = setup_logger(self.__class__.__name__, level=logging.DEBUG)
        self.redis = RedisClient(self.config.redis_config)
        self.scheduler = BackgroundScheduler()
        self.metrics: MetricListConfig = self._get_service_metrics()
        self.last_update: datetime | None = self._get_last_update(self.metrics)

    def start(self):
        """
        Запускает процесс слежения за изменениями метрик в redis
        """
        self.scheduler.add_job(self.check_metrics, "interval", seconds=self.config.interval_seconds)
        self.scheduler.start()

    def stop(self):
        """
        Останавливает процесс слежения за изменениями метрик в redis
        """
        self.scheduler.shutdown()


    def _get_service_metrics(self) -> MetricListConfig:
        """
        Получает метрики сервиса из redis
        """
        key = f"{self.config.service_name}.metrics" if not self.config.service_name.endswith(".metrics") else self.config.service_name
        try:
            result = self.redis.get_json_key(key)
            return MetricListConfig.model_validate(result)
        except Exception as err:
            raise err

    @staticmethod
    def _get_last_update(metrics: MetricListConfig) -> datetime | None:
        """
        Получает дату последнего обновления метрик
        """
        if metrics:
            return metrics.root[-1].last_update
        return None


    def check_metrics(self):
        """
        Проверяет наличие обновлений метрик в redis
        """
        new_metrics = self._get_service_metrics()
        new_last_update = self._get_last_update(new_metrics)
        if not self.config.force_update:
            if new_last_update and (not self.last_update or new_last_update > self.last_update):
                self.log.debug(f"Обнаружены обновленные метрики в redis для сервиса {self.config.service_name}")
                self.metrics = new_metrics
                self.last_update = new_last_update
                self.on_update(new_metrics) # Вызывает метод _update_metrics из Metrics
        else:
            self.log.debug(f"Принудительное обновление метрик из redis для сервиса {self.config.service_name}")
            self.metrics = new_metrics
            self.last_update = new_last_update
            self.on_update(new_metrics) # Вызывает метод _update_metrics из Metrics
