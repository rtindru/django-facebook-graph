__author__ = 'indrajit'

import importlib

from facebook_graph import SocialGraph, get_user_model

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

user_model = get_user_model()

class BaseMapper(object):
    """
    Maps a Django Model object to a Graph Node
    """
    _graph = None

    class Meta:
        key_field = 'pk'
        data_fields = []

    def __init__(self, vertex, instance):
        self._vertex = vertex
        self.instance = instance
        for key, value in vertex.data().items():
            setattr(self, key, value)

    @classmethod
    def create(cls, instance):
        if not cls._graph:
            cls._graph = SocialGraph().g
        assert cls.Meta.key_field not in cls.Meta.data_fields
        insert_dict = {key: getattr(instance, key) for key in cls.Meta.data_fields}
        insert_dict.update({cls.Meta.key_field: getattr(instance, cls.Meta.key_field)})
        vertex = cls._graph.vertices.create(
            label=instance.__class__.__name__,
            **insert_dict
        )

        node = cls(vertex, instance)
        return node

    @classmethod
    def get(cls, instance):
        if not cls._graph:
            cls._graph = SocialGraph().g
        query_dict = {cls.Meta.key_field: getattr(instance, cls.Meta.key_field)}
        vertices = cls._graph.vertices.index.lookup(label=instance.__class__.__name__, **query_dict)
        if vertices:
            return cls(vertices.next(), instance)
        return None

    @classmethod
    def get_or_create(cls, instance):
        node = cls.get(instance)
        if not node:
            node = cls.create(instance)
        return node

    @classmethod
    def filter(cls, **kwargs):
        vertices = cls._graph.vertices.index.lookup(**kwargs)
        if vertices:
            for vertex in vertices:
                yield cls(vertex, None)


class FacebookGraphUser(BaseMapper):
    _graph = SocialGraph().g

    def __unicode__(self):
        return '{} - {}'.format(self.instance, self._vertex)

    class Meta:
        key_field = 'uid'
        data_fields = ['pk']

    def is_friend(self, user):
        return self.has_relation(user, 'friends')

    def has_relation(self, node, relation):
        edges = self._vertex.bothE(relation)
        if edges:
            for edge in edges:
                if node._vertex == edge.inV():
                    return edge
        return None

    def relate(self, node, relation, bi_directed=False, **attrs):
        if not FacebookGraphUser._graph:
            FacebookGraphUser._graph = SocialGraph().g
        edge = self.has_relation(node, relation)
        if edge is None:
            edge = FacebookGraphUser._graph.edges.create(self._vertex, relation, node._vertex)
        if bi_directed:
            edge_2 = node.has_relation(self, relation)
            if edge_2 is None:
                edge_2 = FacebookGraphUser._graph.edges.create(node._vertex, relation, self._vertex)
        for key, value in attrs.items():
            setattr(edge, key, value)
            if bi_directed:
                setattr(edge_2, key, value)
        return edge

    def friends(self):
        vertices = self._vertex.outV('friends')
        friends = []
        if vertices:
            for vertex in vertices:
                query_dict = {self.Meta.key_field: vertex.data()[self.Meta.key_field]}
                friends.append(FacebookGraphUser(vertex, user_model.objects.get(**query_dict)))
        return friends

    def friends_of_friends(self):
        level_1 = []
        level_2 = []
        vertices = self._vertex.outV('friends')
        if vertices:
            for vertex in vertices:
                query_dict = {self.Meta.key_field: vertex.data()[self.Meta.key_field]}
                level_1.append(FacebookGraphUser(vertex, user_model.objects.get(**query_dict)))
                layer_2 = vertex.outV('friends')
                if layer_2:
                    for vertex_2 in layer_2:
                        if vertex_2 != self._vertex:
                            query_dict = {self.Meta.key_field: vertex_2.data()[self.Meta.key_field]}
                            level_2.append(FacebookGraphUser(vertex_2, user_model.objects.get(**query_dict)))
        return {1: level_1, 2: level_2}

    def get_friends_with_relation(self, instance, relation):
        friends = []
        relation_node = BaseMapper.get(instance)
        if not relation_node:
            return friends
        vertices = self._vertex.outV('friends')
        if vertices:
            for vertex in vertices:
                if vertex.outV(relation):
                    query_dict = {self.Meta.key_field: vertex.data()[self.Meta.key_field]}
                    friends.append(FacebookGraphUser(vertex, user_model.objects.get(**query_dict)))
        return friends

    def fof_with_relation(self, instance, relation):
        level_1 = self.get_friends_with_relation(instance, relation)
        level_2 = []
        for friend in level_1:
            level_2.extend(friend.get_friends_with_relation(instance, relation))
        while self in level_2:
            level_2.remove(self)
        return {1: level_1, 2: level_2}

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{} - {}'.format(self.product.name, self.user)
