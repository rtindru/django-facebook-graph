# __author__ = 'indrajit'
#
# from facebook_graph import SocialGraph
#
# class GenericRelation(object):
#     _graph = None
#
#     @classmethod
#     def relate(cls, nodeA, nodeB, bi_directed=False, **attrs):
#         if not cls._graph:
#             cls._graph = SocialGraph().g
#         edge = cls.has_relation(nodeA, nodeB)
#         if not edge:
#             edge = cls._graph.edges.create(nodeA._vertex, cls.__name__.lower(), nodeB._vertex)
#         for key, value in attrs.items():
#             setattr(edge, key, value)
#         return edge
#
#     @classmethod
#     def has_relation(cls, nodeA, nodeB):
#         edges = nodeA._vertex.outE(cls.__name__.lower())
#         if edges:
#             for edge in edges:
#                 if nodeB._vertex == edge.inV():
#                     return edge
#         return False
#
#
# class Friends(GenericRelation):
#     pass
#
#
# # class IncrementalRelation(GenericRelation):
# #
# #     @classmethod
# #     def relate(cls, nodeA, nodeB, bi_directed=False, **attrs):
# #         edge = cls.has_relation(nodeA, nodeB)
# #         if not edge:
# #             edge = super(IncrementalRelation, cls).relate(nodeA, nodeB)
# #         count = getattr(edge, 'count', 0)
# #         setattr(edge, 'count', count+1)
# #         return edge
#
#
# # def get_base_relation(class_name, attrs={}):
# #     return type(class_name, (GenericRelation, ), attrs)
# #
# #
# # def get_incremental_relation(class_name, attrs={}):
# #     return type(class_name, (IncrementalRelation, ), attrs)
#
