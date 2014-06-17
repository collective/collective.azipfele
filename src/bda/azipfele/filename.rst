prepare
=======

imports::

    >>> from bda.azipfele.browser.interfaces import IZipFileName
    >>> from zope.component import queryMultiAdapter


test filename adapter
"""""""""""""""""""""

::

    >>> uid = "37373737439077432133433443"
    >>> filename_adapter = queryMultiAdapter(({}, {}), IZipFileName)
    >>> filename_adapter(uid)
    '37373737439077432133433443.zip'
