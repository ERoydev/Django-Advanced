from django.http import HttpResponse
from django.shortcuts import render


class BaseView:
    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls()

            # dispatch
            if request.method == "GET":
                return self.get(request, *args, **kwargs)
            else:
                return self.post(request, *args, **kwargs)

        return view


class IndexView(BaseView):
    def get(self, request):
        return HttpResponse('Class Based Views')



def index(request):
    return HttpResponse('Function Based Views')