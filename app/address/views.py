from django.shortcuts import render
from django.http import QueryDict, HttpResponse, JsonResponse
# from django.core import serializers
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from .models import RequestVendor
import json
from .vendor.stragy import StragyVendor
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
        vendor = post.get('vendor')
        vendor_id = post.get('vendor_id')
        vendor_password = post.get('vendor_password')
        postcode = post.get('postcode')
        address = post.get('address')
        details = post.get('details')
        print(vendor, vendor_id, vendor_password, postcode, address, details)

        StragyVendor
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
