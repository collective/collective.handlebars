# -*- coding: utf-8 -*-
from collective.handlebars.browser.views import HandlebarsBrowserView
from collective.handlebars.browser.views import HandlebarsPloneView
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.handlebars


class CollectiveHandlebarsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.handlebars)
        self.loadZCML(package=collective.handlebars, name='testing.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.handlebars:default')


class HBSTestView(HandlebarsBrowserView):

    def get_contents(self):
        return {'title': u'Fäncy Title', 'body': u'This is the body'}


class HBSTestPloneView(HandlebarsPloneView):

    def get_contents(self):
        return {'title': u'Fäncy Title',
                'body': u'This is the Plone View body'}


COLLECTIVE_HANDLEBARS_FIXTURE = CollectiveHandlebarsLayer()


COLLECTIVE_HANDLEBARS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_HANDLEBARS_FIXTURE,),
    name='CollectiveHandlebarsLayer:IntegrationTesting'
)


COLLECTIVE_HANDLEBARS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_HANDLEBARS_FIXTURE,),
    name='CollectiveHandlebarsLayer:FunctionalTesting'
)


COLLECTIVE_HANDLEBARS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_HANDLEBARS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveHandlebarsLayer:AcceptanceTesting'
)
