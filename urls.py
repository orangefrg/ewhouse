from django.conf.urls import url
from django.contrib import admin
from ewhouse.views import loginpage, testpage

admin.autodiscover()

urlpatterns = [url(r'^name_yourself/$', loginpage, name='login'),
               url(r'^test_page/$', testpage, name='testpage')]
