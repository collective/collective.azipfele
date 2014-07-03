# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipContentExtractor
from collective.azipfele.interfaces import IZipFileCreatedEvent
from collective.azipfele.interfaces import IZipQueueAdder
from collective.azipfele.settings import ZIPDIRKEY
from plone.app.uuid.utils import uuidToObject
from zope.component import getSiteManager
from zope.component import queryAdapter
from zope.event import notify
from zope.interface import implementer
import json
import logging
import os
import time
import uuid
import zipfile

logger = logging.getLogger('collective.azipfele.zipper')


def add_zip_job(settings, fileinfos):
    adder = getSiteManager().getUtility(IZipQueueAdder)
    jobinfo = dict()
    jobinfo['uid'] = str(uuid.uuid4())
    jobinfo['settings'] = settings
    jobinfo['fileinfos'] = fileinfos
    adder(jobinfo)


@implementer(IZipFileCreatedEvent)
class ZipFileCreatedEvent(object):

    def __init__(self, portal, jobinfo):
        self.object = portal
        self.jobinfo = jobinfo


def zip_filename(jobinfo):
    return "download-{0}.zip".format(jobinfo['uid'])


class Zipit(object):
    """Creates a Zip File
    """

    def __init__(self, portal, jobinfo):
        """Initialize the creation job.

        portal
            the Plone portal object

        jobinfo
            dict with uid, settings and fileinfos
        """
        self.portal = portal
        self.jobinfo = jobinfo
        if ZIPDIRKEY not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing to target '
                'directory for zip-files, shared with nginx in order to '
                'work with x-sendfile.'.format(ZIPDIRKEY)
            )
        self.jobinfo['directory'] = os.environ[ZIPDIRKEY]

    @property
    def zip_filename(self):
        return zip_filename(self.jobinfo)

    def __call__(self):
        """creates a zipfile with data from the initialized params
        """
        self.jobinfo['start'] = time.time()
        self.jobinfo['filename'] = self.zip_filename
        logger.info('Creating ZIP File {0}'.format(
            self.jobinfo['filename']
        ))
        with zipfile.ZipFile(
                os.path.join(
                    self.jobinfo['directory'],
                    self.jobinfo['filename']
                ),
                mode='w',
                compression=zipfile.ZIP_DEFLATED,
                allowZip64=True
        ) as zf:
            for fileinfo in self.jobinfo['fileinfos']:
                if 'uid' not in fileinfo:
                    logger.error('No UID for context given, skipping.')
                    continue
                try:
                    context = uuidToObject(fileinfo['uid'])
                except Exception:
                    filename = 'failed-uid-{0}-L.txt'.format(fileinfo['uid'])
                    filedata = 'Context lookup failed for UID.\n'
                    zf.writestr(filename, filedata)
                    continue
                extractor_name = fileinfo.get('extractor', None)
                if extractor_name:
                    extractor = queryAdapter(
                        context,
                        IZipContentExtractor,
                        name=extractor_name
                    )
                else:
                    try:
                        extractor = IZipContentExtractor(context)
                    except:
                        extractor = None
                if extractor is None:
                    filename = 'failed-uid-{0}-E.txt'.format(fileinfo['uid'])
                    filedata = 'Context Type={0}.\n'.format(context.Type())
                    filedata += 'Extractor name={0} lookup failed.'.format(
                        str(extractor_name)
                    )
                else:
                    try:
                        filename, filedata = extractor(
                            fileinfo,
                            self.jobinfo
                        )
                    except:
                        filename = 'failed-uid-{0}-R.txt'.format(
                            fileinfo['uid']
                        )
                        filedata = u'Context Type={0}.\n'.format(
                            context.Type()
                        )
                        filedata += u'Extractor name={0} failed.\n\n'.format(
                            str(extractor_name)
                        )
                        filedata += u'\n\nFileinfo:\n'
                        filedata += json.dumps(fileinfo)
                        filedata += u'\n\nSettings:\n'
                        filedata += json.dumps(self.jobinfo['settings'])

                zf.writestr(filename, filedata)
        self.jobinfo['end'] = time.time()
        notify(
            ZipFileCreatedEvent(
                self.portal,
                self.jobinfo
            )
        )
