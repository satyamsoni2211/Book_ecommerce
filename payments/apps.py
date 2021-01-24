from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'payments'

    def ready(self):
        # Makes sure all signal handlers are connected
        from payments import handlers  # noqa
