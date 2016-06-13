# -*- coding: utf-8 -*-
"""
ViewSets defined for API using REST Framework.
"""
import datetime
from functools import partial

import pandas as pd
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from news.models import Topic, ChannelAudience, Segment
from news.serializers import TopicSerializer, TopicNameChannelSerializer, SegmentSerializer, ChannelAudienceSerializer


def add_audience_mean(row: 'pd.DataFrame', audience: 'pd.DataFrame'):
    """
    Function to calculate Segments audience based on all ChannelAudience records that match time range.

    :param row: Row to apply function.
    :param audience: Audience DataFrame.
    :return: Series with sum of audience for each segment.
    """
    return audience[(audience['timestamp'] >= row['start']) &
                    (audience['timestamp'] <= row['end']) &
                    (audience['channel'] == row['channel'])]['audience'].mean()


def add_audience_by_channel_mean(row: 'pd.DataFrame', channel_audience: 'pd.DataFrame'):
    """
    Function to calculate percent difference between segment audience and his channel audience.

    :param row: Row to apply function.
    :param channel_audience: DataFrame with audience by channel.
    :return: Series with mean audience.
    """
    return (channel_audience.ix[row['channel']] - row['audience']) / channel_audience.ix[row['channel']]


class TopicViewSet(viewsets.ModelViewSet):
    """
    Topics related to a Segment. Each topic is defined by a name, the number of times that the topic was mentioned and
    a score.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @list_route()
    def best_by_channel(self, request, *args, **kwargs):
        """
        Given a day, select the topics that works better in each channel.
        """
        if 'date' in request.query_params:
            day = datetime.datetime.strptime(request.query_params['date'], '%Y-%m-%d')
        else:
            day = datetime.datetime.now()

        init_date = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        end_date = init_date + datetime.timedelta(days=1)

        # Get all necessary objects to perform analysis
        all_audience = ChannelAudience.objects.all() \
            .to_dataframe(fieldnames=['timestamp', 'audience', 'channel'], index='id')
        segments_qs = Segment.objects.filter(start__gte=init_date, end__lt=end_date)
        segments = segments_qs.to_dataframe(fieldnames=['start', 'end', 'channel'], index='id')
        topics = Topic.objects.filter(segment__in=segments_qs) \
            .to_dataframe(fieldnames=['name', 'segment__id'], index='id')

        try:
            # Get audience between date range
            audience = all_audience[(all_audience['timestamp'] >= init_date) & (all_audience['timestamp'] < end_date)]

            # Get partial function applying audience dataframe to keyword, necessary to use with pandas apply method
            audience_mean = partial(add_audience_mean, audience=audience)

            # Calculate segments audience
            segments['audience'] = segments.apply(audience_mean, axis=1)

            # Merge topics and segments data
            df = pd.merge(topics, segments, how='inner', left_on='segment__id', right_index=True)

            # Convert index (id) to column
            df.reset_index(level=0, inplace=True)

            # Group topics by name and later by channel and then get audiences mean
            df = df.groupby(['name', 'channel'], as_index=False).mean()

            # Get channel mean audience and partial function to calculate segments mean audience by channel audience
            channel_mean_audience = all_audience.groupby(['channel'])['audience'].mean()
            audience_by_channel = partial(add_audience_by_channel_mean, channel_audience=channel_mean_audience)

            # Apply function to get normalized audience
            df['audience_mean'] = df.apply(audience_by_channel, axis=1)

            # Again, group by name, and keep only topics with max audience
            df['audience_mean'] = df.groupby(['name'], as_index=False)['audience_mean'].max()['audience_mean']

            # Last step, clean duplicates
            df.dropna().drop_duplicates('name', inplace=True)

            result = [{"name": k, "topics": list(v)} for k, v in df.groupby(['channel'])['name']]
        except ValueError:
            result = []

        return Response(data=result)

    @list_route()
    def performance(self, request, *args, **kwargs):
        """
        Given a topic, calculate performance in each channel.
        """
        topic_name = request.query_params['topic']

        # Get all necessary objects to perform analysis
        topics = Topic.objects.filter(name=topic_name).select_related('segment')
        segments_id = {t.segment.id for t in topics}
        segments = Segment.objects.filter(id__in=segments_id) \
            .to_dataframe(fieldnames=['start', 'end', 'channel'], index='id')
        audience = ChannelAudience.objects.to_dataframe(fieldnames=['timestamp', 'audience', 'channel'], index='id')

        try:
            # Get partial function applying audience dataframe to keyword, necessary to use with pandas apply method
            audience_mean = partial(add_audience_mean, audience=audience)

            # Calculate segments audience
            segments['audience'] = segments.apply(audience_mean, axis=1)

            # Group segments by channel and get audience mean
            df = segments.groupby(['channel'], as_index=False).mean()

            # Get channel mean audience
            channel_mean_audience = audience.groupby(['channel'])['audience'].mean()
            audience_by_channel = partial(add_audience_by_channel_mean, channel_audience=channel_mean_audience)

            # Apply function to calculate performance
            df['audience'] = df.apply(audience_by_channel, axis=1)
            result = df.to_dict('records')
        except ValueError:
            result = []

        return Response(data=result)


class SegmentViewSet(viewsets.ModelViewSet):
    """
    Segments related to a Channel. Each segment is defined by a start and end time, his associated channel and a list of
    topics.
    """
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer

    @list_route()
    def best_segments(self, request, *args, **kwargs):
        """
        Given a topic, look for segments with best audience.
        """
        topic_name = request.query_params['topic']

        # Get all necessary objects to perform analysis
        topics = Topic.objects.filter(name=topic_name).select_related('segment')
        segments_id = {t.segment.id for t in topics}
        segments = Segment.objects.filter(id__in=segments_id) \
            .to_dataframe(fieldnames=['start', 'end', 'channel'], index='id')
        audience = ChannelAudience.objects.to_dataframe(fieldnames=['timestamp', 'audience', 'channel'], index='id')

        try:
            # Get partial function applying audience dataframe to keyword, necessary to use with pandas apply method
            audience_mean = partial(add_audience_mean, audience=audience)

            # Calculate segments audience
            segments['audience'] = segments.apply(audience_mean, axis=1)

            # Get channel mean audience
            channel_mean_audience = audience.groupby(['channel'])['audience'].mean()
            audience_by_channel = partial(add_audience_by_channel_mean, channel_audience=channel_mean_audience)

            # Apply function to calculate performance
            segments['audience_mean'] = segments.apply(audience_by_channel, axis=1)

            # Group segments with max performance
            df = segments.ix[segments.groupby(['channel'], as_index=False)['audience_mean'].idxmax()]

            # Get segments objects
            segments = self.queryset.filter(id__in=set(df.index.tolist())).select_related('channel')
        except ValueError:
            segments = self.queryset.none()

        serializer = SegmentSerializer(segments, many=True)

        return Response(serializer.data)


class ChannelAudienceViewSet(viewsets.ModelViewSet):
    """
    Audience related to a Channel. Is defined with the audience value and the exact time when was measured.
    """
    queryset = ChannelAudience.objects.all()
    serializer_class = ChannelAudienceSerializer
