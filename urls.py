from django.conf.urls import url
from django.contrib import admin
from ewhouse.views import getter, all_items

admin.autodiscover()

urlpatterns = [url(r'^getter/$', getter, name='getter'),
               url(r'^units/$', all_items, name='all_items')]
