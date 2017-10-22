from django.contrib import admin

# Register your models here.

from .models import ComponentType, ComponentMacroType, Component, Warehouse, Position, \
    Supplier, Currency, Unit, PriceInfo, Transaction


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'id')


class ComponentAdmin(admin.ModelAdmin):
    def typename(self, obj):
        return obj.component_type.name
    def macrotype_name(self, obj):
        if obj.component_type.macro_type is not None:
            return obj.component_type.macro_type.name
        else:
            return "-"
    typename.short_description = 'Component type'
    macrotype_name.short_description = 'Component macrotype'

    list_display = ('name', 'macrotype_name', 'typename', 'package')


class ComponentMacroTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ComponentTypeAdmin(admin.ModelAdmin):
    def macrotype_name(self, obj):
        if obj.macro_type is not None:
            return obj.macro_type.name
        else:
            return "-"
    macrotype_name.short_description = 'Component macrotype'

    list_display = ('macrotype_name', 'name')


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PositionAdmin(admin.ModelAdmin):
    def description(self, obj):
        return "{} @ {}".format(obj.name, obj.warehouse.name)
    description.short_description = 'Description'

    list_display = ('description', 'address_a', 'address_b')


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier_type')


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'rate')


class UnitAdmin(admin.ModelAdmin):
    def comp_name(self, obj):
        return obj.component.name
        comp_name.short_description = 'Component'
    def position_name(self, obj):
        return "{} @ {}".format(obj.location.name, obj.location.warehouse.name)
        position_name.short_description = 'Location'

    list_display = ('comp_name', 'current_count', 'position_name')

class PriceInfoAdmin(admin.ModelAdmin):
    def curr_info(self, obj):
        return obj.price_currency.symbol
        curr_info.short_description = 'Currency'
    def realprice(self, obj):
        return obj.price * obj.price_currency.rate
        realprice.short_description = 'Price in roubles'
    def comp_info(self, obj):
        if obj.component.component_type.macro_type is not None:
            return "{} ({} - {})".format(obj.component.name, obj.component.component_type.name,
                                         obj.component.component_type.macro_type.name)
        else:
            return "{} ({})".format(obj.component.name, obj.component.component_type.name)

        comp_info.short_description = 'Component'
    def supplier_info(self, obj):
        return obj.supplier.name
        supplier_info.short_description = 'Supplier'

    list_display = ('comp_info', 'price', 'curr_info', 'realprice', 'supplier_info')

class TransactionAdmin(admin.ModelAdmin):
    def user_info(self, obj):
        return obj.user.name
    user_info.short_description = 'User'

    list_display = ('t_date', 't_type', 'user_info')

admin.site.register(ComponentMacroType, ComponentMacroTypeAdmin)
admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(PriceInfo, PriceInfoAdmin)
admin.site.register(Transaction, TransactionAdmin)