# -*- coding: utf-8 -*-
from bda.azipfele.interfaces import IZipContentExtractor
from bda.azipfele.interfaces import IZipFileCreatedEvent
from bda.azipfele.interfaces import IZipQueueAdder
from bda.azipfele.settings import ZIPDIRKEY
from plone.app.uuid.utils import uuidToObject
from zope.event import notify
from zope.interface import implementer
from zope.component import getSiteManager
import logging
import os
import uuid
import zipfile

logger = logging.getLogger('bda.azipfele.zipper')


def add_zip_job(params):
    adder = getSiteManager().getUtility(IZipQueueAdder)
    adder(params)


@implementer(IZipFileCreatedEvent)
class ZipFileCreatedEvent(object):

    def __init__(self, params, settings, filename, directory):
        self.object = settings['portal']
        self.params = params
        self.settings = settings
        self.filename = filename
        self.directory = directory


def zip_filename(uid):
    return "download-{0}.zip".format(uid)


class Zipit(object):
    """Creates a Zip File
    """

    def __init__(self, params, settings):
        """Initialize the creation job.

        portal
            the Plone portal object

        params
            a list of dicts describing the content to be added.
            each dicts has at least a uid of some contebnt object

        settings
            dict with arbitary settings. contains at least portal and userid
        """
        self.params = params
        self.settings = settings
        self.portal = settings['portal']
        if ZIPDIRKEY not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing to target '
                'directory for zip-files, shared with nginx in order to '
                'work with x-sendfile.'.format(ZIPDIRKEY)
            )
        self.dir = os.environ[ZIPDIRKEY]

        # generate an own uuid for the zipping operation
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
                    filedata = 'Context lookup failed for UID.\n'
                    zf.writestr(filename, filedata)
                    continue
                extractor_name = param.get('extractor', None)
                # extractor = getGlobalSiteManager().queryAdapter(
                #     context,
                #     IZipContentExtractor,
                #     name=extractor_name
                # )
                if extractor_name:
                    raise NotImplemented("TODO")

                else:
                    try:
                        extractor = IZipContentExtractor(context)
                    except:
                        extractor = None
                if extractor is None:
                    filename = 'failed-uid-{0}-E.txt'.format(param['uid'])
                    filedata = 'Context Type={0}.\n'.format(context.Type())
                    filedata += 'Extractor name={0} lookup failed.'.format(
                        str(extractor_name)
                    )
                else:
                    filename, filedata = extractor(param, self.settings)
                zf.writestr(filename, filedata)

        notify(
            ZipFileCreatedEvent(
                self.params,
                self.settings,
                self.zip_filename,
                self.dir
            )
        )
