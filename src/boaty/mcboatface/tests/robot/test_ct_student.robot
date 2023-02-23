# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s boaty.mcboatface -t test_student.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src boaty.mcboatface.testing.BOATY_MCBOATFACE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/boaty/mcboatface/tests/robot/test_student.robot
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

Scenario: As a site administrator I can add a Student
  Given a logged-in site administrator
    and an add Department form
   When I type 'My Student' into the title field
    and I submit the form
   Then a Student with the title 'My Student' has been created

Scenario: As a site administrator I can view a Student
  Given a logged-in site administrator
    and a Student 'My Student'
   When I go to the Student view
   Then I can see the Student title 'My Student'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Department form
  Go To  ${PLONE_URL}/++add++Department

a Student 'My Student'
  Create content  type=Department  id=my-student  title=My Student

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Student view
  Go To  ${PLONE_URL}/my-student
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Student with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Student title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
