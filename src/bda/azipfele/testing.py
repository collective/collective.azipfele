# -*- coding: utf-8 -*-

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class AZipFileFixture(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # z2.installProduct(app, 'Products.DateRecurringIndex')

        # Load ZCML
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity,
                      context=configurationContext)
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes,
                      context=configurationContext)

        import bda.azipfele
        self.loadZCML(package=bda.azipfele,
                      context=configurationContext)

        def setUpPloneSite(self, portal):
            self.applyProfile(portal, 'bda.azipfele:default')


AZIPFILE_FIXTURE = AZipFileFixture()
AZIPFILE_LAYER = IntegrationTesting(
    bases=(AZIPFILE_FIXTURE,),
    name="AZIPFILE:Integration"
)

AZIP_ROBOT_TESTING = FunctionalTesting(
    bases=(AZIPFILE_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="AZIPFILE:Robot")


# start robotserver with
# ./bin/robot-server zlag.mediadb.testing.MEDIADB_ROBOT_TESTING


# run testscript
# ./bin/robot src/zlag/mediadb/test.robot

# run with zope testrunner
# ./bin/test -t robot
