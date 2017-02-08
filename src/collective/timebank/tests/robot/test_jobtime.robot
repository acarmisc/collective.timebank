# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.timebank -t test_jobtime.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.timebank.testing.COLLECTIVE_TIMEBANK_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_jobtime.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a JobTime
  Given a logged-in site administrator
    and an add jobtime form
   When I type 'My JobTime' into the title field
    and I submit the form
   Then a jobtime with the title 'My JobTime' has been created

Scenario: As a site administrator I can view a JobTime
  Given a logged-in site administrator
    and a jobtime 'My JobTime'
   When I go to the jobtime view
   Then I can see the jobtime title 'My JobTime'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add jobtime form
  Go To  ${PLONE_URL}/++add++JobTime

a jobtime 'My JobTime'
  Create content  type=JobTime  id=my-jobtime  title=My JobTime


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the jobtime view
  Go To  ${PLONE_URL}/my-jobtime
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a jobtime with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the jobtime title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
