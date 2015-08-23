__author__ = 'indrajit'

import importlib

from django.conf import settings

from bulbs.neo4jserver import Graph, Config, NEO4J_URI, Edge
from facepy import GraphAPI

def get_user_model():
    path = settings.FACEBOOK_USER_MODEL
    module_name, class_name = path.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)

def get_token_model():
    path = settings.AUTH_TOKEN_MODEL
    module_name, class_name = path.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)

class SocialGraph(object):
    user_model = get_user_model()

    def __init__(self):
        db_url = 'http://{}:{}{}'.format(settings.NEO4J_DATABASES['default']['HOST'], settings.NEO4J_DATABASES['default']['PORT'], settings.NEO4J_DATABASES['default']['ENDPOINT'])
        config = Config(db_url, settings.NEO4J_DATABASES['default']['USER'], settings.NEO4J_DATABASES['default']['PASSWORD'])
        self.g = Graph(config)

    def build_graph(self, user, access_token=None):
        from models import FacebookGraphUser

        if not access_token:
            token_model = get_token_model()
            access_token = token_model.objects.get(account=user).token

        user_node = FacebookGraphUser.get_or_create(user)
        graph = GraphAPI(access_token)
        friends = graph.get('me/friends/')
        for friend in friends['data']:
            try:
                user = SocialGraph.user_model.objects.get(uid=friend['id'])
            except SocialGraph.user_model.DoesNotExist as e:
                continue
            friend_node = FacebookGraphUser.get_or_create(user)
            self.add_friend(user_node, friend_node)

    def add_friend(self, userA, userB):
        userA.relate(userB, 'friends', bi_directed=True)