from django.conf.urls import url, include
from django.contrib import admin
from ewhouse.views import loginpage, check_user, log_out, inventory, operations, library
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
               #url(r'^test_page/$', testpage, name='testpage'),
               #url(r'^main/$', mainpage, name='mainpage'),
               url(r'^check_user/$', check_user, name='check_user'),
               url(r'^inventory/$', inventory, name='inventory'),
               url(r'^inventory/(?P<warehouse_id>[0-9]+)/$', inventory, name='inventory'),
               url(r'^logout/$', log_out, name='log_out'),
               url(r'^ops/$', operations, name='operations'),
               url(r'^library/$', library, name='library'),
               url(r'^library/(?P<library_name>[\w]+)/$', library, name='library-plain'),
               url(r'^library/(?P<library_name>[\w]+)/(?P<entity_id>[0-9]+)/$', library, name='library-obj'),
               url(r'^library/(?P<library_name>[\w]+)/(?P<entity_id>[0-9]+)/delete/$',
                   library, {'delete': True}, name='library-obj-delete')
               #url(r'^api/v0.0/', include(router.urls, namespace='api'))]
               ]

#urlpatterns += router.urls