from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = "api.core"
    verbose_name = _("core")

    def ready(self) -> None:
        import api.core.signals  # noqa
