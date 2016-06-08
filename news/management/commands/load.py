# -*- coding: utf-8 -*-
"""
Command to load data.
"""
import argparse
import datetime
import json
import logging
from itertools import takewhile, zip_longest

from django.core.management import BaseCommand, CommandError

from news.models import Channel, ChannelAudience, Segment, Topic

logger = logging.getLogger(__name__)


def grouper(iterable, n):
    """
    Collect data into fixed-length chunks or blocks.

    :param iterable: Iterable to be grouped.
    :param n: Chunks length.
    :return: Iterable of chunks.
    """
    args = [iter(iterable)] * n
    return (tuple(takewhile(lambda x: x is not None, i)) for i in zip_longest(*args))


class Command(BaseCommand):
    """
    Management commands to work with a Redshift instance
    """
    AUDIENCE = 'audience'
    SEGMENTS = 'segments'
    COMMAND_CHOICES = (AUDIENCE, SEGMENTS)

    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('command', type=str, choices=self.COMMAND_CHOICES)
        parser.add_argument('input_file', type=str)
        parser.add_argument('extra_args', nargs=argparse.REMAINDER)

    def audience(self, input_file, *args, **kwargs):
        """
        Load audience file.

        :param input_file: Path to the input file that will be loaded.
        """
        logger.info("Loading audience file: %s", input_file)

        try:
            with open(input_file, 'r') as finput:
                data = json.load(finput)

                # Clean previous data
                ChannelAudience.objects.all().delete()

                # Get or create the channels
                channel_a, _ = Channel.objects.get_or_create(name='A')
                channel_b, _ = Channel.objects.get_or_create(name='B')

                # Split iterator in chunks to avoid memory collapse
                for chunk in grouper(data.items(), 10000):
                    audiences = []

                    # Create all audience objects from this chunk and save at once in a single query
                    for epoch, audience in chunk:
                        timestamp = datetime.datetime.utcfromtimestamp(int(epoch))

                        # Create audience objects
                        audiences.append(ChannelAudience(timestamp=timestamp, audience=audience[0], channel=channel_a))
                        audiences.append(ChannelAudience(timestamp=timestamp, audience=audience[1], channel=channel_b))

                    # Save batch of audience objects
                    ChannelAudience.objects.bulk_create(audiences)
        except:
            logger.exception("An error occurred while loading audience file")
        else:
            logger.info("Audience file loaded successfully")

    def segments(self, input_file, *args, **kwargs):
        """
        Load segments file.

        :param input_file: Path to the input file that will be loaded.
        """
        logger.info("Loading segments file: %s", input_file)

        try:
            with open(input_file, 'r') as finput:
                # Clean previous data
                Segment.objects.all().delete()
                Topic.objects.all().delete()

                # Create an iterator with applied loads function from json
                loaded_iterator = (json.loads(i) for i in finput.readlines())

                # Retrieve channels and store in memory to fast access
                channels = {c.name: c for c in Channel.objects.all()}

                for chunk in grouper(loaded_iterator, 10000):
                    topics = []
                    for data in chunk:
                        # Create and store segment, it's necessary to store at this moment to link it to their topics
                        segment = Segment.objects.create(
                            start=datetime.datetime.utcfromtimestamp(data['start_ts']),
                            end=datetime.datetime.utcfromtimestamp(data['end_ts']),
                            channel=channels[data['channel']]
                        )

                        ts = [Topic(name=t['name'], count=t['count'], score=t['score'], segment=segment)
                              for t in data['topics']]
                        topics.extend(ts)

                    Topic.objects.bulk_create(topics)
        except:
            logger.exception("An error occurred while loading segments file")
        else:
            logger.info("Segments file loaded successfully")

    def handle(self, *args, **options):
        command = getattr(self, options['command'], None)

        if not command:
            raise CommandError("Invalid command '{}'".format(options['command']))
        else:
            options.pop('command')
            if 'extra_args' in options:
                extra_args = options.pop('extra_args')
            else:
                extra_args = ()
            command(*extra_args, **options)
