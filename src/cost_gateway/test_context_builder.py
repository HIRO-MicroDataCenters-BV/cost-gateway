from unittest import TestCase

from cost_gateway.context_builder import ContextBuilder


class ContextBuilderTest(TestCase):
    def test_success(self) -> None:
        is_success, path = ContextBuilder.parse_args(["--config", "./etc/config.yaml"])
        self.assertTrue(is_success)
        self.assertEqual(path, "./etc/config.yaml")

    def test_failure(self) -> None:
        is_success, msg = ContextBuilder.parse_args(["--config"])
        self.assertFalse(is_success)
        self.assertEqual(
            msg,
            (
                "usage: pytest [-h] --config CONFIG\n\n"
                "Cost Gateway.\n\n"
                + "options:\n"
                + "  -h, --help       show this help message and exit\n"
                + "  --config CONFIG  Cost Gateway Configuration\n"
                + "argument --config: expected one argument"
            ),
        )
