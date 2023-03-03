# -*- coding: utf-8 -*-
from boaty.mcboatface.content.student import IStudent  # NOQA E501
from boaty.mcboatface.testing import BOATY_MCBOATFACE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility
from AccessControl.unauthorized import Unauthorized
import unittest
from plone.app.testing import login

class TestInstructorTasks(unittest.TestCase):

    layer = BOATY_MCBOATFACE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Department",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]
        api.user.create(email="instructoruser@test.com", username="instructoruser")
        setRoles(self.portal, "instructoruser", ["Instructor"])

    def test_instructor_user_login(self):
        """"""
        portal = self.layer['portal']
        login(portal, 'instructoruser')
        