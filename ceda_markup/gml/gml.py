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
from ceda_markup.markup import createMarkup

GML_NAMESPACE = 'http://www.opengis.net/gml'
GML_PREFIX = 'gml'
GML_ROOT_TAG = 'metadata'

def createGML(root = None, tagName = GML_ROOT_TAG, ns = GML_NAMESPACE):      
    '''
        @param root: the root tag of the document containing this element
        @param tagName: the tagName 
        @param ns: the tag namespace       
    '''
    return createMarkup(tagName, GML_PREFIX, ns, root)

def createPosList(root = None, ns = GML_NAMESPACE, values = [], 
                  srsDimension = None):      
    """
        Creates a GML.Envelope tag
        **Parameters**
            * root: the root tag of the document containing this element
            * ns: the tag namespace
            * values: a list of xsd:double 
            * srsDimension: xsd:positiveInteger              
    """  
    markup = createMarkup('posList', GML_PREFIX, ns, root)
    if srsDimension is not None:  
        markup.set('srsDimension', srsDimension)
    if values is not None:
        markup.text = "".join(["%s " % el for el in values])
    return markup

def createLinearRing(root = None, ns = GML_NAMESPACE, body = None):      
    '''
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param body: an instance of GML.PosList
    '''
    markup = createMarkup('LinearRing', GML_PREFIX, ns, root)
    if body is not None:
        markup.append(body)   
    return markup        

def createExterior(root = None, ns = GML_NAMESPACE, body = None):      
    '''
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param body: an instance of GML.LinerRing
    '''
    markup = createMarkup('exterior', GML_PREFIX, ns, root)
    if body is not None:
        markup.append(body)   
    return markup        

def createPolygon(root = None, ns = GML_NAMESPACE, body = None):      
    '''
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param body: an instance of GML.Exterior
    '''
    markup = createMarkup('Polygon', GML_PREFIX, ns, root)
    if body is not None:
        markup.append(body)
    return markup        

def createEnvelope(lowerCorner, upperCorner, 
                   root = None, ns = GML_NAMESPACE):
    """
        Creates a GML.Envelope tag
        **Parameters**
            * lowerCorner: a GML.LowerCorner instance 
            * upperCorner: a GML.UpperCorner instance
            * root: the root tag of the document containing this element
            * ns: the tag namespace 
    """  
    markup = createMarkup('Envelope', GML_PREFIX, ns, root)
    markup.append(lowerCorner)
    markup.append(upperCorner)
    return markup

def createLowerCorner(root = None, ns = GML_NAMESPACE, values = []):
    """
        Creates a GML.Envelope tag
        **Parameters**
            * root: the root tag of the document containing this element
            * ns: the tag namespace
            * values: a list of xsd:double
    """  
    markup = createMarkup('lowerCorner', GML_PREFIX, ns, root)
    if values is not None:
        markup.text = "".join(["%s " % el for el in values])
    return markup
     
def createUpperCorner(root = None, ns = GML_NAMESPACE, values = []):
    """
        Creates a GML.Envelope tag
        **Parameters**
            * root: the root tag of the document containing this element
            * ns: the tag namespace
            * values: a list of xsd:double
    """  
    markup = createMarkup('upperCorner', GML_PREFIX, ns, root)
    if values is not None:
        markup.text = "".join(["%s " % el for el in values])
    return markup     
     
def createValidTime(root = None, ns = GML_NAMESPACE, body = None):      
    '''
        @param root: the root tag of the document containing this element        
        @param ns: the tag namespace 
        @param body: an instance of GML.TimePeriod        
    '''
    markup = createMarkup('validTime', GML_PREFIX, ns, root)
    if body is not None:
        markup.append(body)
    return markup        

def createTimePeriod(root = None, ns = GML_NAMESPACE, begin = None, end = None):      
    '''
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param begin: an instance of GML.BeginPosition 
        @param end: an instance of GML.EndPosition 
    '''
    markup = createMarkup('TimePeriod', GML_PREFIX, ns, root)
    if begin is not None:
        markup.append(begin)
    if end is not None:
        markup.append(end) 
    return markup        
        
def _createTimePositionType(itype, root = None, ns = GML_NAMESPACE, body = None):      
    '''
        @param itype: 'beginPosition' or endPosition    
        @param root: the root tag of the document containing this element 
        @param ns: the tag namespace        
        @param body: an instance of GML.TimePeriod        
    '''
    markup = createMarkup(itype, GML_PREFIX, ns, root)
    if body is not None:
        markup.append(body)
    return markup        

def createBeginPosition(root = None, ns = GML_NAMESPACE, body = None):      
    '''    
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param body: a string
    '''
    markup = createMarkup('beginPosition', GML_PREFIX, ns, root)
    if body is not None:
        markup.text = body
    return markup        
    
def createEndPosition(root = None, ns = GML_NAMESPACE, body = None):      
    '''    
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace 
        @param body: a string
    '''
    markup = createMarkup('endPosition', GML_PREFIX, ns, root)
    if body is not None:
        markup.text = body   
    return markup         