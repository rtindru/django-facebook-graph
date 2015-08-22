# from django.shortcuts import HttpResponseRedirect, HttpResponse, Http404
# from allauth.socialaccount.models import SocialAccount, SocialToken
#
# from models import *
# from signals import *
#
#
# def add_product(request):
#     if request.method == 'GET':
#         product = Product.objects.all()[0]
#         txn = Transaction.objects.create(user=request.user, product=product)
#         graph_user = FacebookGraphUser.get(user_model.objects.all()[0])
#         graph_user.get_friends()
#         print graph_user.get_friends_with_relation(product, 'friends')
#         new_relation_event.send(sender=None, user=request.user,
#                                 model_instance=product, relation_instance='transaction')
#         return