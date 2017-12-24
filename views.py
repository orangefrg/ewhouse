from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import loader
from .models import Package
from .models import Package, Warehouse, Location, ComponentType, Component, Supplier, Inventory, Device, DeviceParts
from .presenters import show_inventory, get_available_libraries, WarehouseForm, LocationForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django import forms
from .forms import OperationForm, ManualOperationForm
from .workers import find_items, check_availability
import simplejson, sys

LOGIN_PAGE = '/ewhouse/name_yourself/'
MAIN_PAGE = '/ewhouse/inventory/'

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
def inventory(request, warehouse_id=None):
    if warehouse_id is not None:
        try:
            wh = Warehouse.objects.get(id=warehouse_id)
        except ObjectDoesNotExist:
            wh = None
            exc = "Склад не найден!"
    else:
        wh = None
    units = show_inventory(wh)
    template = loader.get_template('inventory.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'items': units, 'warehouse': wh, 'warehouses': Warehouse.objects.all()}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def operations_query(request):
    if request.method == "POST":
        form = OperationForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            excl_location = cdata["to_location"]
            component = cdata["component"]
            count = cdata["count"]
            variants = find_items(component, count, excl_location)
    else:
        form = OperationForm()
        variants = None
    template = loader.get_template('operations_query.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'form': form, 'variants': variants}
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_PAGE)
def operations_manual(request):
    template = loader.get_template('operations_manual.html')
    availability = []
    if request.method == "POST":
        form = ManualOperationForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            comp = cdata["component"]
            locs = form.get_location_tuples()
            for l in locs:
                av = check_availability(comp, l[1], l[0])
                availability.append((av, comp, l[1], l[0]))
    else:
        form = ManualOperationForm()
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'form': form, 'availability': availability}
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_PAGE)
def operations_file(request):
    template = loader.get_template('operations_file.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email}
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_PAGE)
def operations(request):
    template = loader.get_template('operations.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email}
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_PAGE)
def warehouses(request, wh_id=None, loc_id=None, delete_loc=None, exc=None, delete_wh=None, edit_wh=None):
    template = loader.get_template('warehouses.html')
    warehouse = None
    location = None
    exc = None
    warehouses = Warehouse.objects.all()
    loc_form = LocationForm()
    wh_form = WarehouseForm()
    if wh_id is not None:
        try:
            warehouse = Warehouse.objects.get(id=wh_id)
            wh_form = WarehouseForm(instance=warehouse)
            if delete_wh:
                if request.user in warehouse.managed_by.all():
                    warehouse.delete()
                    return redirect('warehouses-all')
                else:
                    exc = ("danger", "Недостаточно прав для удаления склада")
            elif edit_wh:
                if request.method == "POST":
                    if request.user in warehouse.managed_by.all():
                        wh_form = WarehouseForm(request.POST, instance=warehouse)
                        if wh_form.is_valid():
                            wh = wh_form.save()
                            exc = ("success", "Склад успешно изменён")
                            return redirect('warehouses-one', wh_id = wh.id)
                        else:
                            exc = ("warning", "Ошибка заполнения формы")
                            return redirect('warehouses-all')
                    else:
                        exc = ("danger", "Недостаточно прав для редактирования склада")
            elif loc_id is not None:
                location = Location.objects.filter(warehouse=warehouse).get(id=loc_id)
                if delete_loc:
                    if request.user not in location.warehouse.managed_by.all():
                        exc = ("danger", "Недостаточно прав для редактирования склада")
                    else:
                        location.delete()
                        return redirect('warehouses-one', wh_id=location.warehouse.id)
                elif request.method == "POST":
                    loc_form = LocationForm(request.POST, instance=location)
                    if loc_form.is_valid():
                        if request.user not in location.warehouse.managed_by.all():
                            exc = ("danger", "Недостаточно прав для редактирования склада")
                        else:
                            loc_form.save()
                            exc = ("success", "Расположение успешно изменено")
                    else:
                        exc = ("warning", "Ошибка заполнения формы")
                else:
                    loc_form = LocationForm(instance=location)

            elif request.method == "POST":
                loc_form = LocationForm(request.POST)
                if loc_form.is_valid():
                    loc_form.save()
                    exc = ("success", "Расположение успешно добавлено")
                else:
                    exc = ("warning", "Ошибка заполнения формы")
            loc_form.fields['warehouse'].initial = warehouse.id
            loc_form.fields['warehouse'].widget = forms.HiddenInput()

        except ObjectDoesNotExist:
            exc = ("danger", "Склад или расположение не найдены")
            return redirect('warehouses-all', exc=exc)
    elif edit_wh:
        wh_form = WarehouseForm(request.POST)
        if wh_form.is_valid():
            wh_form.save()
            return redirect('warehouses-all')
        else:
            exc = ("warning", "Ошибка заполнения формы")

    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'current_wh': warehouse, 'current_loc': location,
               'all_wh': warehouses, 'exc': exc, 'current_usr': request.user,
               'loc_form': loc_form, 'wh_form': wh_form}
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_PAGE)
def library(request, library_name=None, entity_id=None, delete=False, exc=None):
    libs = get_available_libraries()
    curlib = None
    curobj = None
    if library_name is not None:
        for l in libs:
            if l["shortname"] == library_name:
                curlib = l
                if entity_id is not None:
                    try:
                        curobj = curlib["model"].objects.get(id=entity_id)
                        if delete:
                            curobj.delete()
                            return redirect('library-plain', library_name=library_name)
                        elif request.method == "POST":
                            curlib["form"] = curlib["form"](request.POST, instance=curobj)
                            if curlib["form"].is_valid():
                                curlib["form"].save()
                                exc = ("success", "Объект успешно изменён")
                        else:
                            curlib["form"] = curlib["form"](instance=curobj)
                    except ObjectDoesNotExist:
                        exc = ("danger", "Объект не найден")
                        curobj = None
                elif request.method == "POST":
                    curlib["form"] = curlib["form"](request.POST)
                    if curlib["form"].is_valid():
                        curlib["form"].save()
                        exc = ("success", "Объект успешно добавлен")
                break
        if curlib is None:
            exc = ("danger", "Библиотека не найдена")
    template = loader.get_template('library_main.html')
    context = {'name': request.user.first_name, 'lastname': request.user.last_name,
               'email': request.user.email, 'libs': libs, 'curlib': curlib, 'curobj': curobj,
               'exc': exc}
    return HttpResponse(template.render(context, request))
