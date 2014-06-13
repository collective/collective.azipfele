from .testing import MEDIADB_LAYER
from .testing import MEDIADB_ROBOT_TESTING
from interlude import interact
from plone.testing import layered
from plone.testing import z2
import doctest
import pkg_resources
import pprint
import robotsuite
import unittest

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE
# --udiff doesnt get grip on cmdline
optionflags = optionflags | doctest.REPORT_UDIFF

basedir = pkg_resources.ResourceManager().resource_filename(__name__, '.')

TESTFILES = [
    'test/azipfele.rst',
]

def test_suite():
    suite = unittest.TestSuite()
    tests = []
    for testfile in TESTFILES:
        if testfile.endswith('.rst'):
            test = doctest.DocFileSuite(
                testfile,
                globs={'interact': interact,
                        'pprint': pprint.pprint,
                        'z2': z2,
                        'basedir':basedir,
                },
                optionflags=optionflags,
            )
            tests.append(layered(test, layer=MEDIADB_LAYER))

        if testfile.endswith('.robot'):
            test = robotsuite.RobotTestSuite(testfile)
            tests.append(layered(test, layer=MEDIADB_ROBOT_TESTING))

    suite.addTests(tests)
    return suite

