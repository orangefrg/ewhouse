from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from .models import Package
from rest_framework import viewsets
from .models import Package, Warehouse, Location, ComponentType, Component, Supplier, Inventory, Device, DeviceParts
from .serializers import PackageSerializer, WarehouseSerializer, LocationSerializer, ComponentTypeSerializer,\
    ComponentSerializer, SupplierSerializer, InventorySerializer, DeviceSerializer, DevicePartsSerializer
from .presenters import show_inventory

import simplejson, sys

LOGIN_PAGE = '/ewhouse/name_yourself/'
MAIN_PAGE = '/ewhouse/main/'

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ComponentTypeViewSet(viewsets.ModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DevicePartsViewSet(viewsets.ModelViewSet):
    queryset = DeviceParts.objects.all()
    serializer_class = DevicePartsSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

def loginpage(request):
    template = loader.get_template('login.html')
    context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else MAIN_PAGE,
               'login_unsuccessful': request.GET and 'login_fail' in request.GET and request.GET['login_fail']=="true",
               'logged_out': request.GET and 'logout' in request.GET and request.GET['logout'] == "true"}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def testpage(request):
    template = loader.get_template('test.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def mainpage(request):
    template = loader.get_template('main.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'packages': Package.objects.all()}
    return HttpResponse(template.render(context, request))


def check_user(request):
    username = request.POST["uname"]
    password = request.POST["pwd"]
    next = request.POST["next"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next and len(next)>0:
            return redirect(next)
        else:
            return HttpResponse("OK!")
    else:
        return redirect(LOGIN_PAGE + '?next=' + next + "&login_fail=true")


@login_required(login_url=LOGIN_PAGE)
def log_out(request):
    logout(request)
    return redirect(LOGIN_PAGE + '?logout=true')


@login_required(login_url=LOGIN_PAGE)
def all_items(request):
    objs = Unit.objects.all()
    objs_val = {'objects': ''}
    ret = JsonResponse(objs_val)
    ret['Access-Control-Allow-Origin'] = '*'
    ret['charset'] = 'utf-8'
    return ret


@login_required(login_url=LOGIN_PAGE)
def inventory(request):
    wh, units = show_inventory()
    template = loader.get_template('inventory.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'items': units, 'warehouse': wh, 'warehouses': Warehouse.objects.all()}
    return HttpResponse(template.render(context, request))
