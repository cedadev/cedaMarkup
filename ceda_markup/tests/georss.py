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
from ceda_markup.georss.georss import createGEORSS, createWhere
from ceda_markup.tests.gml import create_test_polygon
from ceda_markup.georss import create_where_from_postgis


class GeoRSSTest(unittest.TestCase):

    def georss_test(self):
        #georss tag as root
        root = createGEORSS()                
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.georss.org/georss" />')
        
        #georss tag as SubElement of another root element
        root = Element('myCustomTag')
        georss = createGEORSS(root)
        root.append(georss)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:georss="http://www.georss.org/georss"><georss:metadata /></myCustomTag>')
        
    def where_test(self):
        root = createGEORSS() 
        where = createWhere(root, body = create_test_polygon(root))
        root.append(where)             
        self.assertEqual(tostring(root), '<metadata xmlns="http://www.georss.org/georss" xmlns:gml="http://www.opengis.net/gml">\
<where><gml:Polygon><gml:exterior><gml:LinearRing>\
<gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </gml:posList>\
</gml:LinearRing></gml:exterior></gml:Polygon></where></metadata>')
        
        root = Element('myCustomTag')
        georss = createWhere(root, body = create_test_polygon(root))
        root.append(georss)        
        self.assertEqual(tostring(root), '<myCustomTag xmlns:georss="http://www.georss.org/georss" xmlns:gml="http://www.opengis.net/gml">\
<georss:where><gml:Polygon><gml:exterior><gml:LinearRing>\
<gml:posList>45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45 </gml:posList>\
</gml:LinearRing></gml:exterior></gml:Polygon></georss:where></myCustomTag>')   
        
                     
    def create_where_from_postgis_test(self):
        root = createGEORSS()
        georss = \
            create_where_from_postgis('BOX2D(45.256 -110.45, 46.46 -109.48)', 
                                      root)
        root.append(georss)
        self.assertEqual(tostring(root), 
                         '<metadata xmlns="http://www.georss.org/georss" \
xmlns:gml="http://www.opengis.net/gml"><where><gml:Envelope>\
<gml:lowerCorner>45.256 -110.45 </gml:lowerCorner>\
<gml:upperCorner>46.46 -109.48 </gml:upperCorner>\
</gml:Envelope></where></metadata>')
        
        root = createGEORSS()
        georss = \
            create_where_from_postgis('POLYGON((-71.1776585052917 42.3902909739571, -71.1776585052917 42.3902909739571))', 
                                      root)
        root.append(georss)
        self.assertEqual(tostring(root), 
                         '<metadata xmlns="http://www.georss.org/georss">\
<where>\
<Polygon xmlns="http://www.opengis.net/gml">\
<exterior xmlns="http://www.opengis.net/gml">\
<LinearRing xmlns="http://www.opengis.net/gml">\
<posList srsDimension="2" xmlns="http://www.opengis.net/gml">\
-71.1776585053 42.390290974 -71.1776585053 42.390290974 </posList>\
</LinearRing></exterior></Polygon></where></metadata>')
        
        root = createGEORSS()
        georss = \
            create_where_from_postgis('MULTIPOLYGON(\
            ((-71.1776585052917 42.3902909739571, -71.1776585052917 42.3902909739571)), \
            ((-71.1776585052917 42.3902909739571, -71.1776585052917 42.3902909739571)))', 
                                      root)
        root.append(georss)
        self.assertEqual(tostring(root), 
                         '<metadata xmlns="http://www.georss.org/georss">\
<where>\
<Polygon xmlns="http://www.opengis.net/gml">\
<exterior xmlns="http://www.opengis.net/gml">\
<LinearRing xmlns="http://www.opengis.net/gml">\
<posList srsDimension="2" xmlns="http://www.opengis.net/gml">\
-71.1776585053 42.390290974 -71.1776585053 42.390290974 \
</posList></LinearRing></exterior>\
</Polygon>\
<Polygon xmlns="http://www.opengis.net/gml">\
<exterior xmlns="http://www.opengis.net/gml">\
<LinearRing xmlns="http://www.opengis.net/gml">\
<posList srsDimension="2" xmlns="http://www.opengis.net/gml">\
-71.1776585053 42.390290974 -71.1776585053 42.390290974 \
</posList></LinearRing></exterior></Polygon></where></metadata>')        