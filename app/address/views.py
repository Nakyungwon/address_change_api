from django.shortcuts import render
from django.http import QueryDict, HttpResponse, JsonResponse
# from django.core import serializers
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from .models import RequestVendor'
import json
import bcrypt
import jwt
from .models import UserInfo
import json
from .vendor.stragy import *
from django.utils.safestring import mark_safe
# Create your views here.


def room(request, room_name):
    return render(request, 'address/index.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


def index(req):
    context = {

    }
    room_name = 'abc'
    return render(
        req,
        "address/index.html",
        {
            "context": context,
            "room_name_json": mark_safe(json.dumps(room_name))
        }
    )


def render_signup(req):
    context = {

    }
    return render(req, "address/signup.html", context=context)


def signin(req):
    if req.method == 'POST':
        data = QueryDict(req.body)
        # 존재하는 이메일인지 확인
        if UserInfo.objects.filter(user_id=data['user_id']).exists():
            print('ok')
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
    context = {

    }
    return render(req, "address/signin.html", context=context)


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
