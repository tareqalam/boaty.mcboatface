# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s boaty.mcboatface -t test_department.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src boaty.mcboatface.testing.BOATY_MCBOATFACE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/boaty/mcboatface/tests/robot/test_department.robot
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

Scenario: As a site administrator I can add a Department
  Given a logged-in site administrator
    and an add Department form
   When I type 'My Department' into the title field
    and I submit the form
   Then a Department with the title 'My Department' has been created

Scenario: As a site administrator I can view a Department
  Given a logged-in site administrator
    and a Department 'My Department'
   When I go to the Department view
   Then I can see the Department title 'My Department'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Department form
  Go To  ${PLONE_URL}/++add++Department

a Department 'My Department'
  Create content  type=Department  id=my-department  title=My Department

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Department view
  Go To  ${PLONE_URL}/my-department
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Department with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Department title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
