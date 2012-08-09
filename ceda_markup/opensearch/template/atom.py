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

Created on 5 May 2012

@author: Maurizio Nagni
'''
from ceda_markup.opensearch.template.osresponse import OSEngineResponse
from ceda_markup.opensearch import create_autodiscovery_link,\
    generate_autodiscovery_path
from ceda_markup.atom.link import REL_SEARCH, REL_SELF, REL_FIRST, REL_NEXT,\
    REL_LAST
from ceda_markup.atom.atom import createAtomDocument
from ceda_markup.opensearch.os_response import createOpenSearchRespose
from xml.dom import minidom
from xml.etree.ElementTree import tostring
from abc import abstractmethod

class OSAtomResponse(OSEngineResponse):
    '''
    classdocs
    '''

    def __init__(self):
        '''
            Constructor
        '''
        #type = "application/atom+xml"               
        super(OSAtomResponse, self).__init__('atom')


    def generate_response(self, results, queries, osHostURL, context):
        ospath = generate_autodiscovery_path(osHostURL, None, self.extension, rel = None)
        
        #Generates the ATOM document
        atomdoc = createAtomDocument(ospath + "atom", results.title, results.updated)

        #Generate feed's links
        self._generate_feed_links(atomdoc, ospath, results)
        
        #Inserts the OpenSearchResponse elements
        createOpenSearchRespose(atomdoc, results.totalResult, results.startIndex, results.count, queries)
        
        self.generateEntries(atomdoc, results.subresult, ospath)
        
        reparsed = minidom.parseString(tostring(atomdoc))
        return reparsed.toprettyxml(indent="  ")
    
    @abstractmethod
    def generate_entries(self, atomroot, subresults, path):
        pass
    
        
    def _generate_feed_links(self, atomroot, path, result, linkid = None):
        '''
        Appends a number of atom <links> tags  
        '''
        atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                linkid, start_index = None, rel = REL_SEARCH))        
        atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                linkid, start_index = result.startIndex, \
                                                rel = REL_SELF))        
        atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                linkid, \
                                                start_index = 1, rel = REL_FIRST))
        
        if result.totalResult > result.startIndex + result.count:
            atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                    linkid, \
                                                    start_index = result.startIndex + result.count, \
                                                    rel = REL_NEXT))     
        else:
            atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                    linkid, \
                                                    start_index = result.startIndex, \
                                                    rel = REL_NEXT))
            
        last_index = (result.totalResult -  result.startIndex) % result.count
        atomroot.append(create_autodiscovery_link(atomroot, path, self.extension, \
                                                    linkid, \
                                                    start_index = result.totalResult - last_index, \
                                                    rel = REL_LAST))