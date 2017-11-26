from .models import Component, ComponentType, Package, Supplier, Inventory, Warehouse, Location
from django import forms

class ComponentTypeForm(forms.ModelForm):
    class Meta:
        model = ComponentType
        fields = ["name", "description", "upper_level", "measurement_units"]

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ["name", "description", "component_type", "package", "value", "unit_multiplier"]

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ["name", "description"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "description", "supplier_type", "url"]

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "description", "latitude", "longitude", "managed_by"]

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "description", "warehouse"]

LIBS = [("Типы компонентов", "ctypes", ComponentType, ComponentTypeForm),
        ("Компоненты", "comps", Component, ComponentForm),
        ("Корпуса", "packages", Package, PackageForm),
        ("Поставщики", "suppliers", Supplier, SupplierForm)
        ]

def show_inventory(warehouse=None):
    if warehouse is not None:
        current_units = Inventory.objects.filter(location__warehouse=warehouse, count__gt=0)
    else:
        current_units = Inventory.objects.filter(count__gt=0)
    return (current_units)

def get_available_libraries():
    out = []
    for l in LIBS:
        current = {
            "name": l[0],
            "shortname": l[1],
            "model": l[2],
            "objs": l[2].objects.all(),
            "form": l[3]
        }
        out.append(current)
    return out
