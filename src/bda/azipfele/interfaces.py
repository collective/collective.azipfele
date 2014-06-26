# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface


class AZIPLayer(Interface):
    """Theme layer"""


class ITaskHandler(Interface):

    def add_task(payload):
        """add taks to queue
        """


class IZipQueueAdder(Interface):
    """add job to queue on __call_
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
