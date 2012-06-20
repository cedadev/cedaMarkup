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
from xml.etree.ElementTree import Element, SubElement

class Entry(object):
    '''
    classdocs
    '''


    def __init__(self, iid, title, updated, \
                 author = None, content = None, link = None, \
                 summary = None, category = None, contributor = None, \
                 published = None, source = None, rights = None):
        '''
            Constructor
            @param id: a unique identifier, eventually an URI
            @param title: an atom.Entry instance 
            @param updated: the last time the record was updated
            @param author: one or more atom.Author instances
            @param content: an atom.Content instance             
            @param link: one or more atom.Link instances
            @param summary: an atom.Summary instance                        
            @param category:             
            @param contributor: one or more atom.Contributor instances
            @param published:                         
            @param source: 
            @param rights: an atom.Rights instance                        
        '''
        self.id = iid
        self.title = title
        self.updated = updated        
        
        if author:
            self.author = author
        
        if content is not None:
            self.content = content
                    
        if link:
            self.link = link
            
        if summary:
            self.summary = summary
            
        if category:
            self.category = category
            
        if contributor:
            self.contributor = contributor                                    
                        
        if published:
            self.published = published
            
        if source:
            self.source = source                    
            
        if rights:
            self.rights = rights
                        
    def buildElement(self):
        entry = Element("entry")
        
        iid = SubElement(entry, 'id')
        iid.text = self.id
        
        title = SubElement(entry, 'title')
        title.text = self.title
        
        updated = SubElement(entry, 'updated')
        updated.text = self.updated
        
        if hasattr(self, 'author'):
            if isinstance(self.author, list):
                entry.extend(self.author)
            else:
                entry.append(self.author)
                
        if hasattr(self, 'contributor'):
            if isinstance(self.contributor, list):
                entry.extend(self.contributor)
            else:
                entry.append(self.contributor)                
                
        if hasattr(self, 'content'):
            entry.append(self.content)
            
        if hasattr(self, 'link'):
            link = SubElement(entry, 'link')
            link.text = self.link
            
        if hasattr(self, 'summary'):
            summary = SubElement(entry, 'summary')
            summary.text = self.summary

        if hasattr(self, 'category'):
            if isinstance(self.category, list):
                entry.extend(self.category)
            else:
                entry.append(self.category)
                                            
        if hasattr(self, 'published'):
            published = SubElement(entry, 'published')
            published.text = self.published             
            
        if hasattr(self, 'source'):
            source = SubElement(entry, 'source')
            source.text = self.source          
        
        return entry  