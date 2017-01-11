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
    return jobinfo['uid']


@implementer(IZipFileCreatedEvent)
class ZipFileCreatedEvent(object):

    def __init__(self, portal, jobinfo):
        self.portal = portal
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

    def _get_log_data(self, context, extractor_name, fileinfo):
        filedata = 'Context Type: {0}\n'.format(context.Type())
        filedata += 'Extractor name: {0}\n'.format(
            str(extractor_name)
        )
        filedata += u'Fileinfo:\n'
        filedata += json.dumps(fileinfo, sort_keys=True, indent=4)
        filedata += u'\n\nSettings:\n'
        filedata += json.dumps(
            self.jobinfo['settings'],
            sort_keys=True,
            indent=4
        )
        return filedata

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
        filepath = os.path.join(
            self.jobinfo['directory'],
            self.jobinfo['filename']
        )
        with zipfile.ZipFile(
            filepath,
            mode='w',
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True
        ) as zf:
            filenames = set()
            count = 0
            for fileinfo in self.jobinfo['fileinfos']:
                count += 1
                if 'uid' not in fileinfo:
                    logger.error('No UID for context given, skipping.')
                    continue
                try:
                    context = uuidToObject(fileinfo['uid'])
                except Exception:
                    filename = u'failed-{0:04d}-uid-{1}-L.txt'.format(
                        count, fileinfo['uid'])
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
                    filename = u'failed-{0:04d}-uid-{1}-E.txt'.format(
                        count, fileinfo['uid'])
                    filedata = "Extractor lookup failed.\n\n"
                    filedata += self._get_log_data(
                        context,
                        extractor_name,
                        fileinfo
                    )
                    logger.warn(filename+'\n'+filedata)
                else:
                    try:
                        start = time.time()
                        filename, filedata = extractor(
                            fileinfo,
                            self.jobinfo
                        )
                        logger.info(u'Retrieved in {0:1.3f}s: {1}'.format(
                            time.time() - start, filename)
                        )
                    except:
                        filename = u'failed-{0:04d}-uid-{1}-R.txt'.format(
                            count, fileinfo['uid']
                        )
                        filedata = "Data retrieval exception.\n\n"
                        filedata += self._get_log_data(
                            context,
                            extractor_name,
                            fileinfo
                        )
                        logger.warn(filename+'\n'+filedata, exc_info=True)
                if filename in filenames:
                    if self.jobinfo['settings'].get(
                        'ignore_duplicates', False
                    ):
                        logger.info('Ignored duplicate.')
                        continue
                    failedfilename = filename
                    filename = u'failed-{0:04d}-uid-{1}-D.txt'.format(
                        count, fileinfo['uid']
                    )
                    filedata = u'Duplicate filename: {0}\n'.format(
                        failedfilename
                    )
                    filedata += self._get_log_data(
                        context,
                        extractor_name,
                        fileinfo
                    )
                    logger.warn(filename+'\n'+filedata)
                else:
                    filenames.update([filename])
                zf.writestr(filename, filedata)
        self.jobinfo['end'] = time.time()
        notify(
            ZipFileCreatedEvent(
                self.portal,
                self.jobinfo
            )
        )
        logger.info('Creation of ZIP File finished\n'+filepath)
