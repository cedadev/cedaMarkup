'''
BSD Licence
Copyright (c) 2012, Science & Technology Facilities Council (STFC)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
        this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
    * Neither the name of the Science & Technology Facilities Council (STFC) 
        nor the names of its contributors may be used to endorse or promote 
        products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on 11 Jul 2012

@author: mnagni
'''
import unittest
from ceda_markup.markup import createMarkup
from ceda_markup.opensearch.os_request import OS_ROOT_TAG, OS_PREFIX, \
    OS_NAMESPACE, create_short_name
from xml.etree.ElementTree import tostring
from ceda_markup.opensearch.template.osresponse import Subresult
from ceda_markup.opensearch import filter_results


class OpensearchTest(unittest.TestCase):

    def filter_results_test(self):    
        inititems = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        res = filter_results(inititems, 0, 0, 0)
        self.assertEqual(inititems, res, "Error")
        res = filter_results(inititems, 3, 0, 0)
        self.assertEqual([1, 2, 3], res, "Error")        
        res = filter_results(inititems, 3, 0, 3)
        self.assertEqual([7, 8, 9], res, "Error")        
        res = filter_results(inititems, 3, 0, 4)
        self.assertEqual([10], res, "Error")        

        res = filter_results(inititems, 1, 1, 1)
        self.assertEqual(1, res[0], "Error")
        res = filter_results(inititems, 1, 1, 2)
        self.assertEqual(2, res[0], "Error")
        res = filter_results(inititems, 1, 1, 3)
        self.assertEqual(3, res[0], "Error")
        
        res = filter_results(inititems, 5, 1, 2)
        self.assertEqual([6, 7, 8, 9, 10], res, "Error")        
        res = filter_results(inititems, 5, 1, 3)
        self.assertEqual([1, 2, 3, 4, 5], res, "Error")
                
        res = filter_results(inititems, 5, 2, 1)
        self.assertEqual([2, 3, 4, 5, 6], res, "Error")                
        res = filter_results(inititems, 5, 2, 2)
        self.assertEqual([7, 8, 9, 10], res, "Error")
        res = filter_results(inititems, 5, 3, 2)
        self.assertEqual([8, 9, 10], res, "Error")
        
        res = filter_results(inititems, 5, 6, 1)
        self.assertEqual([6, 7, 8, 9, 10], res, "Error")
        res = filter_results(inititems, 5, 6, 2)
        self.assertEqual([6, 7, 8, 9, 10], res, "Error")
        res = filter_results(inititems, 5, 7, 2)
        self.assertEqual([7, 8, 9, 10], res, "Error")
        res = filter_results(inititems, 5, 10, 2)
        self.assertEqual([10], res, "Error")        

    def short_name_test(self):
        markup = createMarkup(OS_ROOT_TAG, OS_PREFIX, OS_NAMESPACE)
        markup.append(create_short_name("augh!",root = markup))
        res = tostring(markup)
        self.assertEqual(res, '<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">\
<ShortName>augh!</ShortName></OpenSearchDescription>', "Error")
        
    def subresult_test(self):
        sr = Subresult(myvar = 'ciao')
        self.assertEquals(getattr(sr, 'myvar'), 'ciao', "Error")