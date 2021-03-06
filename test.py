import unittest

import data_helper
import utils
import analyze
import pdb
import logging
from analyze.users import get_one_time_builder_application_ids

_TEST_DATA_FILE = "test-data/some-lupapiste-usage-pub-20161031.csv"
_OPERATIVE_TEST_DATA_FILE = "test-data/some-applications-operative-pub-20161031.csv"

class TestApplicationSummary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.odf = data_helper.import_operative_data(_OPERATIVE_TEST_DATA_FILE)
        self.udf = data_helper.import_usage_data(_TEST_DATA_FILE)        
        self.apps = analyze.summarize_applications(self.odf, self.udf)

    def test_number_of_applications(self):
        self.assertEqual(len(self.apps), 10)

    def test_number_of_events(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['nEvents'].item(), 675)

    def test_number_of_comments(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['nApplicationComments'].item(), 16)
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['nApplicationCommentsApplicant'].item(), 5)
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['nApplicationCommentsAuthority'].item(), 11)

    def test_session_length(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['sessionLength'].item(), 462)
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['sessionLengthApplicant'].item(), 143)
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['sessionLengthAuthority'].item(), 279)
            
    def test_lead_time(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['leadTime'].item(), 35)
    
    def test_application_month(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['createdMonth'].item(), 10)
    
    def test_application_weekday(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['createdWeekDay'].item(), 4)
        
    def test_application_hour(self):
        self.assertEqual(self.apps[self.apps['applicationId'] == 'LP-1001-219067']['createdHour'].item(), 9)    
    
class TestUsersSummary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.odf = data_helper.import_operative_data(_OPERATIVE_TEST_DATA_FILE)
        self.udf = data_helper.import_usage_data(_TEST_DATA_FILE)        
        self.users = analyze.summarize_users(self.odf, self.udf)

    def test_number_of_users(self):
        self.assertEqual(len(self.users), 71)
    
    def test_one_time_builder_applications(self):
        self.one_time_builder_applications = analyze.get_one_time_builder_application_ids(self.users)
        self.assertEqual(len(self.one_time_builder_applications), 9)
        

if __name__ == '__main__':
    unittest.main()

