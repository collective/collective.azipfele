prepare
=======

imports

::

    >>> from bda.azipfele.browser.interfaces import AZIPLayer
    >>> from plone import api
    >>> from plone.app.testing import login
    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> from Products.CMFCore.utils import getToolByName
    >>> from zope.interface import alsoProvides

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
