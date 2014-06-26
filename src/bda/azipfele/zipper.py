# -*- coding: utf-8 -*-
from bda.azipfele.interfaces import IZipContentExtractor
from bda.azipfele.interfaces import IZipFileCreatedEvent
from bda.azipfele.interfaces import IZipQueueAdder
from bda.azipfele.settings import ZIPDIRKEY
from plone.app.uuid.utils import uuidToObject
from zope.component import getUtility
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implementer
import logging
import os
import uuid
import zipfile

logger = logging.getLogger('bda.azipfele.zipper')


def add_zip_job(params):
    adder = getUtility(IZipQueueAdder)
    adder(params)


@implementer(IZipFileCreatedEvent)
class ZipFileCreatedEvent(object):

    def __init__(self, portal, params, filename, directory, userid):
        self.object = portal
        self.params = params
        self.filename = filename
        self.directory = directory
        self.userid = userid


def zip_filename(uid):
    return "download-{0}.zip".format(uid)


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

    @property
    def zip_filename(self):
        return zip_filename(self.uid)

    def __call__(self):
        """creates a zipfile with data from the initialized params
        """
        logger.info('Creating ZIP File {0}'.format(self.zip_filename))
        with zipfile.ZipFile(
                os.path.join(self.dir, self.zip_filename),
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
                    filename = 'failed-uid-{0}-L.txt'.format(param['uid'])
                    filedata = 'Context lookup failed for UID.'
                    zf.writestr(filename, filedata)
                    continue
                extractor_name = param.get('extractor', None)
                extractor = queryAdapter(
                    context,
                    IZipContentExtractor,
                    name=extractor_name
                )
                if extractor is None:
                    filename = 'failed-uid-{0}-E.txt'.format(param['uid'])
                    filedata = 'Extractor name={0} lookup failed.'.format(
                        str(extractor_name)
                    )
                else:
                    filename, filedata = extractor(param)
                zf.writestr(filename, filedata)
        notify(
            ZipFileCreatedEvent(
                self.portal,
                self.params,
                self.zip_filename,
                self.dir,
                self.userid
            )
        )
