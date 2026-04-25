from pydantic_settings import BaseSettings


class PrometheusSettings(BaseSettings):
    endpoint_port: int = 8080


class Settings(BaseSettings):
    prometheus: PrometheusSettings
