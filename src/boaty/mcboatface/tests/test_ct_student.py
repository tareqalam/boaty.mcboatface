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
from plone.app.testing import login, logout

class StudentIntegrationTest(unittest.TestCase):

    layer = BOATY_MCBOATFACE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        api.user.create(email="testmanager@test.com", username="testmanager")
        setRoles(self.portal, "testmanager", ["Manager"])
        # setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, "testmanager")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "Department",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]
        logout()
        api.user.create(email="teststudent@test.com", username="teststudent")
        setRoles(self.portal, "teststudent", ["Student"])
        login(self.portal, "teststudent")
        

    def test_ct_student_schema(self):
        fti = queryUtility(IDexterityFTI, name="Student")
        schema = fti.lookupSchema()
        self.assertEqual(IStudent, schema)

    def test_ct_student_fti(self):
        fti = queryUtility(IDexterityFTI, name="Student")
        self.assertTrue(fti)

    def test_ct_student_factory(self):
        fti = queryUtility(IDexterityFTI, name="Student")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IStudent.providedBy(obj),
            "IStudent not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_student_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Instructor"])
        obj = api.content.create(
            container=self.parent,
            type="Student",
            id="student",
        )

        self.assertTrue(
            IStudent.providedBy(obj),
            "IStudent not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("student", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("student", parent.objectIds())

    def test_ct_student_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Student")
        self.assertFalse(fti.global_allow, "{0} is globally addable!".format(fti.id))

    def test_student_cannot_add_student(self):
        # setRoles(self.portal, TEST_USER_ID, ["Student"])
        # import pdb;pdb.set_trace()
        try:
            obj = api.content.create(
                container=self.parent,
                type="Student",
                id="student",
            )
            raise RuntimeError('Student are not allowed to add student!')
        except Unauthorized:
            pass