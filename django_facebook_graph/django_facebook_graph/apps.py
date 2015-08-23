__author__ = 'indrajit'

from django.apps import AppConfig

class DjangoFBGraphConfig(AppConfig):
    name = 'django_facebook_graph'
    verbose_name = "Django Facebook Graph"

    def ready(self):
        import signals