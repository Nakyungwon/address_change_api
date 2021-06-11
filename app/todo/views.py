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

def my_view(request):
    todo_list = Todo.objects.all()
    serializers_todo_list = serializers.serialize("json",todo_list)
    return JsonResponse({'todo_list': serializers_todo_list})