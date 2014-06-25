# -*- coding: utf-8 -*-
from .interfaces import IZipContentExtractor
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IImage
from zope.component import adapter
from zope.interface import implementer
import os


@implementer(IZipContentExtractor)
class BaseExtractor(object):
    """Abstract Base adapter for a ZipContentExtractor
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, payload):
        raise NotImplementedError()


class BaseDxBlobExtractor(BaseExtractor):
    """Extractor for one blobfile field of Dexterity content
    """
    fieldname = None

    def __call__(self, payload):
        """extracts the content of a blob
        """
        fieldvalue = getattr(self.context, self.fieldname)
        import pdb; pdb.set_trace()
        filedata = fieldvalue.data  # blobfile as string
        filename = os.path.basename(fieldvalue.filename)

        return filename, filedata


@adapter(IFile)
class DxFileExtractor(BaseDxBlobExtractor):
    """Extractor made for plone.app.contenttypes File type

    Suitable also for other Dexterity Types with a BlobField named ``file``
    """

    fieldname = "file"


@adapter(IImage)
class DxImageExtractor(BaseDxBlobExtractor):
    """Extractor made for plone.app.contenttypes File type

    Suitable also for other Dexterity Types with a BlobField named ``image``,
    such as the LeadImage behavior.
    """
    fieldname = "image"


@adapter(IDocument)
class DxDocumentExtractor(BaseExtractor):
    """Extractor made for plone.app.contenttypes Document type

    Suitable also for other Dexterity Types with a RichField named ``text``.
    """

    def __call__(self, payload):
        filedata = self.context.text.output
        filename = self.context.id + '.html'
        return (filename, filedata)
