# -*- coding: utf-8 -*-
from rest_framework import serializers

from news.models import Topic, Segment, Channel, ChannelAudience


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name')


class ChannelAudienceSerializer(serializers.ModelSerializer):
    channel = serializers.CharField(source='channel.name', read_only=True)

    class Meta:
        model = ChannelAudience
        fields = ('id', 'timestamp', 'audience', 'channel')


class SegmentSerializer(serializers.ModelSerializer):
    channel = serializers.CharField(source='channel.name', read_only=True)

    class Meta:
        model = Segment
        fields = ('id', 'start', 'end', 'channel')


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name', 'count', 'score', 'segment')


class TopicNameChannelSerializer(serializers.ModelSerializer):
    channel = serializers.CharField(source='segment.channel.name', read_only=True)

    class Meta:
        model = Topic
        fields = ('name', 'channel')
