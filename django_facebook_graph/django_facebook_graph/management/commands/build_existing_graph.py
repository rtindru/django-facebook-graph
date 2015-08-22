__author__ = 'indrajit'

import logging
import importlib

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_facebook_graph.facebook_graph import SocialGraph, get_user_model

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Usage: python manage.py build_existing_graph
        """
        user_model = get_user_model()

        users = user_model.objects.all()
        graph = SocialGraph()
        for user in users:
            graph.build_graph(user)