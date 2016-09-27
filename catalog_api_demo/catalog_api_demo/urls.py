from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from views import class_search_api

urlpatterns = [
	url(r'^catalog_api_demo/class_search_api/$', class_search_api),
]
urlpatterns += staticfiles_urlpatterns()
