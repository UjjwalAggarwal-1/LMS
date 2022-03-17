from django.apps import AppConfig


class AllBooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'all_books'

    def ready(self):
        import all_books.signals
