from .models import Component, Inventory, Transaction, AtomicTransaction, Location
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from random import randint

def make_atomic_transaction(transaction, count, component,
                            from_location=None, to_location=None, price=None):
    at = AtomicTransaction(
        transaction = transaction,
        count = count,
        component = component,
        price = price,
        from_location = from_location,
        to_location = to_location
    )
    at.save()
    return at

def get_items_count(component, location):
    return location.inventory_set.filter(unit=component).aggregate(Sum('count'))['count__sum']

def check_availability(component, count, location):
    return get_items_count(component, location) >= count

def find_inventory_by_price(location, component, price):
    try:
        return location.inventory_set.filter(unit=component, price=price).get()
    except ObjectDoesNotExist:
        return None

def find_non_empty_inventories(location, component):
    invs = location.inventory_set.filter(unit=component, count__gt=0)
    if invs.count() == 0:
        return None
    return invs

def execute_atomic_transaction(at):
    remaining_count = at.count
    for inv in find_non_empty_inventories(at.from_location, at.component):
        if inv.count < remaining_count:
            to_add = inv.count
            inv.count = 0
            remaining_count -= to_add
            if at.price is None:
                to_inv = find_inventory_by_price(at.to_location, at.component, price)
                if to_inv is None:
                    to_inv = Inventory(
                        unit = at.component,
                        location = at.to_location,
                        count = to_add,
                        price = inv.price
                    )
                else:
                    to_inv.count += to_add
                to_inv.save()
            inv.save()
        else:
            to_add = remaining_count
            inv.count -= remaining_count
            if at.price is None:
                to_inv = find_inventory_by_price(at.to_location, at.component, price)
                if to_inv is None:
                    to_inv = Inventory(
                        unit = at.component,
                        location = at.to_location,
                        count = to_add,
                        price = inv.price
                    )
                else:
                    to_inv.count += to_add
                to_inv.save()
            inv.save()
            break
    if at.price is not None:
        to_inv = find_inventory_by_price(at.to_location, at.component, at.price)
        if to_inv is None:
            to_inv = Inventory(
                unit = at.component,
                location = at.to_location,
                count = at.count,
                price = at.price
            )
        else:
            to_inv.count += at.count
        to_inv.save()
    at.is_completed = True
    at.save()

def create_transaction(user, name, description, transaction_type, supplier=None):
    transaction = Transaction(
        author = user,
        transaction_type = transaction_type,
        supplier = supplier,
        name = name,
        description = description
    )
    transaction.save()
    return transaction

def find_recursively(component, current_loc, count_left, variant, excl_location_ids=[], maximum_variants=5):
    all_variants = []
    cnt = get_items_count(component, current_loc)
    if cnt == 0:
        return None
    excl_location_ids.append(current_loc.id)
    if cnt >= count_left:
        variant.append({"location": current_loc, "count": count_left, "will_be_left": cnt - count_left})
        all_variants.append(variant)
        return all_variants
    variant.append({"location": current_loc, "count": cnt, "will_be_left": 0})
    count_left -= cnt
    for loc in Location.objects.exclude(id__in=excl_location_ids):
        new_variant = list(variant)
        result = find_recursively(component, loc, count_left, new_variant, excl_location_ids, maximum_variants)
        if result is not None:
            print("Result length is {}".format(len(result)))
            # Simple for as foreach didn't work here, so here goes old-school for
            for v in range(len(result)):
                if len(all_variants) >= maximum_variants:
                    return all_variants
                else:
                    all_variants.append(result[v])
    if len(all_variants)>0:
        return all_variants
    else:
        return None

def find_items(component, count, excl_location=None, maximum_variants=10):
    all_variants = []
    if excl_location is not None:
        all_locs = Location.objects.exclude(id=excl_location.id)
        excl_location_ids = [excl_location.id]
    else:
        all_locs = Location.objects.all()
        excl_location_ids = []
    for l in all_locs:
        res_variants = find_recursively(component, l, count, [], list(excl_location_ids), maximum_variants)
        if res_variants is not None:
            all_variants += res_variants
    # Filter by warehouse
    # TODO: Filtering by warehouse
    # TODO: Logistics - use only closest possible warehouses
    return all_variants