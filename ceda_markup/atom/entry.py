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
from ceda_markup import extendElement
from ceda_markup.atom.atom import ATOM_NAMESPACE, ATOM_PREFIX
from ceda_markup.markup import createMarkup

def createEntry(iid, title, updated, \
                 author = None, content = None, link = None, \
                 published = None, root = None, 
                 ns = ATOM_NAMESPACE):      
        '''
            Constructor
            @param iid: an atom.ID instance
            @param title: an atom.Title instance 
            @param updated: an atom.Update instance
            @param author: one or more atom.Author instances
            @param content: an atom.Content instance             
            @param link: one or more atom.Link instances                                     
            @param published: an atom.Published instance                          
            @param root: the document root element where attach the prefix:namespace for this element                        
        '''
        markup = createMarkup('entry', ATOM_PREFIX, ns, root)        
        markup.append(iid)                
        markup.append(title)        
        markup.append(updated)
        
        if author:
            if isinstance(author, list):
                extendElement(markup, author)
            else:
                markup.append(author)               
                
        if content:
            markup.append(content)
            
        if link is not None:
            markup.append(link)
                                            
        if published:
            markup.append(published)               
              
        return markup
        
