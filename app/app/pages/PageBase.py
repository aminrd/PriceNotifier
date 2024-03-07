from django.shortcuts import render
from django.core.exceptions import BadRequest
from ..common_variables import APPLICATION_NAME


class PageBase:
    page_name = "Page"
    template_name = "base.html"

    params = dict()

    def get_contex(self):
        cntx = {
            "page_name": self.page_name,
            "APPLICATION_NAME": APPLICATION_NAME
        }
        for k, v in self.params.items():
            cntx[k] = v
        return cntx

    def default_response(self, request):
        return render(request, template_name=self.template_name, context=self.get_contex())

    def get_hanlder(self, request):
        return self.default_response(request)

    def post_hanlder(self, request):
        return BadRequest("Invalid Request")

    def delete_handler(self, request):
        return BadRequest("Invalid Request")

    def render(self, request):
        if request.method == "GET":
            return self.get_hanlder(request)
        elif request.method == "POST":
            return self.post_hanlder(request)
        elif request.method == "DELETE":
            return self.delete_handler(request)
        else:
            return BadRequest("Invalid Request")