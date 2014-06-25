prepare
=======

imports::

    >>> from plone import api
    >>> from plone.app.testing import login
    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import TEST_USER_NAME
    >>> from plone.dexterity.utils import createContentInContainer
    >>> from plone.namedfile.file import NamedBlobFile
    >>> from plone.uuid.interfaces import IUUID
    >>> from StringIO import StringIO
    >>> import os
    >>> import tempfile


getportal, login and create folder
""""""""""""""""""""""""""""""""""

::

    >>> portal = api.portal.get()
    >>> login(portal, TEST_USER_NAME)
    >>> setRoles(portal, TEST_USER_ID, ['Manager'])

    >>> user = api.user.get_current()
    >>> usermail = user.getProperty('email')
    >>> userid = user.getId()
    >>> testurl = 'https://lcp.zumtobel.com'

    >>> folder = createContentInContainer(
    ...    portal, 'Folder',
    ...    title=u'mdb',
    ...    description=u'Application pictures, product pictures and videos for \
    ...    downloading will help you when advising your customers.')


create normal files with uid and blob
"""""""""""""""""""""""""""""""""""""

::

    >>> testdir = os.path.join(basedir.rstrip('.'), 'csvimport', 'testdata')

    >>> f1 = os.path.join(testdir, 'image1.jpg')
    >>> f2 = os.path.join(testdir, 'image2.jpg')
    >>> f1 = unicode(f1)
    >>> f2 = unicode(f2)

    >>> b1 = NamedBlobFile(filename=f1, data=open(f1, 'r').read())
    >>> b2 = NamedBlobFile(filename=f2, data=open(f2, 'r').read())

    >>> img1 = createContentInContainer(
    ...    folder, 'File',
    ...    title=u'img1',
    ...    file=b1)

    >>> img2 = createContentInContainer(
    ...    folder, 'File',
    ...    title=u'img2',
    ...    file=b2)

    >>> img1.indexObject()
    >>> img2.indexObject()

    >>> uid1 = IUUID(img1)
    >>> uid2 = IUUID(img2)

    >>> uids = [uid1, uid2]


create zipper
=============

set testenviron
"""""""""""""""

::

    >>> os.environ[ZIPDIRKEY] = tempfile.mkdtemp()
    >>> zipit = Zipit(portal, usermail, testurl, userid, uids)


create
""""""

::

    >>> zipit.create()
    >>> zipit.zf_name
    'zumtobel-lcp-test_user_1_-...-...-...-....zip'


check zipfile
"""""""""""""

::
    >>> import zipfile
    >>> zf = zipfile.ZipFile(
    ...     os.path.join(os.environ[ZIPDIRKEY], zipit.zf_name), 'r')
    >>> zf.printdir()
    File Name                                             Modified             Size
    image1.jpg                                     ... ...                      519
    image2.jpg                                     ... ...                      519

cleanup
"""""""

remove temp directory::

   >>> import shutil
   >>> shutil.rmtree(os.environ[ZIPDIRKEY])
