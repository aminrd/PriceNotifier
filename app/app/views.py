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
    page = pages.Home()
    return page.render(request)


def add_stock(request):
    page = pages.NewStock()
    return page.render(request)


def modify_stock(request, id):
    page = pages.ModifyStock(id)
    return page.render(request)


def add_other(request):
    page = pages.NewOther()
    return page.render(request)


def modify_other(request, id):
    page = pages.ModifyOther(id)
    return page.render(request)


def settings(request):
    page = pages.Settings()
    return page.render(request)


def handle404(request, exception):
    return render(request, '404.html', {})
