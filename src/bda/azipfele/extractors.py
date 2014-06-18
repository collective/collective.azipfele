# -*- coding: utf-8 -*-

from .browser.interfaces import IZipContentExtractor
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IImage
from zope.component import adapter
from zope.interface import implementer
import os


@implementer(IZipContentExtractor)
class BaseExtractor(object):
    def __init__(self, context):
        self.context = context

    def __call__(self, payload):
        raise NotImplementedError()


class BaseDxBlobExtractor(BaseExtractor):
    fieldname = None

    def __call__(self, payload):
        fieldvalue = getattr(self.context, self.fieldname)
        filedata = fieldvalue.data  # blobfile as string
        filename = os.path.basename(fieldvalue.filename)

        return (filename, filedata)


@adapter(IFile)
class DxFileExtractor(BaseDxBlobExtractor):
    fieldname = "file"


@adapter(IImage)
class DxImageExtractor(BaseDxBlobExtractor):
    fieldname = "file"


@adapter(IDocument)
class DxDocumentExtractor(BaseExtractor):
    def __call__(self, payload):
        filedata = self.context.text.output
        filename = self.context.id + '.html'

        return (filename, filedata)
