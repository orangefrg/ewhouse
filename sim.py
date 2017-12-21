from .models import Location, Warehouse, Component, Inventory
from decimal import *
import random
from django.db.models import ProtectedError

def generate_single_inventory(location, component, minimum_stock=0, maximum_stock=10, minimum_price=10, maximum_price=100, records=1):
    for r in range(records):
        inv = Inventory(
            unit = component,
            location = location,
            count = random.randint(minimum_stock, maximum_stock),
            price = Decimal(random.randint(minimum_price*100, maximum_price*100))/100
        )
        inv.save()

def generate_location_inventory(location, pass_count=10, records=1):
    for i in range(pass_count):
        cur_type = random.choice(Component.objects.all())
        generate_single_inventory(location, cur_type, records=records)

def generate_random_inventory(excluded_warehouses=[], pass_count=10, records=1):
    for w in Warehouse.objects.all():
        if w in excluded_warehouses:
            continue
        for l in w.location_set.all():
            generate_location_inventory(l, pass_count, records)

def clear_inventory(warehouses=[], force_delete=True):
    if len(warehouse) > 0:
        invs = Inventory.objects.filter(location__warehouse__in=warehouses)
    else:
        invs = Inventory.objects.all()
    for i in invs:
        if force_delete:
            i.delete()
            print("Unit:{} from {} deleted".format(i.unit.name, i.location.name))
        else:
            i.count = 0
            print("Unit:{} from {} count set to zero".format(i.unit.name, i.location.name))


def show_all_components():
    for o in Component.objects.all():
        print("ID:{}, name:{}, package:{}".format(o.id, o.name, o.package.name))
