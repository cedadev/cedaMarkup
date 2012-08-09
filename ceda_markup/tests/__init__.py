from unittest import TestSuite
from ceda_markup.tests.opensearch.opensearch import OpensearchTest
from ceda_markup.tests.atom import AtomTest
from ceda_markup.tests.common import CommonTest
from ceda_markup.tests.dc import DCTest
from ceda_markup.tests.georss import GeoRSSTest
from ceda_markup.tests.gml import GmlTest

def suite():
    suite = TestSuite()
    suite.addTest(CommonTest)    
    suite.addTest(OpensearchTest)    
    suite.addTest(AtomTest)
    suite.addTest(DCTest)    
    suite.addTest(GeoRSSTest)    
    suite.addTest(GmlTest)    
            
    return suite