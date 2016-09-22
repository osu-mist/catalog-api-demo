from django.conf.urls import url, include
from django.contrib import admin

from views import catalog_api_demo

urlpatterns = [
	url(r'^catalog_api_demo/$', catalog_api_demo),
]
