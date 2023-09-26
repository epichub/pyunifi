#!/usr/bin/env python3
import logging
import unittest

import pytest
import vcr
from unifiwrapper import TrafficRule, UnifiController, getlogininfo
from utils import myordered

logging.basicConfig(level=logging.DEBUG)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


@pytest.fixture(scope="class")
def controller_class(request):
    UNIFI_USERNAME, UNIFI_PASSWORD, UNIFI_HOSTNAME = getlogininfo()
    request.cls.controller = UnifiController(host=UNIFI_HOSTNAME,
                                             password=UNIFI_PASSWORD,
                                             username=UNIFI_USERNAME)


@pytest.mark.usefixtures("controller_class")
class TestUNIFIWrapper(unittest.TestCase):

    @vcr.use_cassette('tests/vcr_cassettes/tokentest.yml',
                      match_on=['uri', 'headers'], record_mode='new_episodes')
    def testtoken(self):
        assert hasattr(self, "controller")

        assert len(self.controller.token) > 0

    def testgetallsites(self):
        sites = self.controller.sites
        assert len(sites) > 0

    @vcr.use_cassette('tests/vcr_cassettes/gettrafficruletest.yml',
                      match_on=['uri', 'headers'])
    def testgettrafficrules(self):
        trafficrules = self.controller.trafficrules

        assert len(trafficrules) > 0

        for rule in trafficrules:
            json1 = rule._jsondata
            trule: TrafficRule = rule
            json2 = trule.to_json()
            assert myordered(json1) == myordered(json2)

    @vcr.use_cassette('tests/vcr_cassettes/testenabletrafficrules.yml',
                      match_on=['uri', 'headers'], record_mode='new_episodes')
    def testenabletrafficrules(self):
        trafficrules = self.controller.trafficrules

        assert len(trafficrules) > 0

        for rule in trafficrules:
            rule.enable()
            #rule.disable()
