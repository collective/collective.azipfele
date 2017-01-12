# -*- coding: utf-8 -*-
from collective.azipfele.interfaces import IZipQueueAdder
from collective.azipfele.settings import QUEUE_NAME
from collective.taskqueue import taskqueue
from zope.interface import implementer
from collective.azipfele.interfaces import IZipState
from zope.component.hooks import getSite

import json
import time

VIEW_NAME = 'azipfele_taskqueue_processor'


@implementer(IZipQueueAdder)
class TaskQueueJobAdder(object):

    def __call__(self, jobinfo):
        """Queues job for zipping
        """
        jobid = taskqueue.add(
            '/'.join(getSite().getPhysicalPath() + (VIEW_NAME, )),
            method='post',
            queue=QUEUE_NAME,
            payload=json.dumps(jobinfo),
        )
        state = IZipState(jobinfo['uid'])
        state['task'] = 'pending'
        state['taskqueue_jobid'] = jobid
        state['queued'] = time.time()
        return jobid
