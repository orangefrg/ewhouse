from django.conf.urls import url
from django.contrib import admin
from ewhouse.views import getter

admin.autodiscover()

urlpatterns = [url(r'^getter/$', getter, name='getter')]
