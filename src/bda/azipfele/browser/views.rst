
prepare
=======

imports

::

    >>> from plone import api
    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import login
    >>> from Products.CMFCore.utils import getToolByName
    >>> from zope.interface import alsoProvides
    >>> from bda.azipfele.browser.interfaces import AZIPLayer
    >>> from bda.azipfele.lightbox import LightBoxStorage
    >>> from bda.azipfele.browser.views import LightBoxView


preparation

::

    >>> app = layer['app']
    >>> request = layer['request']
    >>> portal = layer['portal']
    >>> acl_users = getToolByName(portal, 'acl_users')
    >>> acl_users.userFolderAddUser('user1', 'user1', ['Manager'], [])
    >>> login(portal, 'user1')


Test
====

Basic
-----

create folder, set our layer on it and check if the view works

::

    >>> portal.invokeFactory('Folder', 'f1', title=u"Lightbox Folder")
    'f1'

    >>> f1 = portal['f1']

    >>> alsoProvides(request, MDBLayer)

    >>> f1.unrestrictedTraverse("@@" + "mdblightbox")
    <Products.Five.metaclass.LightBoxView object at 0x...>


check get and post
------------------

when there is no lbs_data, theres nothing to display
....................................................

::
    >>> view = f1.unrestrictedTraverse("@@" + "mdblightbox")
    >>> view()
    '{"state": "ok", "data": {}}'


set some testdata
.................

::

    >>> request["REQUEST_METHOD"] = 'POST'
    >>> request['BODY'] = '{"a" : "720", "b" : "1080", "c" : "720", "d" : "1080", "e" : "720"}'



when data is set successfully, return ok
........................................

::

    >>> view()
    '{"state": "ok", "data": {"a": "720", "c": "720", "b": "1080", "e": "720", "d": "1080"}}'


change requestmode and lookup the data, which was set before
............................................................

::

    >>> request["REQUEST_METHOD"] = 'GET'
    >>> pprint(view())
    '{"state": "ok", "data": {"a": "720", "c": "720", "b": "1080", "e": "720", "d": "1080"}}'


change request and check if get is empty, if there was no lbs_data in the request
.................................................................................

::

    >>> request["REQUEST_METHOD"] = 'POST'
    >>> request['BODY'] = '{}'
    >>> view()
    '{"state": "ok", "data": {}}'
