# -*- coding: utf-8 -*-
# @Date    : 2018-01-29 17:42:51
# @Author  : Md Nazrul Islam (email2nazrul@gmail.com)
# @Link    : http://nazrul.me/
# @Version : $Id$
# All imports here
from fhir.heart.compat import json
from fhir.heart.compat import pathlib
from fhir.heart.utils import get_fhir_field
from fhir.heart.testing import FHIR_HEART_FUNCTIONAL_TESTING
from fhir.heart.testing import FHIR_HEART_INTEGRATION_TESTING
from fhir.heart.testing import FHIR_HEART_REST_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from plone.testing import z2

import logging
import os
import six
import sys
import transaction
import unittest


__author__ = 'Md Nazrul Islam (email2nazrul@gmail.com)'


FIXTURE_DIRECTORY = \
    pathlib.Path(os.path.dirname(os.path.abspath(__file__))) / 'fixtures'
FHIR_RESOURCE_DIRECTORY = FIXTURE_DIRECTORY / 'FHIR'


class BaseIntegrationTest(unittest.TestCase):
    """" """
    layer = FHIR_HEART_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.enable_event_log()
        self.portal = self.layer['portal']
        # prepare the user
        self.init_fixture()

    def init_fixture(self):
        """ """
        with api.env.adopt_roles('Manager'):

            with open(str(FHIR_RESOURCE_DIRECTORY / 'Organization' / 'Organization.json'), 'r') as f:  # noqa: E501
                fhir = json.load(f)
            hospital = api.content.create(
                self.portal,
                fhir['resourceType'],
                id=fhir['id'],
                title=fhir['name'])

            fhir_field = get_fhir_field(obj=hospital)

            setattr(hospital,
                    fhir_field.getName(),
                    fhir_field.bind(hospital).from_dict(fhir))

    def enable_event_log(self, loggers=None, plone_log_level='ERROR'):
        """
            :param loggers: dict of loggers. format {'logger name': 'level name'}
            :param plone_log_level: log level of plone. default is ERROR
         """
        defaults = {
            'fhir.heart': 'INFO'
        }
        from Products.CMFPlone.log import logger

        loggers = loggers or defaults

        for logger_name, level_name in six.iteritems(loggers):
            logging.getLogger(logger_name).setLevel(getattr(logging, level_name.upper()))
        # Plone log level:
        logger.root.setLevel(getattr(logging, plone_log_level.upper()))

        # Enable output when running tests:
        logger.root.addHandler(logging.StreamHandler(sys.stdout))


class BaseServiceIntegrationTest(BaseIntegrationTest):
    """" """

    def prepare_request(self, method='GET'):
        """ """
        request = self.layer['request'].clone()
        request.method = method
        request.environ.update({
            'ACCEPT': 'application/json',
            'CONTENT_TYPE': 'application/json',
            'ACCEPT_LANGUAGE': 'en',
            'REQUEST_METHOD': method
            })
        return request


class BaseFunctionalTest(unittest.TestCase):
    """ """
    layer = FHIR_HEART_FUNCTIONAL_TESTING

    def setUp(self):
        """" """
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.admin_browser = z2.Browser(self.layer['app'])
        self.admin_browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        self.anon_browser = z2.Browser(self.layer['app'])

        self.error_setup(self.admin_browser)
        self.error_setup(self.anon_browser)

        self.enable_event_log()

    def init_fixture(self):
        """ """
        with api.env.adopt_roles('Manager'):
            with open(str(FHIR_RESOURCE_DIRECTORY / 'Organization' / 'Organization.json'), 'r') as f:  # noqa: E501
                fhir = json.load(f)
            hospital = api.content.create(
                self.portal,
                fhir['resourceType'],
                id=fhir['id'],
                title=fhir['name'])

            fhir_field = get_fhir_field(obj=hospital)

            setattr(hospital,
                    fhir_field.getName(),
                    fhir_field.bind(hospital).from_dict(fhir))

            transaction.commit()

    def enable_event_log(self, loggers=None, plone_log_level='ERROR'):
        """
            :param loggers: dict of loggers. format {'logger name': 'level name'}
            :param plone_log_level: log level of plone. default is ERROR
         """
        defaults = {
            'fhir.heart': 'INFO'
        }
        from Products.CMFPlone.log import logger

        loggers = loggers or defaults

        for logger_name, level_name in six.iteritems(loggers):
            logging.getLogger(logger_name).setLevel(getattr(logging, level_name.upper()))
        # Plone log level:
        logger.root.setLevel(getattr(logging, plone_log_level.upper()))

        # Enable output when running tests:
        logger.root.addHandler(logging.StreamHandler(sys.stdout))

    def error_setup(self, browser):
        """ """
        browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print (info[1])

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising


class BaseServiceFunctionalTest(BaseFunctionalTest):
    """ """
    layer = FHIR_HEART_REST_FUNCTIONAL_TESTING

    def setUp(self):
        """" """
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()

        self.admin_session = self.make_session()
        self.admin_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.anon_session = self.make_session()

        self.enable_event_log()

    def make_session(self, base_url=None):
        """ """
        base_url = base_url or self.portal_url
        session = RelativeSession(base_url)
        session.headers.update({
            'Accept-Language': 'en',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        return session
