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

GEORSS_NAMESPACE = 'http://www.georss.org/georss'
GEORSS_PREFIX = 'georss'
GEORSS_ROOT_TAG = 'metadata'

def createGEORSS(root = None, tagName = GEORSS_ROOT_TAG, ns = GEORSS_NAMESPACE):      
    '''
        @param root: the root tag of the document containing this element
        @param tagName: the tagName 
        @param ns: the tag namespace       
    '''
    return createMarkup(tagName, GEORSS_PREFIX, ns, root)

def createWhere(root = None, body = None, ns = GEORSS_NAMESPACE):   
    """
        Creates a GEORSS.Where tag
        **Parameters**
            * root: the root tag of the document containing this element
            * body: one instance among GML.Envelope, GML.Polygon or [GML.Polygon]        
            * ns: the tag namespace              
    """
    where = createMarkup('where', GEORSS_PREFIX, ns, root)
    items = []
    if body is not None:
        if not isinstance(body, list):
            items.append(body)             
        else:
            items = body            
        for item in items:
            where.append(item)
    return where