from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Unit
import simplejson


@csrf_exempt
def getter(request):
    json_string = request.body.decode('utf-8')
    return HttpResponse()

@csrf_exempt
def all_items(request):
    objs = Unit.objects.all()
    objs_val = {'objects': list(objs.values('component__name', 'component__component_type__name',
                           'component__component_type__macro_type__name','where_from__name',
                           'price','price_currency__symbol','location__name',
                           'location__warehouse__name','current_count'))}
    ret = JsonResponse(objs_val)
    ret['Access-Control-Allow-Origin'] = '*'
    ret['charset'] = 'utf-8'
    return ret
