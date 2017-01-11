# -*- coding: utf-8 -*-
from collective.azipfele import _
from collective.azipfele.zipper import add_zip_job
from plone import api
from plone.folder.interfaces import IFolder
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView

import logging


logger = logging.getLogger('collective.azipfele.browser.views')


class ZipperBaseAdderView(BrowserView):
    """Base Class for Adding Jobs to the zip queue
    """

    def __call__(self):
        self.uid = add_zip_job(self.params, self.settings)
        return self.after_add_action()

    @property
    def params(self):
        raise NotImplemented('Base class has no implementation')

    @property
    def settings(self):
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

    @property
    def settings(self):
        return {}

    def after_add_action(self):
        api.portal.show_message(
            message=_(
                '',
                default=u'Folder queued for ZIP download. '
                        u'Job-ID {0}'.format(self.uid)
            ),
            request=self.request
        )
        self.request.response.setCookie('azipjobid', self.uid, path='/')
        self.request.response.redirect(self.context.absolute_url())
        return ""
