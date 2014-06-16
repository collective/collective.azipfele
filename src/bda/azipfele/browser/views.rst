
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
