from django.shortcuts import render, redirect, reverse
from django.http import QueryDict, HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, RequestContext
# from django.core import serializers
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from .models import RequestVendor'
import json 
import bcrypt
import jwt
from django.conf import settings
from django.core import serializers
from .models import UserInfo
from django.contrib.auth.models import User
from django.contrib import auth
import json
import jwt
from .vendor.stragy import *
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
    room_name = 'abc'
    # param = req.GET
    return render(
        req,
        "address/index.html",
        {
            "user_token": "abc",
            "room_name_json": mark_safe(json.dumps(room_name))
        }
    )


def render_signup(req):
    context = {

    }
    return render(req, "auth/signup.html", context=context)


def signin(req):
    
    if req.method == 'POST':
        data = QueryDict(req.body)
        # 존재하는 이메일인지 확인
        if UserInfo.objects.filter(user_id=data['user_id']).exists():
            result = UserInfo.objects.\
                filter(user_id=data['user_id']).\
                values('user_id', 'address')
            result = list(result)[0]
            user_token = jwt.encode(result, JWT_SECRET_KEY, algorithm=ALGORITHM)
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
    try:
        if user_token:
            jwt.decode(user_token, options={"verify_signature": False})
            return redirect('/')
    except jwt.exceptions.DecodeError:
        raise
        
    context = {

    }
    return render(req, "auth/signin.html", context=context)


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
