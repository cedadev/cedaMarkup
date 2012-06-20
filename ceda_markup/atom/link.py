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

Created on 22 May 2012

@author: Maurizio Nagni
'''
from xml.etree.ElementTree import Element

class Link(object):
    '''
    classdocs
    '''

    REL_ALTERNATE = 'alternate'
    REL_ENCLOSURE = 'enclosure'    
    REL_RELATED = 'related'    
    REL_SELF = 'self'    
    REL_VIA = 'via'    
    REL_SEARCH = 'search'
    REL_FIRST = 'first'    
    REL_NEXT = 'next'    
    REL_LAST = 'last'    
    REL = [REL_ALTERNATE, REL_ENCLOSURE, REL_RELATED, REL_SELF, REL_VIA, REL_SEARCH, REL_FIRST, REL_NEXT, REL_LAST]    
    

    def __init__(self, href, rel = None, type = None, hreflang = None, title = None, length = None):
        '''
        Constructor
        @param root: the document root element where attach the prefix:namespace for this element 
        @param href: 
        @param rel: one of the Link.REL constants
        @param type: 
        @param hreflang:
        @param title: an atom.Title instance
        @param length: length of the resource in bytes    
        '''
        self.href = href
        
        if rel and rel in Link.REL:
            self.rel = rel
            
        if type:
            self.type = type            
        
        if hreflang:
            self.hreflang = hreflang        
            
        if title:
            self.title = title            
        
        if length:
            self.length = length    
            
    def buildElement(self):
        link = Element("link")        
        link.set('href', self.href)
                
        if hasattr(self, 'rel'):
            link.set('rel', self.rel)            
        
        if hasattr(self, 'type'):
            link.set('type', self.type)

        if hasattr(self, 'hreflang'):
            link.set('hreflang', self.hreflang)
            
        if hasattr(self, 'title'):
            link.set('title', self.title)

        if hasattr(self, 'length'):
            link.set('length', self.length)                        

        return link                