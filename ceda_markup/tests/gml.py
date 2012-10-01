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

Created on 28 Jun 2012

@author: mnagni
'''
import unittest
from xml.etree.ElementTree import tostring, Element
from ceda_markup.gml.gml import createGML, createPosList, createLinearRing,\
    createExterior, createPolygon, createBeginPosition, createEndPosition,\
    createTimePeriod, createValidTime


class GmlTest(unittest.TestCase):

    def gml_test(self):
        #gml tag as root
        gml = createGML()        
        self.assertEqual(tostring(gml), '<metadata xmlns="http://www.opengis.net/gml" />')
        
        #gml tag as SubElement of another root element
        root = Element('myCustomTag')
        gml = createGML(root)
        root.append(gml)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:metadata />\
</myCustomTag>')

    def pos_list_test(self):   
        postList = create_test_pos_list()         
        self.assertEqual(tostring(postList), '<posList xmlns="http://www.opengis.net/gml">45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </posList>')
        
        root = Element('myCustomTag')
        postList = create_test_pos_list(root)
        root.append(postList)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml">\
<gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </gml:posList></myCustomTag>')
        
    def linear_ring(self):
        root = createGML()
        linearRing = create_test_linear_ring(root)
        root.append(linearRing)
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml">\
<LinearRing><posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45</posList></LinearRing></metadata>')
        
        root = Element('myCustomTag')
        linearRing = create_test_linear_ring(root)
        root.append(linearRing)                
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml">\
<gml:LinearRing><gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45</gml:posList>\
</gml:LinearRing></myCustomTag>')
        
    def exterior_test(self):
        iroot = createGML()
        exterior = create_test_exterior(iroot)
        iroot.append(exterior) 
        self.assertEqual(tostring(iroot), '<metadata xmlns="http://www.opengis.net/gml"><exterior>\
<LinearRing><posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </posList></LinearRing></exterior></metadata>')
        
        iroot = Element('myCustomTag')
        exterior = create_test_exterior(iroot)
        iroot.append(exterior)                        
        self.assertEqual(tostring(iroot), '<myCustomTag xmlns:gml="http://www.opengis.net/gml">\
<gml:exterior><gml:LinearRing><gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </gml:posList>\
</gml:LinearRing></gml:exterior></myCustomTag>')        
        
    def polygon_test(self):
        root = createGML()
        polygon = create_test_polygon(root = root)
        root.append(polygon)         
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml"><Polygon><exterior>\
<LinearRing><posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </posList></LinearRing></exterior></Polygon></metadata>')
        
        root = Element('myCustomTag')
        polygon = create_test_polygon(root)
        root.append(polygon)                 
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:Polygon><gml:exterior>\
<gml:LinearRing><gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </gml:posList></gml:LinearRing>\
</gml:exterior></gml:Polygon></myCustomTag>')        
        
    def begin_position_test(self):                
        root = createGML()
        bp = create_test_begin_position(root)
        root.append(bp)         
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml"><beginPosition>2011-03-20T12:31:15.451Z</beginPosition></metadata>')        
                
        root = Element('myCustomTag')
        bp = create_test_begin_position(root)
        root.append(bp)         
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:beginPosition>2011-03-20T12:31:15.451Z</gml:beginPosition></myCustomTag>')                
                
    def end_position_test(self):                
        root = createGML()
        bp = create_test_end_position(root)
        root.append(bp)         
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml"><endPosition>2011-03-20T12:31:15.451Z</endPosition></metadata>')        
                
        root = Element('myCustomTag')
        bp = create_test_end_position(root)
        root.append(bp)         
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:endPosition>2011-03-20T12:31:15.451Z</gml:endPosition></myCustomTag>')                
                
    def time_period_test(self):                
        root = createGML()
        tp = create_test_time_period(root)
        root.append(tp)                         
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml"><TimePeriod>\
<beginPosition>2011-03-20T12:31:15.451Z</beginPosition><endPosition>2011-03-20T12:31:15.451Z</endPosition>\
</TimePeriod></metadata>')        
                
        root = Element('myCustomTag')
        tp = create_test_time_period(root)
        root.append(tp)         
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:TimePeriod>\
<gml:beginPosition>2011-03-20T12:31:15.451Z</gml:beginPosition><gml:endPosition>2011-03-20T12:31:15.451Z</gml:endPosition>\
</gml:TimePeriod></myCustomTag>')     
        
    def valid_time_test(self):
        root = createGML()
        vt = create_test_valid_time(root)
        root.append(vt)                 
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.opengis.net/gml"><validTime>\
<TimePeriod><beginPosition>2011-03-20T12:31:15.451Z</beginPosition><endPosition>2011-03-20T12:31:15.451Z</endPosition>\
</TimePeriod></validTime></metadata>')        
                
        root = Element('myCustomTag')
        vt = create_test_valid_time(root)
        root.append(vt)         
        self.assertEqual(tostring(root), '<myCustomTag xmlns:gml="http://www.opengis.net/gml"><gml:validTime>\
<gml:TimePeriod><gml:beginPosition>2011-03-20T12:31:15.451Z</gml:beginPosition>\
<gml:endPosition>2011-03-20T12:31:15.451Z</gml:endPosition></gml:TimePeriod></gml:validTime></myCustomTag>')                 
                
def create_test_pos_list(root = None, body = [45.256, -110.45, 46.46, 
                                              -109.48, 43.84, -109.86, 
                                              45.256, -110.45]):
    return createPosList(root, values = body)

def create_test_linear_ring(root = None, body = None):
    if body == None:
        return createLinearRing(root, body = create_test_pos_list(root))
    return createLinearRing(root, body = body)

def create_test_exterior(root = None, body = None):
    if body == None:        
        return createExterior(root, body = create_test_linear_ring(root))         
    return createExterior(root, body)

def create_test_polygon(root = None, body = None):
    if body == None:        
        return createPolygon(root, exterior = create_test_exterior(root))         
    return createPolygon(root, body = body)

def create_test_begin_position(root = None, body = '2011-03-20T12:31:15.451Z'):
    return createBeginPosition(root, body = body)

def create_test_end_position(root = None, body = '2011-03-20T12:31:15.451Z'):
    return createEndPosition(root, body = body)    

def create_test_time_period(root = None, begin = None, end = None):  
    if begin == None or end == None:
        begin = create_test_begin_position(root)        
        end = create_test_end_position(root)            
        return createTimePeriod(root, begin = begin, end = end)         
    return createTimePeriod(root, begin = begin, end = end)  

def create_test_valid_time(root = None, body = None):
    if body == None:        
        return createValidTime(root, body = create_test_time_period(root))         
    return createValidTime(root, body = body)  