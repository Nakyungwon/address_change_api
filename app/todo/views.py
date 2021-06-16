from django.shortcuts import render
from .models import Todo
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import QueryDict
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

# def BootStrap(request):
# return render(request, 'todo/base.html')

# @method_decorator(csrf_exempt, name='dispatch')
def selectAll(request):
    if request.method == 'GET':
        # todo_list = Todo.objects.all().order_by('created_at')
        # serializers_todo_list = serializers.serialize("json", todo_list)
        return render(request, 'todo/index.html', {'todo_list': getAllTask()})


def getAllTask() -> list:
    todo_list = Todo.objects.all().order_by('-created_at')
    # todo_list = Todo.objects.values_list(
    #     'task', 'do_yn', 'pk').order_by('-created_at')
    print(todo_list)
    serializers_todo_list = serializers.serialize("json", todo_list)
    return json.loads(serializers_todo_list)
    # <QuerySet [('장고 너무 어렵당', 0, 13), ('123', 0, 12), ('asdasdasd', 0, 11), ('sdfsdfdsf', 0, 10), ('asdasdsad', 0, 9), ('asdasdsads', 0, 8)]>
    # <QuerySet [<Todo: 장고 너무 어렵당>, <Todo: 123>, <Todo: asdasdasd>, <Todo: sdfsdfdsf>, <Todo: asdasdsad>, <Todo: asdasdsads>]>


def Do(request):
    if request.method == 'POST':
        post = QueryDict(request.body)
        task = post.get('task')
        todo_obj = Todo()
        todo_obj.task = task
        todo_obj.user_id = 'saecomaster1'
        todo_obj.save()

        return HttpResponse(json.dumps(getAllTask()), content_type='application/json')
    if request.method == 'PUT':
        put = QueryDict(request.body)
        pk = put.get('pk', None)
        do_yn = put.get('do_yn', None)

        todo_obj = Todo.objects.get(id=pk)
        todo_obj.do_yn = 1 if do_yn == 'true' else 0
        todo_obj.save()

        list = getAllTask()
        print(list)

        return HttpResponse(json.dumps(getAllTask()), content_type='application/json')
    if request.method == 'DELETE':
        put = QueryDict(request.body)
        pk = put.get('pk', None)
        todo_obj = Todo.objects.get(id=pk)
        todo_obj.delete()
        context = {
            'do': "yes"
        }
        return HttpResponse(json.dumps(getAllTask()), content_type='application/json')
