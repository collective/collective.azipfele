# -*- coding: utf-8 -*-
from collective.azipfele.settings import ZIPNGINXKEY
from collective.azipfele.zipper import zip_filename
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import os


@implementer(IPublishTraverse)
class ZipperDownloadView(BrowserView):

    def __call__(self):
        filename = zip_filename({'uid': self.uid})
        nginx_path = os.path.join(os.environ[ZIPNGINXKEY], filename)
        self.request.response.setHeader('X-Accel-Redirect', nginx_path)
        self.request.response.setHeader('Content-Type', 'application/zip')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename={0}'.format(filename)
        )
        return ""  # empty body here by intend

    def publishTraverse(self, request, name):
        self.uid = name
        return self
