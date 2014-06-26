prepare
=======

imports::

    >>> from plone import api
    >>> from plone.dexterity.utils import createContentInContainer
    >>> from plone.app.textfield import RichTextValue
    >>> from plone.namedfile.file import NamedBlobFile
    >>> from plone.uuid.interfaces import IUUID
    >>> from StringIO import StringIO
    >>> import os
    >>> import tempfile


getportal, login and create folder and test content
"""""""""""""""""""""""""""""""""""""""""""""""""""

::

    >>> portal = api.portal.get()
    >>> folder = portal.folder
    >>> user = api.user.get_current()
    >>> testdir = os.path.join(basedir.rstrip('.'), 'test', 'testdata')

    >>> i1 = unicode(os.path.join(testdir, 'image1.jpg'))
    >>> blob_i1 = NamedBlobFile(filename=i1, data=open(i1, 'r').read())
    >>> img1 = createContentInContainer(
    ...    folder, 'Image',
    ...    title=u'img1.jpg',
    ...    image=blob_i1)
    >>> img1.indexObject()

    >>> f1 = unicode(os.path.join(testdir, 'test.txt'))
    >>> blob_f1 = NamedBlobFile(filename=f1, data=open(f1, 'r').read())
    >>> file1 = createContentInContainer(
    ...    folder, 'File',
    ...    title=u'test.txt',
    ...    file=blob_f1)

    >>> file1.indexObject()

    >>> doc1 = createContentInContainer(
    ...    folder, 'Document',
    ...    title=u'Documentheading1',
    ...    text = RichTextValue('lorem ipsum dolor sit amet'))
    >>> doc1.indexObject()

    >>> from bda.azipfele.interfaces import IZipContentExtractor
    >>> extr = IZipContentExtractor(img1)
    >>> extr = IZipContentExtractor(file1)
    >>> extr = IZipContentExtractor(doc1)


create zipper
=============

set testenviron
"""""""""""""""

::

    >>> from bda.azipfele import settings
    >>> from bda.azipfele.zipper import Zipit
    >>> os.environ[settings.ZIPDIRKEY] = tempfile.mkdtemp()
    >>> params = [
    ...     {'uid': IUUID(img1)},
    ...     {'uid': IUUID(file1)},
    ...     {'uid': IUUID(doc1)},
    ... ]
    >>> zipit = Zipit(portal, user.getId(), params)


create
""""""

::

    >>> zipit()
    >>> zipit.zip_filename
    'download-...-...-...-....zip'


check zipfile
"""""""""""""

::
    >>> import zipfile
    >>> zf = zipfile.ZipFile(
    ...     os.path.join(os.environ[settings.ZIPDIRKEY], zipit.zip_filename),
    ...     'r'
    ... )
    >>> zf.printdir()
    File Name                                      Modified             Size
    image1.jpg                                     ... ...               519
    test.txt                                       ... ...                20
    documentheading1.html                          ... ...                26


cleanup
"""""""

remove temp directory::

   >>> import shutil
   >>> shutil.rmtree(os.environ[settings.ZIPDIRKEY])
