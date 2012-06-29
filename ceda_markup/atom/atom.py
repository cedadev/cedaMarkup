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

Created on 6 May 2012

@author: Maurizio Nagni
'''
from xml.etree.ElementTree import Element, SubElement, _ElementInterface
from ceda_markup.markup import createMarkup

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
ATOM_PREFIX = 'atom'
ATOM_ROOT_TAG = 'feed'

def createDocument(iid, title, updated, subtitle = None, rights = None):
    top = createAtom()        
   
    ititle = SubElement(top, 'title')
    ititle.text = title
    
    iupdated = SubElement(top, 'updated')
    iupdated.text = updated              
    
    doc_id = SubElement(top, 'id')
    doc_id.text = iid
    
    if subtitle:
        subtitle = SubElement(top, 'subtitle')
        subtitle.text = subtitle
        
    if rights:
        rights = SubElement(top, 'rights')
        rights.text = rights            

    
    return top

def createAtom(root = None, tagName = ATOM_ROOT_TAG, ns = ATOM_NAMESPACE):      
    '''
        @param root: the root tag of the document containing this element
        @param tagName: the tagName 
        @param ns: the tag namespace       
    '''
    return createMarkup(tagName, ATOM_PREFIX, ns, root)

def createID(iid, root = None, ns = ATOM_NAMESPACE):      
    '''
        @param iid: a unique identifier, eventually an URI    
        @param root: the root tag of the document containing this element 
        @param ns: the tag namespace       
    '''
    markup = createMarkup('id', ATOM_PREFIX, ns, root)        
    markup.text = str(iid)    
    return markup

def createUpdated(updated, root = None, ns = ATOM_NAMESPACE):      
    '''
        @param updated: is a Date construct indicating the most
   recent instant in time when an entry or feed was modified in a way
   the publisher considers significant.
        @param root: the root tag of the document containing this element 
        @param ns: the tag namespace       
    '''
    markup = createMarkup('updated', ATOM_PREFIX, ns, root)        
    markup.text = str(updated)    
    return markup

def createPublished(published, root = None, ns = ATOM_NAMESPACE):      
    '''
        @param published: is a Date construct indicating an
   instant in time associated with an event early in the life cycle of
   the entry    
        @param root: the root tag of the document containing this element 
        @param ns: the tag namespace       
    '''
    markup = createMarkup('published', ATOM_PREFIX, ns, root)        
    markup.text = str(published)    
    return markup

ATOM_LINK_REL_SELF = 'self'
ATOM_LINK_REL_FIRST = 'first'
ATOM_LINK_REL_LAST = 'last'
ATOM_LINK_REL_SEARCH = 'search'
ATOM_LINK_REL = [ATOM_LINK_REL_SELF, ATOM_LINK_REL_FIRST, ATOM_LINK_REL_LAST, ATOM_LINK_REL_SEARCH]
def createLink(iri, rel = None, itype = None, root = None, ns = ATOM_NAMESPACE):      
    '''
        @param iri: contains the link's IRI
        @param rel: a string like 'self', 'first', 'last', ... 
        @param itype: an advisory media type as 'application/atom+xml'       
        @param root: the root tag of the document containing this element 
        @param ns: the tag namespace       
    '''
    markup = createMarkup('link', ATOM_PREFIX, ns, root)
    markup.set('href', iri)
    if rel is not None:
        markup.set('rel', rel)            
    if itype is not None:
        markup.set('type', itype)        
    return markup