from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from lcp.theme.testing import LCP_THEME_FIXTURE


class AZipFileFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)


    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.DateRecurringIndex')
        z2.installProduct(app, 'Products.TextIndexNG3')

        # Load ZCML
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity,
                      context=configurationContext)
        import zlag.mediadb
        self.loadZCML(package=zlag.mediadb,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'zlag.mediadb:robottest')


AZIPFILE_FIXTURE = AZipFileFixture()
MEDIADB_LAYER = IntegrationTesting(
    bases=(AZIPFILE_FIXTURE,),
    name="MEDIADB:Integration"
)


AZIP_ROBOT_TESTING = FunctionalTesting(
   bases=(AZIPFILE_FIXTURE, LCP_THEME_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
          z2.ZSERVER_FIXTURE),
    name="MEDIADB:Robot")


# start robotserver with
# ./bin/robot-server zlag.mediadb.testing.MEDIADB_ROBOT_TESTING


# run testscript
# ./bin/robot src/zlag/mediadb/test.robot

# run with zope testrunner
# ./bin/test -t robot
