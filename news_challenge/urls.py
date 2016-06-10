# -*- coding: utf-8 -*-
"""
URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

import news.urls

urlpatterns = [
    url(r'^backend/', include(admin.site.urls)),
    url(r'^news/', include(news.urls)),
]
