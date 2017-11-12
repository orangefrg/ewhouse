from django.db import models
from django.contrib.auth.models import User
import uuid

USER_ROLES = (
    ("ADMIN", "Administrator"),
    ("EDITOR", "Editor"),
    ("VIEWER", "Viewer"))

SUPPLIER_TYPES = (
    ("LOCAL", "Local"),
    ("NATIONAL", "National"),
    ("FOREIGN", "Foreign"),
    ("STOCK", "Already in stock"),
    ("OTHER", "Other")
)

TRANSACTION_TYPES = (
    ("BUY", "Buy"),
    ("SELL", "Sell"),
    ("MOVE", "Move"),
    ("USE", "Use"),
    ("LOSE", "Lose"),
    ("GET", "Get"),
    ("OTHER", "Other")
)

MULTIPLIERS = {
    (0, ""),
    (3, "k"),
    (6, "M"),
    (9, "G"),
    (12, "T"),
    (15, "P"),
    (-3, "m"),
    (-6, "u"),
    (-9, "n"),
    (-12, "p"),
    (-15, "f"),
    (-18, "a")
}

class BasicInfo(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    class Meta:
        abstract = True

# Warehouse
class Warehouse(BasicInfo):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    managed_by = models.ManyToManyField(User)

    def total_count(self):
        tcount = 0
        for loc in self.location_set.all():
            tcount += loc.total_count()
        return tcount

    def variations(self):
        vcount = 0
        used = []
        for loc in self.location_set.all():
            for inv in loc.inventory_set.all():
                if inv.unit not in used:
                    vcount += 1
                    used.append(inv.unit)
        return vcount

    def total_price(self):
        tprice = 0
        for loc in self.location_set.all():
            tprice += loc.total_price()
        return tprice

    def __str__(self):
        return self.name

# Particular warehouse location
class Location(BasicInfo):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def total_count(self):
        tcount = 0
        for inv in self.inventory_set.all():
            tcount += inv.count
        return tcount

    def variations(self):
        vcount = 0
        used = []
        for inv in self.inventory_set.all():
            if inv.unit not in used:
                vcount += 1
                used.append(inv.unit)
        return vcount

    def total_price(self):
        tprice = 0
        for inv in self.inventory_set.all():
            tprice += inv.price * inv.count
        return tprice

    def get_full_name(self):
        return "{} @ {}".format(self.name, self.warehouse.name)

    def __str__(self):
        return self.get_full_name()


# Component type, e.g. transistor or capacitor
class ComponentType(BasicInfo):
    upper_level = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.CASCADE)

    measurement_units = models.CharField(max_length=10, null=True, blank=True)

    def is_root(self):
        return self.upper_level is None

    def get_full_name(self):
        fname = []
        if self.upper_level is not None:
            fname = self.upper_level.get_full_name()
        fname.append(self.name)
        return fname

    def get_full_name_string(self):
        fname_arr = self.get_full_name()
        return " - ".join(fname_arr)

    def get_units(self):
        if self.measurement_units is None:
            if self.upper_level is not None:
                return self.upper_level.get_units()
        return self.measurement_units


    def __str__(self):
        return self.get_full_name_string()

# Package type, e.g. TO220 or LQFP144
class Package(BasicInfo):
    def __str__(self):
        return self.name

# Components. Full name goes here, such as STM32F103C8T8
class Component(BasicInfo):
    component_type = models.ForeignKey(ComponentType, on_delete=models.PROTECT)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=30, decimal_places=6, default=None, null=True, blank=True)
    unit_multiplier = models.IntegerField(choices=MULTIPLIERS, default=0)
    location = models.ManyToManyField(Location, through='Inventory')

    def get_units_name(self):
        if self.component_type.get_units() != 0:
            return dict(MULTIPLIERS)[self.unit_multiplier] + self.component_type.get_units()
        else:
            return self.component_type.get_units()

    def get_full_value(self):
        if self.value is not None:
            if self.unit_multiplier != 0:
                return self.value * 10 ^ self.unit_multiplier
            return self.value

    def get_string_value(self):
        if self.value is not None:
            strval = "{:f}".format(self.value).rstrip('0').rstrip('.')
            return "{} {}".format(strval, self.get_units_name())

    def get_full_name(self):
        fname = self.name
        funits = self.get_string_value()
        if funits is not None:
            fname = "{} ({})".format(fname, funits)
        return fname

    def __str__(self):
        return self.get_full_name()

# Suppliers
class Supplier(BasicInfo):
    supplier_type = models.CharField(max_length=10, choices=SUPPLIER_TYPES)
    url = models.URLField(null=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    unit = models.ForeignKey(Component, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Transaction
class Transaction(BasicInfo):
    registered_at = models.DateTimeField(auto_now_add=True)
    occured_at = models.DateTimeField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)

    def __str__(self):
        return "{:%Y-%m-%d %H:%M} ({})".format(self.occured_at, self.name)

# Transaction part
class AtomicTransaction(models.Model):
    component = models.ForeignKey(Component, on_delete=models.PROTECT)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    from_location = models.ForeignKey(Location, null=True, blank=True, related_name='outgoing_transactions')
    to_location = models.ForeignKey(Location, null=True, blank=True, related_name='incoming_transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)

    def __str__(self):
        ret = ""
        from_l = "..." if self.from_location is None else self.from_location.warehouse.name
        to_l = "..." if self.to_location is None else self.to_location.warehouse.name
        return "{}x {} ({} → {})".format(self.count, self.component.name, from_l, to_l)

# Device prototypes
class Device(BasicInfo):
    parts = models.ManyToManyField(Component, through='DeviceParts', related_name='used_in_devices')
    component = models.ForeignKey(Component, on_delete=models.PROTECT, related_name='device_reference')

    def __str__(self):
        return self.name

class DeviceParts(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    part = models.ForeignKey(Component, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
