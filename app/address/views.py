from django.shortcuts import render
from django.http import QueryDict, HttpResponse, JsonResponse
# from django.core import serializers
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from .models import RequestVendor
import json
from .vendor.stragy import *
# Create your views here.


def index(req):
    context = {

    }
    return render(req, "address/index.html", context=context)


def render_login(req):
    context = {

    }
    return render(req, "address/signin.html", context=context)


def address(request):
    if request.method == 'POST':
        post = QueryDict(request.body)
        # vendor = post.get('vendor')
        vendor_id = post.get('vendor_id')
        vendor_password = post.get('vendor_password')
        # postcode = post.get('postcode')
        address = post.get('address')
        details = post.get('details')
        recipient = post.get('recipient')
        shipping_address = post.get('shipping_address')
        phone_number_head = post.get('phone_number_head')
        phone_number_middle = post.get('phone_number_middle')
        phone_number_tail = post.get('phone_number_tail')
        print(
            vendor_id,
            vendor_password,
            address,
            details,
            recipient,
            shipping_address,
            phone_number_head,
            phone_number_middle,
            phone_number_tail)
        context = Context(MusinsaStagy())
        context.address_run(id=vendor_id,
                            password=vendor_password,
                            address=address,
                            address_detail=details,
                            recipient=recipient,
                            shipping_address=shipping_address,
                            phone_number_head=phone_number_head,
                            phone_number_middle=phone_number_middle,
                            phone_number_tail=phone_number_tail)

    return HttpResponse(
        json.dumps({'msg': "come"}),
        content_type='application/json')
    # post = QueryDict(request.body)
    # task = post.get('task')

    # return HttpResponse(
    #     json.dumps(
    #         getAllTask()),
    #     content_type='application/json')
    # return render(req, "address/signin.html", context=context)
