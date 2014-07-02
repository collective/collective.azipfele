# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.dexterity.utils import createContentInContainer
from plone.testing import z2


class AZipFileFixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.azipfele
        self.loadZCML(package=collective.azipfele,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.azipfele:default')
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        folder = createContentInContainer(
            portal, 'Folder',
            title=u'folder',
            description=u'Some Folder'
        )
        folder.indexObject()


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
