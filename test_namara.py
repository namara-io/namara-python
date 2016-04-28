from unittest import TestCase
from mock import Mock
from namara import Namara

class TestNamara(TestCase):
    subject = None

    def setUp(self):
        self.subject = Namara('myapikey')
        self.dataset = '18b854e3-66bd-4a00-afba-8eabfc54f524'
        self.version = 'en-2'

    def test_base_path(self):
        path = self.subject.get_base_path(self.dataset, self.version)
        self.assertTrue(path == 'https://api.namara.io/v0/data_sets/18b854e3-66bd-4a00-afba-8eabfc54f524/data/en-2')

    def test_path(self):
        path = self.subject.get_path(self.dataset, self.version)
        self.assertTrue(path == 'https://api.namara.io/v0/data_sets/18b854e3-66bd-4a00-afba-8eabfc54f524/data/en-2?api_key=myapikey')

    def test_get_where_field_value_greater_than_1200(self):
        self.subject.get = Mock(return_value=[{u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1201, u'location': u'FORT FRANCES', u'facility_type': u'PULP'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'MANITOU FOREST PRODUCTS LTD.', u'facility_code': 1221, u'location': u'EMO', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'531322 ONTARIO LTD. O/A NICKEL LAKE LUMBER', u'facility_code': 1232, u'location': u'FORT FRANCES', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'AINSWORTH GP LTD.', u'facility_code': 1240, u'location': u'BARWICK', u'facility_type': u'COMPOSITE'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1301, u'location': u'IGNACE', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'E.&G. CUSTOM SAWING LTD.', u'facility_code': 1410, u'location': u'KENORA', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'WEYERHAEUSER COMPANY LTD.', u'facility_code': 1422, u'location': u'KENORA', u'facility_type': u'COMPOSITE'}])
        response = self.subject.get(self.dataset, self.version, options={'where': 'facility_code > 1000'})
        for i in range(0, len(response)):
            if response[i].get('facility_code') <= 1200:
                self.assertTrue(False)
        self.assertTrue(True)

    def test_get_count(self):
        self.subject.get = Mock(return_value={u'result': 129})
        response = self.subject.get(self.dataset, self.version, options={'operation': 'count(*)'})
        self.assertTrue(response.get('result') == 129)
