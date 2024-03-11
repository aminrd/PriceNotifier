import os
from django.http import HttpRequest
from django.shortcuts import render
from django.core.exceptions import BadRequest
from django.contrib.auth.models import User
from ..settings import APPLICATION_NAME, INSTANCE_NAME, IS_LOCAL_INSTANCE


def get_user(request: HttpRequest) -> User:
    if IS_LOCAL_INSTANCE:
        existing_users = User.objects.all()
        if existing_users is None or len(existing_users) < 1:
            username = os.path.expanduser('~')
            user = User.objects.create_user(username)
            user.save()
            return user

        return existing_users[0]

    return request.user


class PageBase:
    page_name = "Page"
    template_name = "base.html"
    user = None
    params = dict()

    def __init__(self, request: HttpRequest):
        self.request = request
        self.user = get_user(request)

    def get_contex(self):
        cntx = {
            "page_name": self.page_name,
            "APPLICATION_NAME": APPLICATION_NAME,
            "INSTANCE_NAME": INSTANCE_NAME,
            "IS_LOCAL": INSTANCE_NAME == "Local"
        }
        for k, v in self.params.items():
            cntx[k] = v
        return cntx

    def default_response(self):
        return render(self.request, template_name=self.template_name, context=self.get_contex())

    def get_hanlder(self):
        return self.default_response()

    def post_hanlder(self):
        return BadRequest("Invalid Request")

    def delete_handler(self):
        return BadRequest("Invalid Request")

    def render(self):
        if self.request.method == "GET":
            return self.get_hanlder()
        elif self.request.method == "POST":
            return self.post_hanlder()
        elif self.request.method == "DELETE":
            return self.delete_handler()
        else:
            return BadRequest("Invalid Request")
