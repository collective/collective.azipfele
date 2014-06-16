# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOTreeSet
from Products.Five.browser import BrowserView
from collective.zamqp.interfaces import IProducer
from plone import api
from plone.registry.interfaces import IRegistry
from zExceptions import MethodNotAllowed
from zExceptions import Unauthorized
from zlag.mediadb import _
from zlag.mediadb.indexers import MEDIA_FILTER_TYPES
from zlag.mediadb.lightbox import LightBoxStorage
from zlag.mediadb.query import MDBQuery
from zlag.mediadb.zipper import QUEUE_NAME
from zlag.mediadb.zipper import ZIPNGINXKEY
from zlag.mediadb.zipper import make_zip_filename
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory
import json
import logging
import os
import urlparse


class AzipMainView(BrowserView):



class JsonBaseView(BrowserView):
    """Base view for JSON, primary for sematic reasons and to
    make p.a.caching Happy
    """


class ResultSearchView(JsonBaseView):

    def __call__(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        language = portal_state.language()
        mdbquery = MDBQuery(api.portal.get_tool('portal_catalog'), language)
        if self.request.method != 'POST':
            raise MethodNotAllowed('Result search is allowed POST only.')
        self.request.response.setHeader('Content-Type', 'application/json')
        requestdata = json.loads(self.request.get('BODY'))

        target_site = get_target_site(self.request, allowed_only=True)
        if target_site:
            requestdata['target_site'] = target_site

        data = {}
        missing_record_uuids = set(requestdata.get('missing', []))

        if 'query' in requestdata:
            data['order'] = mdbquery.search(requestdata['query'])
            missing_record_uuids.update(data['order'])

        missing_record_uuids = missing_record_uuids.difference(
                requestdata.get('loaded', [])
        )

        data['records'] = mdbquery.load(list(missing_record_uuids))

        return json.dumps(data)




class UserAcceptedTermsView(JsonBaseView):

    def _storage(self):
        portal = api.portal.get()
        annotations = IAnnotations(portal)
        if TERMS_ACCEPTED_USERS in annotations:
            storage = annotations[TERMS_ACCEPTED_USERS]
        else:
            annotations[TERMS_ACCEPTED_USERS] = storage = OOTreeSet()
        return storage

    def _has_accepted(self):
        userid = api.user.get_current().getId()
        return userid in self._storage()

    def _do_accept(self):
        userid = api.user.get_current().getId()
        self._storage().update(userid)

    def _do_reset(self):
        userid = api.user.get_current().getId()
        self._storage().remove(userid)

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        if self.request.form.get('reset', False):
            self._do_reset()
            data = {'state': False}
        elif self.request.form.get('accepted', False):
            self._do_accept()
            data = {'state': True}
        else:
            data = {'state': self._has_accepted()}
        return json.dumps(data)


class LightBoxView(JsonBaseView):

    def __call__(self):
        lbs = LightBoxStorage()
        self.request.response.setHeader('Content-Type', 'application/json')
        if self.request["REQUEST_METHOD"] == "POST":
            requestdata = json.loads(self.request.get('BODY'))
            lbs.set(requestdata)
        return json.dumps({"state": "ok", "data": lbs.get()})


class ZipperView(BrowserView):

    def __call__(self):
        if self.request["REQUEST_METHOD"] != "POST":
            raise Unauthorized("Post only allowed")
        logger.info(self.request.get('BODY'))
        producer = getUtility(IProducer, name=QUEUE_NAME)
        producer.register()
        data = json.loads(self.request.get('BODY'))
        data['portal_url'] = api.portal.get().absolute_url()
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        data['lang'] = portal_state.language()
        data['user'] = api.user.get_current().getId()
        producer.publish(data)


@implementer(IPublishTraverse)
class ZipperDownloadView(BrowserView):

    def __call__(self):
        userid = api.user.get_current().getId()
        target_site = get_target_site(self.request)
        filename = make_zip_filename(target_site, userid, self.uid)
        nginx_path = os.environ[ZIPNGINXKEY] + '/' + filename
        self.request.response.setHeader('X-Accel-Redirect', nginx_path)
        # may need to set contenttype? or is this done by nginx?
        return ""  # empty body here

    def publishTraverse(self, request, name):
        self.uid = name
        return self
