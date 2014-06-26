# -*- coding: utf-8 -*-
from bda.azipfele.interfaces import IZipQueueAdder
from bda.azipfele.settings import QUEUE_NAME
from bda.azipfele.zipper import Zipit
from collective.zamqp.consumer import Consumer
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.interfaces import IProducer
from collective.zamqp.producer import Producer
from plone import api
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
import logging

logger = logging.getLogger('bda.azipfele.taskszamqp')


@implementer(IZipQueueAdder)
class ZAMQPJobAdder(object):

    def __call__(self, params, settings={}):
        producer = getUtility(IProducer, name=QUEUE_NAME)
        producer.register()
        message = dict(params=params, settings=settings)
        producer.publish(message, correlation_id='AZIPFELE')


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
    params = message.body.get('params')
    settings = message.body.get('settings')
    settings['portal'] = api.portal.get()
    settings['userid'] = api.user.get_current().getId()
    zipit = Zipit(params, settings)
    zipit()  # this may take a while
    message.ack()


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """
