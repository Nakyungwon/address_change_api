from django.shortcuts import render, redirect, reverse
from django.http import QueryDict, HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, RequestContext
# from django.core import serializers
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
import json 
import bcrypt
import abc
from django.conf import settings
from django.core import serializers
import importlib
import types
from .models import UserInfo, RequestVendor, Vendor
from django.contrib.auth.models import User
from django.contrib import auth
# from .vendor.stragy import *
from utils.token import JWTToken
from django.utils.safestring import mark_safe
# Create your views here.
JWT_SECRET_KEY = getattr(settings, 'JWT_SECRET_KEY', None)
ALGORITHM = getattr(settings, 'ALGORITHM', None)


def bad_request_page(request, exception):
    response = render(request, 'address/400.html')
    response.status_code = 400
    return response


def page_not_found_page(request, exception):
    # response = render_to_response('address/error_404_page.html', {}, context_instance=RequestContext(request))
    return render(request, 'address/404.html', status=404)


def server_error_page(request):
    # response = render_to_response('address/error_500_page.html', {}, context_instance=RequestContext(request))
    # response = render(request, 'address/errors/error_500_page.html')
    response = render(request, 'address/500.html')
    response.status_code = 500
    return response


def room(request, room_name):
    return render(request, 'address/index.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def index(req):
    vendor_list = []
    import_module = importlib.import_module('address.vendor')
    for sub_key, sub_value in import_module.__dict__.items():
        # if isinstance(sub_value,)
        if isinstance(sub_value, abc.ABCMeta):
            vendor_list.append({'value': sub_key.lower(), 'key': getattr(import_module, sub_key).display_name})

    room_name = 'abc'
    user_token = req.COOKIES.get('user_token', None)
    context = {
        "room_name_json": mark_safe(json.dumps(room_name)),
        "vendor_list": vendor_list
    }
    if user_token:
        decoded_token = JWTToken.decodeToken(user_token)
        user_id = decoded_token.get('user_id', None)
        # param = req.GET
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
        context['request_vendor_list'] = serializers.serialize("json", request_vendor_list)
        
    return render(
        req,
        "address/index.html",
        context=context
    )


def render_signup(req):
    context = {

    }
    return render(req, "auth/signup.html", context=context)


def vendor_request(req):
    if req.method == 'POST':
        user_token = req.COOKIES.get('user_token', None)
        decoded_token = JWTToken.decodeToken(user_token)
        data = QueryDict(req.body)
        print(data)


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
        password = data['user_password'].encode('utf-8')                # 입력된 패스워드를 바이트 형태로 인코딩
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        password_crypt = password_crypt.decode('utf-8')
        if UserInfo.objects.filter(user_id=data['user_id']).exists():
            result = UserInfo.objects.\
                filter(user_id=data['user_id']).\
                values('user_id', 'address')
            result = list(result)[0]
            user_token = JWTToken.encodeToken(result)
            # res = JsonResponse({'success': True}) 
            # res.set_cookie('user_token', user_token)
            # context = {
            #     "user_token": user_token
            # }
            # content = loader.render_to_string("address/index.html", request=req)
            # return HttpResponse(content, None, None).set_cookie("user_token", user_token)
            # response = render(req, "address/index.html")  # django.http.HttpResponse
            # response.set_cookie(key="user_token", value=user_token)
            return render(req, 'auth/auth.html', context={'user_token': user_token})
        else:
            print('nono')


def signup(req):
    if req.method == 'POST':
        data = QueryDict(req.body)
        user_obj = UserInfo()
        # 존재하는 이메일인지 확인
        if UserInfo.objects.filter(user_id=data['user_id']).exists():
            return HttpResponse(status=400)
        user_obj.user_id = data['user_id']

        # ==== 비밀번호 암호화====#

        password = data['user_password'].encode('utf-8')                # 입력된 패스워드를 바이트 형태로 인코딩
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
        # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
        password_crypt = password_crypt.decode('utf-8')

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
# def address(request):
#     if request.method == 'POST':
#         post = QueryDict(request.body)
#         # vendor = post.get('vendor')
#         vendor_id = post.get('vendor_id')
#         vendor_password = post.get('vendor_password')
#         # postcode = post.get('postcode')
#         address = post.get('address')
#         details = post.get('details')
#         recipient = post.get('recipient')
#         shipping_address = post.get('shipping_address')
#         phone_number_head = post.get('phone_number_head')
#         phone_number_middle = post.get('phone_number_middle')
#         phone_number_tail = post.get('phone_number_tail')
#         print(
#             vendor_id,
#             vendor_password,
#             address,
#             details,
#             recipient,
#             shipping_address,
#             phone_number_head,
#             phone_number_middle,
#             phone_number_tail)
#         context = Context(MusinsaStagy())
#         context.address_run(id=vendor_id,
#                             password=vendor_password,
#                             address=address,
#                             address_detail=details,
#                             recipient=recipient,
#                             shipping_address=shipping_address,
#                             phone_number_head=phone_number_head,
#                             phone_number_middle=phone_number_middle,
#                             phone_number_tail=phone_number_tail)

#     return HttpResponse(
#         json.dumps({'msg': "come"}),
#         content_type='application/json')
    # post = QueryDict(request.body)
    # task = post.get('task')

    # return HttpResponse(
    #     json.dumps(
    #         getAllTask()),
    #     content_type='application/json')
    # return render(req, "address/signin.html", context=context)
