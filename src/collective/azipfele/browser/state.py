# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipState
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class ZipperStateView(BrowserView):

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.uid = None

    def __call__(self):
        if self.uid is None:
            self.uid = self.request.cookies.get('azipjobid', None)
        self.request.response.setHeader('Content-Type', 'application/json')
        state = IZipState(self.uid)
        result = {
            'task': state['task'],
            'queued': state['queued'],
            'started': state['started'],
            'ended': state['ended'],
        }
        return json.dumps(result)

    def publishTraverse(self, request, name):
        self.uid = name
        return self
