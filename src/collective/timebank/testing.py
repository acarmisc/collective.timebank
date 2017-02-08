# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.timebank


class CollectiveTimebankLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.timebank)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.timebank:default')


COLLECTIVE_TIMEBANK_FIXTURE = CollectiveTimebankLayer()


COLLECTIVE_TIMEBANK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TIMEBANK_FIXTURE,),
    name='CollectiveTimebankLayer:IntegrationTesting'
)


COLLECTIVE_TIMEBANK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TIMEBANK_FIXTURE,),
    name='CollectiveTimebankLayer:FunctionalTesting'
)


COLLECTIVE_TIMEBANK_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TIMEBANK_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveTimebankLayer:AcceptanceTesting'
)
