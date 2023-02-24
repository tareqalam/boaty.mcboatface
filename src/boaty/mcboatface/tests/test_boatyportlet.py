# -*- coding: utf-8 -*-
from boaty.mcboatface.testing import BOATY_MCBOATFACE_FUNCTIONAL_TESTING
from boaty.mcboatface.testing import BOATY_MCBOATFACE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletType
from zope.component import getUtility

import unittest


class PortletIntegrationTest(unittest.TestCase):

    layer = BOATY_MCBOATFACE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_boatyportlet_is_registered(self):
        portlet = getUtility(
            IPortletType,
            name="boaty.mcboatface.portlets.Boatyportlet",
        )
        self.assertEqual(portlet.addview, "boaty.mcboatface.portlets.Boatyportlet")


class PortletFunctionalTest(unittest.TestCase):

    layer = BOATY_MCBOATFACE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
