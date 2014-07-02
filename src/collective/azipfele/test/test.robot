*** Settings ***

#keyword resources
Resource   plone/app/robotframework/selenium.robot
Resource   plone/app/robotframework/keywords.robot
Variables  collective/azipfele/test/robottest_variables.py
Resource   collective/azipfele/test/robottest_keywords.robot
#Resource  plone/app/contenttypes/tests/robot/keywords.txt


Library  Remote  ${PLONE_URL}/RobotRemote

#make selenium slower to follow tests
#Suite setup  Set Selenium speed  0.5s

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***


*** Test Cases ***

Scenario: start
    Given I'm logged in as admin

