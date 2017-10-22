from django.db import models
import uuid

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

TRANSACTION_TYPES = (
    ("BUY", "Buy"),
    ("SELL", "Sell"),
    ("USE", "Use"),
    ("LOSE", "Lose"),
    ("DISCOVER", "Discover"),
    ("OTHER", "Other")
)

class User(models.Model):
    name = models.TextField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    is_active = models.BooleanField(default=False)

class ComponentMacroType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class ComponentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    macro_type = models.ForeignKey(ComponentMacroType, null=True)

class Component(models.Model):
    name = models.CharField(max_length=100, unique=True)
    component_type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    package = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    value = models.FloatField()

class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    updated = models.DateTimeField()

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    address_a = models.CharField(max_length=50)
    address_b = models.CharField(max_length=50)

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    supplier_type = models.CharField(max_length=10, choices=SUPPLIER_TYPES)
    website = models.TextField(blank=True)
    other_contacts = models.TextField(blank=True)

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
    location = models.ForeignKey(Position, on_delete=models.CASCADE)
    days_to_arrive = models.IntegerField()
    current_count = models.IntegerField()

class PriceInfo(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

class Transaction(models.Model):
    t_date = models.DateTimeField()
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    units = models.ManyToManyField(Unit)