# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)

from zope.interface import Interface


class AZIPLayer(Interface):
    """Theme layer"""


class IZipFileName(Interface):
    """returns the zipfilename on call"""

    def __call__(uid):
        """create zipfilename"""


class IZipContentExtractor(Interface):
    """extracts the desired content on call"""

    def __call__(payload):
        """create zipfilename"""
