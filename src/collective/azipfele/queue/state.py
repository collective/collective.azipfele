# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipState
from collective.azipfele.settings import ZIPSTATE_MEMCACHEDSERVER
from memcache import Client
from zope.interface import implementer

import os


@implementer(IZipState)
class MemcachedZipState(object):
    """get or set state of an zip job.
    """

    def __init__(self, uid):
        self._uid = uid
        if ZIPSTATE_MEMCACHEDSERVER not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing a memcached '
                'server in order to share state '
                'information.'.format(ZIPSTATE_MEMCACHEDSERVER)
            )
        self._client = Client([os.environ[ZIPSTATE_MEMCACHEDSERVER]])

    def _combined_key(self, key):
        return '{0}-{1}'.format(self._uid, key)

    def __getitem__(self, key):
        """get state of zip job
        """
        return self._client.get(self._combined_key(key))

    def __setitem__(self, key, value):
        """set state of zip job
        """
        return self._client.set(self._combined_key(key), value)
