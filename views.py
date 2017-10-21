from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def getter(request):
    json_string = request.body.decode("utf-8")
    return HttpResponse()
