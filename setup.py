from setuptools import setup, find_packages
import os

version = '1.1.2'
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
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        "Framework :: Plone",
    ],
    keywords='',
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
        'collective.zamqp',
        'Plone',
        'plone.api',
        'plone.app.contenttypes',
        'python-memcached',
        'setuptools',
    ],
    extras_require={
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
