from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import catalog_api_demo

urlpatterns = [
	url(r'^catalog_api_demo/$', catalog_api_demo),
]
urlpatterns += staticfiles_urlpatterns()