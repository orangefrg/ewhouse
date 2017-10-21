from django.db import models

USER_ROLES = (
    ("ADMIN", "Administrator"),
    ("EDITOR", "Editor"),
    ("VIEWER", "Viewer"))

SUPPLIER_TYPES = (
    ("LOCAL", "Local"),
    ("NATIONAL", "National"),
    ("FOREIGN", "Foreign"),
    ("OTHER", "Other")
)

class ComponentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

class PackageType(models.Model):
    name = models.CharField(max_lenthg=100, unique=True)

class Component(models.Model):
    name = models.CharField(max_length=100, unique=True)
    component_type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE)
    description = models.TextField()
    datasheet_name = models.CharField(max_length=100, unique=True)
    value = models.FloatField()

class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    updated = models.DateTimeField()

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    supplier_type = models.CharField(max_length=10, choices=SUPPLIER_TYPES)
    website = models.TextField()
    other_contacts = models.TextField()

class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    symbol = models.CharField(max_length=10)

class Unit(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    where_from = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    is_ok = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    days_to_arrive = models.IntegerField()
    count = models.IntegerField()

class PriceInfo(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
