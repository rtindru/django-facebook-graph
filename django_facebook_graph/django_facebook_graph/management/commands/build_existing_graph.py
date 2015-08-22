__author__ = 'indrajit'

import logging
import importlib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_facebook_graph.facebook_graph import SocialGraph

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Usage: python manage.py build_existing_graph
        """
        path = settings.FACEBOOK_USER_MODEL
        module_name, class_name = path.rsplit(".", 1)
        user_model = getattr(importlib.import_module(module_name), class_name)

        users = user_model.objects.all()
        graph = SocialGraph()
        for user in users:
            graph.build_graph(user)