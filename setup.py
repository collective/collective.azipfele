# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os

version = '2.0.0'
shortdesc = 'Creates Zip files from Plone or other content asynchronous'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENCE.rst')).read()

setup(
    name='collective.azipfele',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='async zip plone',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://bluedynamics.com',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.contenttypes',
        'Products.CMFPlone',
        'python-memcached',
        'setuptools',
    ],
    extras_require={
        'zamqp': [
            'collective.zamqp',
        ],
        'taskqueue': [
            'collective.taskqueue',
        ],
        'test': [
            'interlude[ipython]>=1.3.1',
            'ipdb',
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
