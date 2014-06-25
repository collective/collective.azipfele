# -*- coding: utf-8 -*-
from bda.azipfele.settings import QUEUE_NAME
from bda.azipfele.settings import ZIPNGINXKEY
from bda.azipfele.zipper import zip_filename
from collective.zamqp.interfaces import IProducer
from plone import api
from Products.Five.browser import BrowserView
from zExceptions import Unauthorized
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import json
import logging
import os

logger = logging.getLogger('bda.azipfele.browser.views')


class AzipMainView(BrowserView):
    def __call__(self):
        return ""


class ZipperView(BrowserView):
    def __call__(self):
        if self.request["REQUEST_METHOD"] != "POST":
            raise Unauthorized("Post only allowed")
        logger.info(self.request.get('BODY'))
        producer = getUtility(IProducer, name=QUEUE_NAME)
        producer.register()
        data = json.loads(self.request.get('BODY'))
        data['portal_url'] = api.portal.get().absolute_url()
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        data['lang'] = portal_state.language()
        data['user'] = api.user.get_current().getId()
        producer.publish(data)


@implementer(IPublishTraverse)
class ZipperDownloadView(BrowserView):
    def __call__(self):
        userid = api.user.get_current().getId()
        filename = zip_filename(self.uid)
        nginx_path = os.environ[ZIPNGINXKEY] + '/' + filename
        self.request.response.setHeader('X-Accel-Redirect', nginx_path)
        # may need to set contenttype? or is this done by nginx?
        return ""  # empty body here

    def publishTraverse(self, request, name):
        self.uid = name
        return self