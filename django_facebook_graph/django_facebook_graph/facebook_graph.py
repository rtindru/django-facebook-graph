__author__ = 'indrajit'

import importlib

from django.conf import settings

from bulbs.neo4jserver import Graph, Config, NEO4J_URI, Edge
from facepy import GraphAPI

class SocialGraph(object):
    path = settings.FACEBOOK_USER_MODEL
    module_name, class_name = path.rsplit(".", 1)
    user_model = getattr(importlib.import_module(module_name), class_name)

    def __init__(self):
        db_url = 'http://{}:{}{}'.format(settings.NEO4J_DATABASES['default']['HOST'], settings.NEO4J_DATABASES['default']['PORT'], settings.NEO4J_DATABASES['default']['ENDPOINT'])
        print db_url
        config = Config(db_url, settings.NEO4J_DATABASES['default']['USER'], settings.NEO4J_DATABASES['default']['PASSWORD'])
        self.g = Graph(config)

    def build_graph(self, user, access_token=None):
        from models import FacebookGraphUser

        if not access_token:
            path = settings.AUTH_TOKEN_MODEL
            module_name, class_name = path.rsplit(".", 1)
            token_model = getattr(importlib.import_module(module_name), class_name)
            access_token = token_model.objects.get(account=user).token

        print access_token
        user_node = FacebookGraphUser.get_or_create(user)
        graph = GraphAPI(access_token)
        friends = graph.get('me/friends/')
        for friend in friends['data']:
            user = SocialGraph.user_model.objects.get(uid=friend['id'])
            friend_node = FacebookGraphUser.get_or_create(user)
            self.add_friend(user_node, friend_node)

    def add_friend(self, userA, userB):
        from relations import Friends
        if userA.is_friend(userB) is None:
            Friends.relate(userA, userB, bi_directed=True)