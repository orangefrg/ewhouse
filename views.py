from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import simplejson, sys

@csrf_exempt
def loginpage(request):
    pars = request.POST
    ret = ""
    if pars["uname"] is not None and pars["pwd"] is not None:
        user = authenticate(username=pars["uname"], password=pars["pwd"])
        if user is not None:
            if user.is_active:
                login(request, user)
                print("REDIRECTING...", file=sys.stderr)
                return redirect("success   page    goes    here")
            else:
                ret = "{} {} Inactive".format(user.first_name, user.last_name)
        else:
            ret = "User not found"
    else:
        ret = "Login error"
    print(ret, file=sys.stderr)
    return HttpResponse(ret)

@csrf_exempt
@login_required(login_url='login    url    goes    here')
def testpage(request):
    return HttpResponse("Hello, {} {}".format(request.user.first_name, request.user.last_name))

@csrf_exempt
def all_items(request):
    objs = Unit.objects.all()
    objs_val = {'objects': ''}
    ret = JsonResponse(objs_val)
    ret['Access-Control-Allow-Origin'] = '*'
    ret['charset'] = 'utf-8'
    return ret
