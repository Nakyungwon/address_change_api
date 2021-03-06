from django.shortcuts import render, redirect, reverse
from django.http import QueryDict, HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, RequestContext
import json
import hashlib
import abc
from django.conf import settings
from django.core import serializers
import importlib
from .models import UserInfo, RequestVendor, Vendor
from django.contrib.auth.models import User
from django.contrib import auth
from utils.token import JWTToken, AES128Crypto
from django.utils.safestring import mark_safe
import logging
logger = logging.getLogger(__name__)
# Create your views here.
JWT_SECRET_KEY = getattr(settings, 'JWT_SECRET_KEY', None)
ALGORITHM = getattr(settings, 'ALGORITHM', None)


def room(request, room_name):
    return render(request, 'address/index.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def health(request):
    stage = getattr(settings, 'STAGE', None)
    return HttpResponse(json.dumps({'stage': stage}), content_type='application/json')


def index(req):
    vendor_list = []
    import_module = importlib.import_module('address.vendor')
    for sub_key, sub_value in import_module.__dict__.items():
        # if isinstance(sub_value,)
        if isinstance(sub_value, abc.ABCMeta):
            vendor_list.append({'value': sub_key.lower(), 'key': getattr(import_module, sub_key).display_name})

    # room_name = 'abc'
    user_token = req.COOKIES.get('user_token', None)
    context = {
        # "room_name_json": mark_safe(json.dumps(room_name)),
        "vendor_list": vendor_list
    }
    if user_token:
        decoded_token = JWTToken.decodeToken(user_token)
        user_id = decoded_token.get('user_id', None)
        # param = req.GET
        if UserInfo.objects.filter(user_id=user_id).exists():
            user_info = UserInfo.objects.filter(user_id=user_id).values(
                'user_id',
                'user_password',
                'address',
                'address_detail',
                'recipient',
                'postcode',
                'shipping_address',
                'phone_number_head',
                'phone_number_middle',
                'phone_number_tail'
            )[0]

            context['user_info'] = user_info
            request_vendor_list = RequestVendor.objects.filter(user_id=user_id)
            cryption_obj = AES128Crypto()
            for idx, obj in enumerate(request_vendor_list):
                # obj.vendor_password = 123
                obj.vendor_password = cryption_obj.decrypt(obj.vendor_password)

            context['request_vendor_list'] = serializers.serialize("json", request_vendor_list)
        else:
            context['token_delete'] = 'Y'
        
    return render(
        req,
        "address/index.html",
        context=context
    )


def render_signup(req):
    return render(req, "auth/signup.html")


def check_id(req):
    if req.method == 'POST':
        body = json.loads(req.body)
        is_user_id = False
        if UserInfo.objects.filter(user_id=body['user_id']).exists():
            is_user_id = True
        return HttpResponse(json.dumps({'is_user_id': is_user_id}), content_type='application/json')


def vendor_request(req):
    if req.method == 'POST':
        cryption_obj = AES128Crypto()
        user_token = req.COOKIES.get('user_token', None)
        decoded_token = JWTToken.decodeToken(user_token)
        user_id = decoded_token.get('user_id', None)
        data = json.loads(req.body)
        vendor_id_list = data['vendor_id']
        vendor_password_list = list(map(lambda x: cryption_obj.encrypt(x), data['vendor_password']))
        vendor_list = data['vendor']
        for i in range(0, len(vendor_id_list)):
            vendor_id = vendor_id_list[i]
            vendor_password = vendor_password_list[i]
            vendor = vendor_list[i]
            if RequestVendor.objects.filter(user_id=user_id, vendor_pk=vendor).exists():
                request_vendor_info = RequestVendor.objects.get(user_id=user_id, vendor_pk=vendor)
            else:
                request_vendor_info = RequestVendor()
                request_vendor_info.user_id = user_id

            request_vendor_info.vendor_pk = vendor
            request_vendor_info.vendor_id = vendor_id
            request_vendor_info.vendor_password = vendor_password
            request_vendor_info.save()
        return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')
    elif req.method == 'DELETE':
        user_token = req.COOKIES.get('user_token', None)
        decoded_token = JWTToken.decodeToken(user_token)
        user_id = decoded_token.get('user_id', None)
        data = json.loads(req.body)
        vendor_pk = data['vendor']
        request_vendor_info = RequestVendor.objects.get(user_id=user_id, vendor_pk=vendor_pk)
        request_vendor_info.delete()
        return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')


def update_address(req):
    if req.method == 'PUT':
        user_token = req.COOKIES.get('user_token', None)
        decoded_token = JWTToken.decodeToken(user_token)
        user_id = decoded_token.get('user_id', None)
        data = json.loads(req.body)
        user_info = UserInfo.objects.get(user_id=user_id)
        user_info.postcode = data['postcode']
        user_info.recipient = data['recipient']
        user_info.address = data['address']
        user_info.address_detail = data['address_detail']
        user_info.shipping_address = data['shipping_address']
        user_info.phone_number_head = data['phone_number_head']
        user_info.phone_number_middle = data['phone_number_middle']
        user_info.phone_number_tail = data['phone_number_tail']
        user_info.save()
        return HttpResponse(json.dumps({'msg': 'success'}), content_type='application/json')


def signin(req):
    
    if req.method == 'POST':
        data = QueryDict(req.body)
        password = data['user_password'].encode('utf-8')                # ????????? ??????????????? ????????? ????????? ?????????
        # password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # ???????????? ???????????? ??????
        password_crypt = hashlib.sha256(password).hexdigest()
        # password_crypt = password_crypt.decode('utf-8')
        if UserInfo.objects.filter(user_id=data['user_id'], user_password=password_crypt).exists():
            result = UserInfo.objects.\
                filter(user_id=data['user_id']).\
                values('user_id', 'address')
            result = list(result)[0]
            user_token = JWTToken.encodeToken(result)
            return render(req, 'auth/auth.html', context={'user_token': user_token})
        else:
            print('nono')


def signup(req):
    if req.method == 'POST':
        data = QueryDict(req.body)
        user_obj = UserInfo()
        # ???????????? ??????????????? ??????
        if UserInfo.objects.filter(user_id=data['user_id']).exists():
            return HttpResponse(status=400)
        user_obj.user_id = data['user_id']
        # ==== ???????????? ?????????====#
        password = data['user_password'].encode('utf-8')  # ????????? ??????????????? ????????? ????????? ?????????
        password_crypt = hashlib.sha256(password).hexdigest()
        # password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # ???????????? ???????????? ??????
        # DB??? ????????? ??? ?????? ???????????? ????????? ????????? ?????????
        # password_crypt = password_crypt.decode('utf-8')
        # ====================#
        user_obj.user_password = password_crypt
        user_obj.save()
        return render(req, "address/index.html")


def render_signin(req):
    user_token = req.COOKIES.get('user_token')
    if user_token:
        decoded_token = JWTToken.decodeToken(user_token)
        print(decoded_token)
    context = {

    }
    return render(req, "auth/signin.html", context=context)


def render_user_info(req):
    # RequestVendor()
    # Vendor()

    return render(req, "auth/userInfo.html")