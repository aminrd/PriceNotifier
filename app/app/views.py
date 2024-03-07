import uuid

from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import *
from django.utils import timezone
from django.contrib import auth
import itertools
import datetime, re, json

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context
from . import pages


def home(request):
    homepage = pages.Home()
    return homepage.render(request)


def add_stock(request):
    homepage = pages.NewStock()
    return homepage.render(request)


def modify_stock(request, id):
    homepage = pages.ModifyStock()
    return homepage.render(request)

def add_other(request):
    homepage = pages.NewOther()
    return homepage.render(request)


def modify_other(request, id):
    homepage = pages.ModifyOther()
    return homepage.render(request)


def settings(request):
    setting_page = pages.Settings()
    return setting_page.render(request)


def handle404(request, exception):
    return render(request, '404.html', {})
