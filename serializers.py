from rest_framework import serializers
from .models import Package, Warehouse, Location, ComponentType, Component, Supplier, Inventory, Device, DeviceParts

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'description')

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'description', 'managed_by', 'latitude', 'longitude')
        depth = 1

class LocationSerializer(serializers.ModelSerializer):
    warehouse = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Location
        fields = ('id', 'name', 'description', 'warehouse')
        depth = 2

class ComponentTypeSerializer(serializers.ModelSerializer):
    upper_level = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    class Meta:
        model = ComponentType
        fields = ('id', 'name', 'description', 'upper_level', 'measurement_units')

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('id', 'name', 'description', 'component_type', 'package', 'location')
        depth = 2

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'unit', 'location', 'count', 'price')
        depth = 1

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'description', 'supplier_type', 'url')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'description', 'parts', 'component')

class DevicePartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceParts
        fields = ('id', 'device', 'part', 'count')
