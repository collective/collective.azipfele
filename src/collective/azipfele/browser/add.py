# -*- coding: utf-8 -*-
from collective.azipfele.zipper import add_zip_job
from Products.Five.browser import BrowserView
from zExceptions import Unauthorized
from plone.folder.interfaces import IFolder
from plone.uuid.interfaces import IUUID
from plone import api
from collective.azipfele import _
import logging

logger = logging.getLogger('collective.azipfele.browser.views')


class ZipperBaseAdderView(BrowserView):
    """Base Class for Adding Jobs to the zip queue
    """

    def __call__(self):
        add_zip_job(self.params)
        return self.after_add_action()

    @property
    def params(self):
        raise NotImplemented('Base class has no implementation')

    def after_add_action(self):
        raise NotImplemented('Base class has no implementation')


class RecursiveFolderAdderView(ZipperBaseAdderView):

    def _add_folder(self, uids, folder):
        for content in folder.values():
            if IFolder.providedBy(content):
                self._add_folder(uids, content)
            else:
                uids.append({'uid': IUUID(content)})
        return uids

    @property
    def params(self):
        uids = []
        self._add_folder(uids, self.context)
        return uids

    def after_add_action(self):
        api.portal.show_message(
            message=_('', default=u"Folder queued for ZIP download"),
            request=self.request
        )
        self.request.response.redirect(self.context.absolute_url())
        return ""
