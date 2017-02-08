# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.timebank.testing import COLLECTIVE_TIMEBANK_INTEGRATION_TESTING  # noqa
from collective.timebank.interfaces import IJobTime

import unittest2 as unittest


class JobTimeIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_TIMEBANK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='JobTime')
        schema = fti.lookupSchema()
        self.assertEqual(IJobTime, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='JobTime')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='JobTime')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IJobTime.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('JobTime', 'JobTime')
        self.assertTrue(
            IJobTime.providedBy(self.portal['JobTime'])
        )
