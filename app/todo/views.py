from django.shortcuts import render
from .models import Todo
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# @method_decorator(csrf_exempt, name='dispatch')
# class TodoView(View):
#     def post(self, request):
#         return HttpResponse("post 요청")

#     def get(self, request):
#         todo_list = Todo.objects.all().order_by('created_at')
#         serializers_todo_list = serializers.serialize("json", todo_list)
#         return JsonResponse({'todo_list': 'come'})

#     def put(self, request):
#         return HttpResponse("put 요청")

#     def delete(self, request):
#         return HttpResponse("delete 요청")


# @method_decorator(csrf_exempt, name='dispatch')
def selectAll(request):
    if request.method == 'GET':
        todo_list = Todo.objects.all().order_by('created_at')
        serializers_todo_list = serializers.serialize("json", todo_list)
        return render(request, 'todo/index.html', {'todo_list': json.loads(serializers_todo_list)})


# def selectOne(request, id):
#     todo_list = Todo.objects.filter(id=id)
#     print(todo_list)
#     serializers_todo_list = serializers.serialize("json", todo_list)
#     return JsonResponse({'todo_list': serializers_todo_list})


# def insert(request):
#     todo = Todo(user_id='saeco', task='장고 꽤 어렵네', highlight=1)
#     todo.save()
#     return JsonResponse({'msg': '성공'})


# def delete(request):
#     pass
