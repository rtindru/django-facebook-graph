__author__ = 'indrajit'

from django.db.models.signals import post_save
from django.dispatch import Signal

from models import FacebookGraphUser, BaseMapper
from facebook_graph import get_user_model, SocialGraph, get_token_model

user_model = get_user_model()
token_model = get_token_model()

def add_graph_user(sender, instance, **kwargs):
    user = user_model.objects.get(pk=instance.account_id)
    graph = SocialGraph()
    graph.build_graph(user=user)

post_save.connect(add_graph_user, sender=token_model, dispatch_uid="add_social_graph_user")

new_relation_event = Signal(providing_args=['social_user', 'model_instance', 'relation'])

def add_new_relation(sender, **kwargs):
    """Draw a new relation between a User and a Model Object"""
    social_user = kwargs['social_user']
    relation = kwargs['relation']
    model_instance = kwargs['model_instance']
    user_node = FacebookGraphUser.get_or_create(social_user)
    product_node = BaseMapper.get_or_create(model_instance)
    import pdb; pdb.set_trace()
    user_node.relate(product_node, relation)

new_relation_event.connect(add_new_relation)