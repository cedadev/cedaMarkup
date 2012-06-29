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

Created on 29 Jun 2012

@author: mnagni
'''
import unittest
from xml.etree.ElementTree import tostring, Element
from ceda_markup.dc.dc import createDC, createDate

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testDC(self):
        dc = createDC()
        self.assertEqual(tostring(dc), '<metadata xmlns="http://purl.org/dc/elements/1.1/" />')
        
        root = Element('myCustomTag')             
        dc = createDC(root = root)
        root.append(dc)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:metadata /></myCustomTag>')

    def testDate(self):
        #gml tag as root
        dc = createDC()
        date = createTestDate(root = dc)
        dc.append(date)        
        self.assertEqual(tostring(dc), '<metadata xmlns="http://purl.org/dc/elements/1.1/">\
<date>2007-09-02T08:31:15.664Z/2011-10-11T07:45:33.000Z</date></metadata>')
        
        #gml tag as SubElement of another root element
        root = Element('myCustomTag')
        date = createTestDate(root = root)
        root.append(date)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:dc="http://purl.org/dc/elements/1.1/">\
<dc:date>2007-09-02T08:31:15.664Z/2011-10-11T07:45:33.000Z</dc:date></myCustomTag>')

def createTestDate(root = None, body = '2007-09-02T08:31:15.664Z/2011-10-11T07:45:33.000Z'):         
    return createDate(root, body)
