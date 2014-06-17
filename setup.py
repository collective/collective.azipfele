from setuptools import setup, find_packages
import sys, os

version = '1.0'
shortdesc = 'bda azipfele'
longdesc = ""

setup(name='bda.azipfele',
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
      package_dir = {'': 'src'},
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.js.angular',
          'collective.zamqp',
          'Plone',
          'plone.api',
          'plone.app.robotframework',
          'plone.app.contenttypes',
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
