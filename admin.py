from django.contrib import admin

# Register your models here.

from .models import ComponentType, Package, Component, Warehouse, Location, \
    Supplier, Device, AtomicTransaction, Transaction

class ComponentTypeAdmin(admin.ModelAdmin):
    def full_name(self, obj):
        return obj.get_full_name_string()
    list_display = ('full_name', 'description')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ComponentAdmin(admin.ModelAdmin):
    def full_name(self, obj):
        return obj.get_full_name()
    def package_name(self, obj):
        return obj.package.name

    list_display = ('full_name', 'package_name')

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')

class LocationAdmin(admin.ModelAdmin):
    def wh_name(self, obj):
        return obj.warehouse.name
    list_display = ('name', 'wh_name')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier_type', 'url')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AtomicTransactionAdmin(admin.ModelAdmin):
    def from_wh(self, obj):
        if obj.from_location is not None:
            return obj.from_location.warehouse.name
        else:
            return "..."
    def to_wh(self, obj):
        if obj.to_location is not None:
            return obj.to_location.warehouse.name
        else:
            return "..."

    def comp_name(self, obj):
        return obj.component.name

    list_display = ('from_wh', 'to_wh', 'comp_name', 'count', 'price')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('occured_at', 'transaction_type', 'name', 'supplier')

admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(AtomicTransaction, AtomicTransactionAdmin)
admin.site.register(Transaction, TransactionAdmin)