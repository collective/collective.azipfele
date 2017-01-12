Asynchronous ZIP File Creation from Plone Content or Webservices
================================================================

.. contents::


This is a basic module aiming to create ZIP files asynchronous.
Even if it has some basic built in data-extractors, it is not meant as a out-of-the-box package,
but for integrators and addon-product authors.

Creating ZIP files in a request-response cycle may take a lot of time.
With this package a zip job info is queued into a task queue.

It supports ``collective.taskqueue`` (optional backed by Redis)
and also ``collective.zamqp`` (AMQP based solution using a AMQP-Server such as  RabbitMQ).

The ZIP file is created in a worker instance.
After the file was created an event is fired.
With it i.e. an e-mail notification can be send out.

The state of the creation (pending, processing, finished) and the timestamps (queued, started, finished) are shared between worker and instance.

The worker instance gets a jobinfo (dict) with global key ``settings`` (dict) and a list of fileinfos (list of dicts).
Each fileinfo has at least a valid UUID of an content item.
For each fileinfo in the list one file will be created.
It adapts the content with the given UUID with ``collective.azipfele.interfaces import IZipContentExtractor`` using ZCA.
If fileinfo contains an ``extractor`` (string) it uses a named adapter.

The ``IZipContentExtractor`` takes on call the fileinfo and global settings.
It is expected to return a tuple of filename and the data to be stored in the zip with the filename.
The returned filename can be a relative path as well.


Installation
============

Just depend in your buildout on the egg ``collective.azipfele``.
ZCML is loaded automagically with z3c.autoinclude.

Install ``Async Zip File Support`` as an addon in Plone control-panel or portal_setup.
Alternatively depend on ``profile-collective.azipfele:default`` in your profiles ``metadata.xml``.

This package is written for Plone 4.3 or later.


Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...) of ``collective.azipfele`` this is a great idea!

The code is located in the `github collective <https://github.com/collective/collective.azipfele>`_.

You can clone it or `get access to the github-collective <http://collective.github.com/>`_ and work directly on the project.

Maintainer is Jens Klein and the BlueDynamics Alliance developer team.
We appreciate any contribution and if a release is needed to be done on pypi,
please just contact one of us `dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_

License is GPL 2, see file ``LICENCE.rst``.


Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Benjamin Stefaner

- initially developed for and funded by Zumtobel Group AG, Austria


