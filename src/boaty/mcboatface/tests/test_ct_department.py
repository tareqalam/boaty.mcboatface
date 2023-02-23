# -*- coding: utf-8 -*-
from boaty.mcboatface.content.department import IDepartment  # NOQA E501
from boaty.mcboatface.testing import BOATY_MCBOATFACE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class DepartmentIntegrationTest(unittest.TestCase):

    layer = BOATY_MCBOATFACE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.parent = self.portal

    def test_ct_department_schema(self):
        fti = queryUtility(IDexterityFTI, name="Department")
        schema = fti.lookupSchema()
        self.assertEqual(IDepartment, schema)

    def test_ct_department_fti(self):
        fti = queryUtility(IDexterityFTI, name="Department")
        self.assertTrue(fti)

    def test_ct_department_factory(self):
        fti = queryUtility(IDexterityFTI, name="Department")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IDepartment.providedBy(obj),
            "IDepartment not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_department_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.portal,
            type="Department",
            id="department",
        )

        self.assertTrue(
            IDepartment.providedBy(obj),
            "IDepartment not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("department", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("department", parent.objectIds())

    def test_ct_department_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Department")
        self.assertTrue(fti.global_allow, "{0} is not globally addable!".format(fti.id))

    def test_ct_department_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="Department")
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            "department_id",
            title="Department container",
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type="Document",
            title="My Content",
        )
        self.assertTrue(obj, "Cannot add {0} to {1} container!".format(obj.id, fti.id))
