from django.conf.urls import url, include
from django.contrib import admin
from ewhouse.views import loginpage, testpage, check_user, log_out, mainpage, inventory
from ewhouse.views import PackageViewSet, WarehouseViewSet, LocationViewSet, ComponentTypeViewSet, ComponentViewSet, \
    InventoryViewSet, DeviceViewSet, DevicePartsViewSet, SupplierViewSet
from rest_framework import routers

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'comptypes', ComponentTypeViewSet)
router.register(r'comps', ComponentViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'device', DeviceViewSet)
router.register(r'dparts', DevicePartsViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [url(r'^name_yourself/$', loginpage, name='login'),
               url(r'^test_page/$', testpage, name='testpage'),
               url(r'^main/$', mainpage, name='mainpage'),
               url(r'^check_user/$', check_user, name='check_user'),
               url(r'^inventory/$', inventory, name='inventory'),
               url(r'^logout/$', log_out, name='log_out')]
               #url(r'^api/v0.0/', include(router.urls, namespace='api'))]

urlpatterns += router.urls