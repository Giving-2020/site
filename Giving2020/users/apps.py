from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Django AppConfig for the Users app."""

    name = 'users'

    def ready(self):
        """Run when the app has been loaded and is ready to serve requests."""
        import users.signals  # NOQA: F401
