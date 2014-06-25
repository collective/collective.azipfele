# -*- coding: utf-8 -*-
from .interfaces import IZipContentExtractor
from .interfaces import IZipFileCreatedEvent
from .settings import ZIPDIRKEY
from plone.app.uuid.utils import uuidToObject
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implementer
import logging
import os
import uuid
import zipfile

logger = logging.getLogger('bda.azipfele.zipper')


@implementer(IZipFileCreatedEvent)
class ZipFileCreatedEvent(object):

    def __init__(self, params, filename, directory, userid):
        self.params = params
        self.filename = filename
        self.directory = directory
        self.userid = userid


def zip_filename(uid):
    return "download-{2}.zip".format(uid)


class Zipit(object):
    """Creates a Zip File
    """

    def __init__(self, portal, userid, params):
        """Initialize the creation job.

        portal
            the Plone portal object

        userid
            user who added the job

        params
            a list of dicts describing the content to be added.
            each dicts has at least a uid of some contebnt object
        """
        self.portal = portal
        self.userid = userid
        self.params = params
        if ZIPDIRKEY not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing to target '
                'directory for zip-files, shared with nginx in order to '
                'work with x-sendfile.'.format(ZIPDIRKEY)
            )
        self.dir = os.environ[ZIPDIRKEY]

        # generate a uuid for the zipping operation
        self.uid = str(uuid.uuid4())

    def zip_filename(self):
        return zip_filename(self.uid)

    def __call__(self):
        """creates a zipfile with data from the initialized params
        """
        self.zf_name = zip_filename(self.uid)
        logger.info('Creating ZIP File {0}'.format(self.zf_name))
        with zipfile.ZipFile(
                os.path.join(self.dir, self.zf_name),
                mode='w',
                compression=zipfile.ZIP_DEFLATED,
                allowZip64=True
        ) as zf:
            for param in self.params:
                if 'uid' not in param:
                    logger.error('No UID given, skipping.')
                    continue
                try:
                    context = uuidToObject(param['uid'])
                except Exception:
                    filename = 'failed-uid-{0}.txt'.format(param['uid'])
                    filedata = 'Context lookup failed for UID.'
                    zf.writestr(filename, filedata)
                    continue
                extractor_name = param.get('extractor', None)
                extractor = queryAdapter(
                    context,
                    IZipContentExtractor,
                    extractor_name
                )
                if extractor is None:
                    filename = 'failed-uid-{0}.txt'.format(param['uid'])
                    filedata = 'Extractor name={0} lookup failed.'.format(
                        str(extractor_name)
                    )
                    zf.writestr(filename, filedata)
                else:
                    filename, filedata = extractor(param)
                zf.writestr(filename, filedata)
        notify(
            ZipFileCreatedEvent(
                self.params,
                zipfile,
                self.dir,
                self.userid
            )
        )
