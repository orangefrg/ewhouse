from django.conf.urls import url, include
from django.contrib import admin
from ewhouse.views import loginpage, check_user, log_out, inventory, operations, operations_multiple, operations_query, operations_file, library, warehouses

admin.autodiscover()

urlpatterns = [url(r'^name_yourself/$', loginpage, name='login'),
               #url(r'^test_page/$', testpage, name='testpage'),
               #url(r'^main/$', mainpage, name='mainpage'),
               url(r'^check_user/$', check_user, name='check_user'),
               url(r'^inventory/$', inventory, name='inventory'),
               url(r'^inventory/(?P<warehouse_id>[0-9]+)/$', inventory, name='inventory'),
               url(r'^logout/$', log_out, name='log_out'),
               url(r'^ops/$', operations, name='operations'),
               url(r'^ops/manual$', operations_multiple, name='operations_multiple'),
               url(r'^ops/query$', operations_query, name='operations_query'),
               url(r'^ops/file$', operations_file, name='operations_file'),
               url(r'^warehouses/$', warehouses, name='warehouses-all'),
               url(r'^warehouses/(?P<wh_id>[0-9]+)/$', warehouses, name='warehouses-one'),
               url(r'^warehouses/edit/$', warehouses, {'edit_wh': True}, name='warehouses-all-edit'),
               url(r'^warehouses/(?P<wh_id>[0-9]+)/(?P<loc_id>[0-9]+)/$', warehouses, name='warehouses-loc'),
               url(r'^warehouses/(?P<wh_id>[0-9]+)/delete/$', warehouses, {'delete_wh': True}, name='warehouses-one-del'),
               url(r'^warehouses/(?P<wh_id>[0-9]+)/edit/$', warehouses, {'edit_wh': True}, name='warehouses-one-edit'),
               url(r'^warehouses/(?P<wh_id>[0-9]+)/(?P<loc_id>[0-9]+)/delete/$', warehouses, {'delete_loc': True},
                   name='warehouses-loc-del'),
               url(r'^library/$', library, name='library'),
               url(r'^library/(?P<library_name>[\w]+)/$', library, name='library-plain'),
               url(r'^library/(?P<library_name>[\w]+)/(?P<entity_id>[0-9]+)/$', library, name='library-obj'),
               url(r'^library/(?P<library_name>[\w]+)/(?P<entity_id>[0-9]+)/delete/$',
                   library, {'delete': True}, name='library-obj-delete')
               ]
