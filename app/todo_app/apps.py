from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TodoAppConfig(AppConfig):
    name = 'todo_app'

    def ready(self):
        import todo_app.signals  # noqa
