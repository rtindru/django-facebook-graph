from django.shortcuts import HttpResponseRedirect, HttpResponse, Http404
from allauth.socialaccount.models import SocialAccount, SocialToken

from models import *
from signals import *
from relations import *


def add_product(request):
    if request.method == 'GET':
        import pdb; pdb.set_trace()
        product = Product.objects.all()[0]
        txn = Transaction.objects.create(user=request.user, product=product)
        graph_user = FacebookGraphUser.get(user_model.objects.all()[0])
        graph_user.get_friends()
        relation = get_base_relation(Transaction.__name__)
        print graph_user.get_friends_with_relation(product, relation)
        import pdb; pdb.set_trace()
        new_relation_event.send(sender=None, user=request.user,
                                model_instance=product, relation_instance=get_incremental_relation(Transaction.__name__))

        return