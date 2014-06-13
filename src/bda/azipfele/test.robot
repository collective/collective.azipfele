*** Settings ***

#keyword resources
Resource   plone/app/robotframework/selenium.robot
Resource   plone/app/robotframework/keywords.robot
Variables  bda/azipfele/test/robottest_variables.py
Resource   bda/azipfele/test/robottest_keywords.robot
#Resource  plone/app/contenttypes/tests/robot/keywords.txt


Library  Remote  ${PLONE_URL}/RobotRemote

#make selenium slower to follow tests
#Suite setup  Set Selenium speed  0.5s

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***


*** Test Cases ***

Login and accept terms and conditions
    Given I'm logged in as admin
    When I go to the media db
    And I click on accept terms
    And I click start db
    Then the mdbfolder should be visible

