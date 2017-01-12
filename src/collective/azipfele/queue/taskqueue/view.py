# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipState
from collective.azipfele.zipper import Zipit
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

import json
import time


class ProcessQueue(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.request.stdin.seek(0)
        jobinfo = json.load(self.request.stdin)
        portal = api.portal.get()
        jobinfo['userid'] = api.user.get_current().getId()  # check here
        state = IZipState(jobinfo['uid'])
        state['task'] = 'processing'
        state['started'] = time.time()
        zipit = Zipit(portal, jobinfo)
        zipit()  # this may take a while
        state = IZipState(jobinfo['uid'])
        state['task'] = 'finished'
        state['ended'] = time.time()
