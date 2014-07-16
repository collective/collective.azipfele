# -*- coding: utf-8 -*-
from zope.interface import Attribute
from zope.interface import Interface


class AZIPLayer(Interface):
    """Theme layer"""


class ITaskHandler(Interface):

    def add_task(jobinfo):
        """add taks to queue
        """


class IZipQueueAdder(Interface):
    """add job to queue on __call_
    """


class IZipState(Interface):
    """get or set state of an zip jon.

    Intended to be initialized with an uid
    """

    def __getitem__(key):
        """get state of zip job
        """

    def __setitem(key, value):
        """set state of zip job
        """


class IZipContentExtractor(Interface):
    """extracts content according to given parameters
    """

    def __call__(fileinfo, settings):
        """extracts one zip content file

        returns tuple with filename and content
        """

    def in_zip_file_path(fileinfo, filename):
        """makes a path to be used use inside of zip
        """


class IZipFileCreatedEvent(Interface):
    """Event to be fired when a zip file was created
    """

    portal = Attribute("Plone portal object")
    jobinfo = Attribute("Dict with job information")
