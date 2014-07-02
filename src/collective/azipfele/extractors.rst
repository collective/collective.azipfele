prepare
=======

imports

.. code-block:: python

    >>> from collective.azipfele.interfaces import IZipContentExtractor
    >>> from plone import api
    >>> from plone.app.textfield import RichTextValue
    >>> from plone.dexterity.utils import createContentInContainer
    >>> from plone.namedfile.file import NamedBlobFile
    >>> from zope.component import getAdapter
    >>> import os

    >>> testdir = os.path.join(basedir.rstrip('.'), 'test', 'testdata')


Test DxFileExtractor
====================

.. code-block:: python

    >>> portal = api.portal.get()
    >>> f1 = unicode(os.path.join(testdir, 'test.txt'))
    >>> blob_f1 = NamedBlobFile(filename=f1, data=open(f1, 'r').read())
    >>> file1 = createContentInContainer(
    ...    portal, 'File',
    ...    title=u'test.txt',
    ...    file=blob_f1)

    >>> file1.indexObject()

    >>> file_extractor = getAdapter(file1, IZipContentExtractor)
    >>> file_extractor({}, {})
    (u'test.txt', 'test 123 und fertig\n')


Test DxImageExtractor
=====================

.. code-block:: python

    >>> i1 = unicode(os.path.join(testdir, 'image1.jpg'))
    >>> blob_i1 = NamedBlobFile(filename=i1, data=open(i1, 'r').read())
    >>> img1 = createContentInContainer(
    ...    portal, 'Image',
    ...    title=u'img1.jpg',
    ...    image=blob_i1)

    >>> img1.indexObject()

    >>> img_extractor = getAdapter(img1, IZipContentExtractor)
    >>> img_extractor({'path': 'in/zip/folder'}, {})
    (u'in/zip/folder/image1.jpg', '...')


Test DxDocumentExtractor
========================

.. code-block:: python

    >>> doc1 = createContentInContainer(
    ...    portal, 'Document',
    ...    title=u'Documentheading1',
    ...    text = RichTextValue('lorem ipsum dolor sit amet'))

    >>> doc1.indexObject()
    >>> doc_extractor = getAdapter(doc1, IZipContentExtractor)
    >>> doc_extractor({}, {})
    ('documentheading1.html', 'lorem ipsum dolor sit amet')
