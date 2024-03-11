from django.shortcuts import render
from django.http import HttpResponseNotFound
from . import pages
from .settings import IS_LOCAL_INSTANCE


def home(request):
    return pages.Home(request).render()


def add_stock(request):
    return pages.NewStock(request).render()


def modify_stock(request, id):
    return pages.ModifyStock(request, id).render()


def add_other(request):
    return pages.NewOther(request).render()


def modify_other(request, id):
    return pages.ModifyOther(request, id).render()


def settings(request):
    if not IS_LOCAL_INSTANCE:
        return HttpResponseNotFound()
    return pages.Settings(request).render()


def handle404(request, exception):
    return render(request, '404.html', {})
