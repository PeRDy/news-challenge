# -*- coding: utf-8 -*-
"""
URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^backend/', include(admin.site.urls)),
]
