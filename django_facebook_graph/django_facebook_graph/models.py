__author__ = 'indrajit'

from facebook_graph import SocialGraph
from relations import Friends

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

    class Meta:
        key_field = 'uid'
        data_fields = ['pk']

    def is_friend(self, user):
        return Friends.has_relation(self, user)