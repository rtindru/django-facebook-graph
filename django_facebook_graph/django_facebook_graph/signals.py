__author__ = 'indrajit'

import importlib

from django.db.models.signals import post_save
from django.dispatch import Signal
from django.conf import settings

from models import FacebookGraphUser

path = settings.FACEBOOK_USER_MODEL
module_name, class_name = path.rsplit(".", 1)
user_model = getattr(importlib.import_module(module_name), class_name)


def add_graph_user(sender, instance, **kwargs):
    FacebookGraphUser.create(instance)
post_save.connect(add_graph_user, sender=user_model, dispatch_uid="add_graph_user")

new_relation_event = Signal(providing_args=['user', 'model_instance', 'relation_instance'])


def add_new_relation(sender, **kwargs):
    """Trap the signal and do whatever is needed"""
    user = kwargs['user']
    model_instance = kwargs['model_instance']
    relation_instance = kwargs['relation_instance']
    relation_instance.relate(user, model_instance)

new_relation_event.connect(add_new_relation)