from .models import Component, Inventory, Warehouse

def show_inventory(warehouse=None):
    if warehouse is not None:
        current_units = Inventory.objects.filter(location__warehouse=warehouse, count__gt=0)
    else:
        current_units = Inventory.objects.filter(count__gt=0)
    return (warehouse, current_units)