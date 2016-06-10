# -*- coding: utf-8 -*-
"""
URL Configuration.
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from news.viewsets import TopicViewSet, SegmentViewSet, ChannelAudienceViewSet

router = DefaultRouter()
router.register(r'topic', TopicViewSet)
router.register(r'segment', SegmentViewSet)
router.register(r'channel_audience', ChannelAudienceViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
]
