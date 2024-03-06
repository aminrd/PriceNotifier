from django.shortcuts import render
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
        for k, v in self.params:
            cntx[k] = v
        return cntx

    def render(self, request):
        return render(request, template_name=self.template_name, context=self.get_contex())
