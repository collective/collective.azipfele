# -*- coding: utf-8 -*-
from .settings import QUEUE_NAME
from .zipper import Zipit
from .interfaces import IZipQueueAdder
from collective.zamqp.consumer import Consumer
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.interfaces import IProducer
from collective.zamqp.producer import Producer
from plone import api
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implementer
import logging

logger = logging.getLogger('bda.azipfele.taskszamqp')


@implementer(IZipQueueAdder)
class ZAMQPJobAdder(object):

    def __call__(params):
        producer = getUtility(IProducer, name=QUEUE_NAME)
        producer.register()
        payload = dict(params=params)
        producer.publish(payload, correlation_id='AZIPFELE')


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """


class ZipProcessingProducer(Producer):
    """ Produces ZIP processing tasks
    """
    connection_id = 'superuser'
    serializer = 'msgpack'
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
    params = message.body.get('params')
    portal = api.portal.get()
    userid = api.user.get_current().getId()
    zipit = Zipit(portal, userid, params)
    zipit()  # this may take a while
    message.ack()


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """
