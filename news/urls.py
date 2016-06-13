# -*- coding: utf-8 -*-
"""
URL Configuration.
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from news.viewsets import TopicViewSet, SegmentViewSet, ChannelAudienceViewSet

router = DefaultRouter()
router.register(r'topic', TopicViewSet)
router.register(r'segment', SegmentViewSet)
router.register(r'channel_audience', ChannelAudienceViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='news/home.html'), name='home'),
    url(r'^topic_by_channel/?$', TemplateView.as_view(template_name='news/topic_by_channel.html'),
        name='topic_by_channel'),
    url(r'^topic_performance/?$', TemplateView.as_view(template_name='news/topic_performance.html'),
        name='topic_performance'),
    url(r'^topic_best_segments/?$', TemplateView.as_view(template_name='news/topic_best_segments.html'),
        name='topic_best_segments'),
    url(r'^api/', include(router.urls, namespace='v1')),
]
