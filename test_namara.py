from unittest import TestCase

import pandas as pd
from mock import Mock

from namara import Namara


class TestNamara(TestCase):
    subject = None

    def setUp(self):
        self.subject = Namara('myapikey')
        self.dataset = '18b854e3-66bd-4a00-afba-8eabfc54f524'
        self.version = 'en-2'

    def test_get_url(self): 
        path = self.subject.get_url('/organizations/{0}/projects/{1}/data_sets'.format('organization', 'project'))
        self.assertTrue(path == 'https://api.namara.io/v0/organizations/organization/projects/project/data_sets')

    def test_is_aggregation(self): 
        options = {'limit': 10, 'operation': 'avg(column_1)'} 
        self.assertTrue(self.subject.is_aggregation(options))

    def test_get_where_field_value_greater_than_1200(self):
        self.subject.get = Mock(return_value=[{u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1201, u'location': u'FORT FRANCES', u'facility_type': u'PULP'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'MANITOU FOREST PRODUCTS LTD.', u'facility_code': 1221, u'location': u'EMO', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'531322 ONTARIO LTD. O/A NICKEL LAKE LUMBER', u'facility_code': 1232, u'location': u'FORT FRANCES', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'AINSWORTH GP LTD.', u'facility_code': 1240, u'location': u'BARWICK', u'facility_type': u'COMPOSITE'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1301, u'location': u'IGNACE', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'E.&G. CUSTOM SAWING LTD.', u'facility_code': 1410, u'location': u'KENORA', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'WEYERHAEUSER COMPANY LTD.', u'facility_code': 1422, u'location': u'KENORA', u'facility_type': u'COMPOSITE'}])
        response = self.subject.get(self.dataset, self.version, options={'where': 'facility_code > 1200'})
        for res in response:
            if res.get('facility_code') <= 1200:
                self.assertTrue(False)
        self.assertTrue(True)

    def test_get_count(self):
        self.subject.get = Mock(return_value={u'result': 129})
        response = self.subject.get(self.dataset, self.version, options={'operation': 'count(*)'})
        self.assertTrue(response.get('result') == 129)

    def test_valid_output_format(self): 
        self.assertRaises(ValueError, self.subject.get, self.dataset, self.version, output_format='invalid-format')

    def test_valid_json_output(self): 
        self.subject.get = Mock(return_value=[{u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1201, u'location': u'FORT FRANCES', u'facility_type': u'PULP'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'MANITOU FOREST PRODUCTS LTD.', u'facility_code': 1221, u'location': u'EMO', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'531322 ONTARIO LTD. O/A NICKEL LAKE LUMBER', u'facility_code': 1232, u'location': u'FORT FRANCES', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'AINSWORTH GP LTD.', u'facility_code': 1240, u'location': u'BARWICK', u'facility_type': u'COMPOSITE'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'RESOLUTE FP CANADA INC.', u'facility_code': 1301, u'location': u'IGNACE', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'E.&G. CUSTOM SAWING LTD.', u'facility_code': 1410, u'location': u'KENORA', u'facility_type': u'SAWMILL'}, {u'mnr_region': u'NORTHWEST', u'facility_name': u'WEYERHAEUSER COMPANY LTD.', u'facility_code': 1422, u'location': u'KENORA', u'facility_type': u'COMPOSITE'}])
        response = self.subject.get(self.dataset, self.version, options={'operation': 'count(*)'}, output_format='json')
        self.assertTrue(isinstance(response, list))

    def test_valid_get_dataframe_ouput(self): 
        self.subject.get = Mock(return_value=pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]}))
        response = self.subject.get(self.dataset, self.version, options={'operation': 'count(*)'}, output_format='dataframe')
        self.assertTrue(isinstance(response, pd.DataFrame))
