from django.shortcuts import render

# Create your views here.


def index(req):
    context = {

    }
    return render(req, "address/index.html", context=context)


def render_login(req):
    context = {

    }
    return render(req, "address/login.html", context=context)
