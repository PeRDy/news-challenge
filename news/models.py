"""
News models.
"""
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_pandas.managers import DataFrameManager


class Channel(models.Model):
    """
    Represents a Channel.
    """
    name = models.CharField(_('name'), max_length=200)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Channel{%s}" % (self.name, )


class ChannelAudience(models.Model):
    """
    Represents audience in a channel.
    """
    timestamp = models.DateTimeField(_('timestamp'))
    audience = models.BigIntegerField(_('audience'))
    channel = models.ForeignKey(Channel, verbose_name=_('channel'))

    # Change default manager to easy use pandas DataFrame
    objects = DataFrameManager()

    def __str__(self):
        return "%s (%s)" % (self.audience, str(self.timestamp))

    def __repr__(self):
        return "ChannelAudience{%s, %s, %s}" % (self.channel, self.audience, str(self.timestamp))


class Segment(models.Model):
    """
    Represents a segment.
    """
    start = models.DateTimeField(_('start timestamp'))
    end = models.DateTimeField(_('end timestamp'))
    channel = models.ForeignKey(Channel, verbose_name=_('channel'))

    # Change default manager to easy use pandas DataFrame
    objects = DataFrameManager()

    def __str__(self):
        return "[%s - %s]" % (str(self.start), str(self.end))

    def __repr__(self):
        return "Segment{%s, %s, %s}" % (repr(self.channel), str(self.start), str(self.end))


class Topic(models.Model):
    """
    Represents a topic with:

    * Name: Name of the topic.
    * Count: Number of time the topic was mentioned in the segment.
    * Score: Higher means the topic is more relevant to the segment.
    """
    name = models.CharField(_('name'), max_length=1000)
    count = models.IntegerField(_('count'))
    score = models.FloatField(_('score'))
    segment = models.ForeignKey(Segment, verbose_name=_('segment'))

    # Change default manager to easy use pandas DataFrame
    objects = DataFrameManager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Topic{%s, %d, %.2f}" % (self.name, self.count, self.score)
