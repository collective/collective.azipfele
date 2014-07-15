# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipQueueAdder
from collective.azipfele.interfaces import IZipState
from collective.azipfele.settings import QUEUE_NAME
from collective.azipfele.settings import ZIPSTATE_MEMCACHEDSERVER
from collective.azipfele.zipper import Zipit
from collective.zamqp.consumer import Consumer
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.interfaces import IProducer
from collective.zamqp.producer import Producer
from memcache import Client
from plone import api
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implementer
import logging
import os
import time

logger = logging.getLogger('collective.azipfele.taskszamqp')


@implementer(IZipQueueAdder)
class ZAMQPJobAdder(object):

    def __call__(self, jobinfo):
        producer = getUtility(IProducer, name=QUEUE_NAME)
        producer.register()
        producer.publish(jobinfo, correlation_id='AZIPFELE')
        state = IZipState(jobinfo['uid'])
        state['task'] = 'pending'
        state['queued'] = time.time()


@implementer(IZipState)
class MemcachedZipState(object):
    """get or set state of an zip job.
    """

    def __init__(self, uid):
        self._uid = uid
        if ZIPSTATE_MEMCACHEDSERVER not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing a memcached '
                'server in order to share state '
                'information.'.format(ZIPSTATE_MEMCACHEDSERVER)
            )
        self._client = Client([os.environ[ZIPSTATE_MEMCACHEDSERVER]])

    def _combined_key(self, key):
        return '{0}-{1}'.format(self._uid, key)

    def __getitem__(self, key):
        """get state of zip job
        """
        return self._client.get(self._combined_key(key))

    def __setitem__(self, key, value):
        """set state of zip job
        """
        return self._client.set(self._combined_key(key), value)


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """


class ZipProcessingProducer(Producer):
    """ Produces ZIP processing tasks
    """
    connection_id = 'superuser'
    #serializer = 'msgpack'
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME

    durable = True
    auto_delete = True


class ZipProcessingConsumer(Consumer):
    """ Consumes Zip processing tasks
    """
    connection_id = 'superuser'
    marker = IZipProcessingMessage
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME
    durable = True
    auto_delete = True


@adapter(IZipProcessingMessage, IMessageArrivedEvent)
def process_message(message, event):
    """ Handle messages received through consumer.
    """
    cid = message.header_frame.correlation_id
    logger.info("process message {0}".format(cid))
    portal = api.portal.get()
    jobinfo = message.body
    jobinfo['userid'] = api.user.get_current().getId()  # check here
    state = IZipState(jobinfo['uid'])
    state['task'] = 'processing'
    state['started'] = time.time()
    zipit = Zipit(portal, jobinfo)
    zipit()  # this may take a while
    message.ack()
    state = IZipState(jobinfo['uid'])
    state['task'] = 'finished'
    state['ended'] = time.time()


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """
