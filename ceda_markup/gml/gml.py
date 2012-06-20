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

Created on 24 May 2012

@author: Maurizio Nagni
'''
from xml.etree.ElementTree import Element

class GML(object):
    '''
    classdocs
    '''

    NAMESPACE = 'http://www.opengis.net/gml'
    PREFIX = 'gml'
    ROOT_TAG = 'metadata'

    def __init__(self, root = None):               
        '''
            Constructor
        '''
        self._hasns = False
        self._root = root
        if self._root is not None:
            self._hasns = True
        else:
            self._root = Element(GML.ROOT_TAG)
            
        self._root.set("xmlns:%s" % (GML.PREFIX), GML.NAMESPACE)        

class Polygon(GML):
    '''
    classdocs
    '''

    def __init__(self, root, body):
        '''
        Constructor
        @param root: the document root element where attach the prefix:namespace for this element 
        @param body: an instance of GML.Exterior 
        '''
        self.body = body
        super(Polygon, self).__init__(root)
    
    def buildElement(self):
        polygon =  Element("%s:%s" % (GML.PREFIX, 'Polygon'))
        polygon.append(self.body.buildElement())
        return polygon
    
class Exterior(GML):
    '''
    classdocs
    '''

    def __init__(self, root, body):
        '''
        Constructor
        @param root: the document root element where attach the prefix:namespace for this element 
        @param body: an instance of GML.LinerRing 
        '''
        self.body = body
        super(Exterior, self).__init__(root)
    
    def buildElement(self):
        exterior =  Element("%s:%s" % (GML.PREFIX, 'exterior'))
        exterior.append(self.body.buildElement())
        return exterior
    
class LinearRing(GML):
    '''
    classdocs
    '''

    def __init__(self, root, body):
        '''
        Constructor
        @param root: the document root element where attach the prefix:namespace for this element 
        @param body: an instance of GML.PosList 
        '''
        self.body = body
        super(LinearRing, self).__init__(root)
    
    def buildElement(self):
        linearRing =  Element("%s:%s" % (GML.PREFIX, 'LinearRing'))
        linearRing.append(self.body.buildElement())
        return linearRing
    
class PosList(GML):
    '''
    classdocs
    '''

    def __init__(self, root, body, srsDimension = None):
        '''
        Constructor
        @param root: the document root element where attach the prefix:namespace for this element 
        @param body: a string like '45.256 -110.45 46.46 -109.48 43.84 -109.86 45.256 -110.45'
        @param srsDimension: a number
        '''
        self.body = body
        self.srsDimension = srsDimension
        super(PosList, self).__init__(root)
    
    def buildElement(self):
        posList =  Element("%s:%s" % (GML.PREFIX, 'posList'))
        posList.set('srsDimension', self.srsDimension)
        posList.text = self.body
        return posList             