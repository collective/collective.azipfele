# -*- coding: utf-8 -*-
from bda.azipfele.interfaces import IZipContentExtractor
from zope.interface import implementer
import os


@implementer(IZipContentExtractor)
class BaseExtractor(object):
    """Abstract Base adapter for a ZipContentExtractor
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, param, settings):
        raise NotImplementedError()


class BaseDxBlobExtractor(BaseExtractor):
    """Extractor for one blobfile field of Dexterity content
    """
    fieldname = None

    def __call__(self, param, settings):
        """extracts the content of a blob
        """
        fieldvalue = getattr(self.context, self.fieldname)
        filedata = fieldvalue.data  # blobfile as string
        filename = os.path.basename(fieldvalue.filename)
        return filename, filedata


class DxFileExtractor(BaseDxBlobExtractor):
    """Extractor made for plone.app.contenttypes File type

    Suitable also for other Dexterity Types with a BlobField named ``file``
    """

    fieldname = "file"


class DxImageExtractor(BaseDxBlobExtractor):
    """Extractor made for plone.app.contenttypes File type

    Suitable also for other Dexterity Types with a BlobField named ``image``,
    such as the LeadImage behavior.
    """
    fieldname = "image"


class DxDocumentExtractor(BaseExtractor):
    """Extractor made for plone.app.contenttypes Document type

    Suitable also for other Dexterity Types with a RichField named ``text``.
    """

    def __call__(self, param, settings):
        filedata = self.context.text.output
        filename = self.context.id + '.html'
        return (filename, filedata)
