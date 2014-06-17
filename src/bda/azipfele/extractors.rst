prepare
=======

imports::

    >>> from bda.azipfele.browser.interfaces import IZipContentExtractor
    >>> from plone import api
    >>> from plone.app.testing import login
    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import TEST_USER_NAME
    >>> from plone.app.textfield import RichTextValue
    >>> from plone.dexterity.utils import createContentInContainer
    >>> from plone.namedfile.file import NamedBlobFile
    >>> from zope.component import getAdapter
    >>> import os


getportal, and login
""""""""""""""""""""

::

    >>> portal = api.portal.get()
    >>> login(portal, TEST_USER_NAME)
    >>> setRoles(portal, TEST_USER_ID, ['Manager'])


create file,img and document
""""""""""""""""""""""""""""

::

    >>> testdir = os.path.join(basedir.rstrip('.'), 'test', 'testdata')
    >>> f1 = os.path.join(testdir, 'test.txt')
    >>> f1 = unicode(f1)
    >>> blob_f1 = NamedBlobFile(filename=f1, data=open(f1, 'r').read())
    >>> file1 = createContentInContainer(
    ...    portal, 'File',
    ...    title=u'test.txt',
    ...    file=blob_f1)

    >>> file1.indexObject()


    >>> i1 = os.path.join(testdir, 'image1.jpg')
    >>> i1 = unicode(i1)
    >>> blob_i1 = NamedBlobFile(filename=i1, data=open(i1, 'r').read())
    >>> img1 = createContentInContainer(
    ...    portal, 'Image',
    ...    title=u'img1.jpg',
    ...    file=blob_i1)

    >>> img1.indexObject()


    >>> doc1 = createContentInContainer(
    ...    portal, 'Document',
    ...    title=u'Documentheading1',
    ...    text = RichTextValue('lorem ipsum dolor sit amet'))

    >>> doc1.indexObject()


Test DxFileExtractor
====================

::

    >>> file_extractor = getAdapter(file1, IZipContentExtractor)
    >>> file_extractor(file1)
    (u'test.txt', 'test 123 und fertig\n')


Test DxImageExtractor
=====================

::

    >>> img_extractor = getAdapter(img1, IZipContentExtractor)
    >>> img_extractor(img1)
    (u'image1.jpg', '...')


Test DxDocumentExtractor
========================

::
    #>>> interact(locals())
    >>> doc_extractor = getAdapter(doc1, IZipContentExtractor)
    >>> doc_extractor(doc1)
    (u'Documentheading1', 'lorem ipsum dolor sit amet')
