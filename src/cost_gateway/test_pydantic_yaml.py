from tempfile import TemporaryDirectory
from unittest import TestCase

from cost_gateway.pydantic_yaml import from_yaml, to_yaml
from cost_gateway.settings import (
    ApiSettings,
    PrometheusSettings,
    Settings,
)


class PyDanticYamlTest(TestCase):
    def test_dump_load_settings(self):
        expected = Settings(
            api=ApiSettings(port=8000),
            prometheus=PrometheusSettings(endpoint_port=8080),
        )
        with TemporaryDirectory("-pydantic", "test") as tmpdir:
            yaml_file = f"{tmpdir}/test.yaml"
            to_yaml(yaml_file, expected)
            actual = from_yaml(yaml_file, Settings)

        self.assertEqual(expected, actual)
