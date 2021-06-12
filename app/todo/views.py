# from django.shortcuts import render

# # Create your views here.


# def index(req):
#     context = {

#     }
#     return render(req, "index.html", context=context)
from .models import Todo
# from .serializers import TodoSerializer
from django.http import JsonResponse
from django.core import serializers
import json


def selectAll(request):
    todo_list = Todo.objects.all().order_by('created_at')
    # .values('task')
    #   .only("todo", "created_at")
    serializers_todo_list = serializers.serialize("json", todo_list)
    return JsonResponse({'todo_list': serializers_todo_list})


def selectOne(request):
    todo_list = Todo.objects.get(
        user_id='saecomaster').filter(user_id='saecomaster')
    print(todo_list)
    serializers_todo_list = serializers.serialize("json", todo_list)
    return JsonResponse({'todo_list': serializers_todo_list})


def insert(request):
    todo = Todo(user_id='saeco', task='장고 꽤 어렵네', highlight=1)
    todo.save()
    return JsonResponse({'msg': '성공'})


def delete(request):
    pass
