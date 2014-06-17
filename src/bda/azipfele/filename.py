from .browser.interfaces import IZipFileName
from zope.interface import implementer


@implementer(IZipFileName)
class UidZipFileName():
    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self, uid):
        return "{0}.zip".format(uid)
