import re
from datetime import datetime

from pydantic import BaseModel, field_validator, conint, RootModel, Field
try:
    from dgredis import RedisConfig
except ImportError:
    RedisConfig = None

class TriggerConfig(BaseModel):
    trigger_count: conint(ge=0)  # целое число >= 0
    trigger_time: str  # строка с временным интервалом

    @classmethod
    @field_validator('trigger_time')
    def validate_trigger_time(cls, v: str) -> str:
        if not re.fullmatch(r'^\d+[mhd]$', v):
            raise ValueError('trigger_time must be in format <number>m, <number>h or <number>d')
        return v

class MetricConfig(BaseModel):
    name: str
    documentation: str
    labels: dict[str, TriggerConfig] | None = None  # опциональный словарь с произвольными ключами
    last_update: datetime | None = None


MetricListConfig = RootModel[list[MetricConfig]]

class MetricsHTTPWatcherConfig(BaseModel):
    url: str = Field(description="URL для получения метрик")
    username: str = Field(description="Имя пользователя")
    password: str = Field(description="Пароль")
    interval_seconds: int = Field(description="Интервал опроса в секундах")

class MetricsRedisWatcherConfig(BaseModel):
    service_name: str = Field(description="Имя сервиса") # С помощью этого имени будет производиться поиск ключа в redis (<service-name.metrics>)
    redis_config: RedisConfig = Field(description="Конфигурация подключения к Redis")
    interval_seconds: int = Field(description="Интервал опроса в секундах")
    force_update: bool = Field(description="Принудительное обновление метрик")


