# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.component.interfaces import IObjectEvent


class AZIPLayer(Interface):
    """Theme layer"""


class ITaskHandler(Interface):

    def add_task(payload):
        """add taks to queue
        """


class IZipFileName(Interface):
    """zipfilename generator
    """

    def __call__(params):
        """create zipfilename

        a zip filename may has a relative path by using slashes as separators

        returns string with filename/ filepath
        """


class IZipContentExtractor(Interface):
    """extracts content according to given parameters
    """

    def __call__(params):
        """extracts one zip content file

        returns tuple with filename and content
        """


class IZipFileCreatedEvent(IObjectEvent):
    """Event to be fired when a zip file was created
    """
