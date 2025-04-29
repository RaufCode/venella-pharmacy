from django.http import HttpResponse


def products(request):
    return HttpResponse('Products')