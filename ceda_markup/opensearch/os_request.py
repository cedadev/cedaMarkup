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
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from os_engine import get_mimetype
from osquery import URL_REL_DEFAULT, URL_INDEX_OFFSET_DEFAULT,\
    URL_PAGE_OFFSET_DEFAULT

MAX_OS_SHORT_NAME_LEN = 16
MAX_OS_LONG_NAME_LEN = 48
MAX_OS_TAGS_LEN = 256
MAX_OS_DESCRIPTION_LEN = 1024
MAX_OS_DEVELOPER_LEN = 64
MAX_OS_ATTRIBUTION_LEN = 256

SYNDACATION_OPEN = 'open'
SYNDACATION_LIMITED = 'limited'
SYNDACATION_PRIVATE = 'private'
SYNDACATION_CLOSED = 'closed'
OS_SYNDACATION_RIGHT = [SYNDACATION_OPEN, SYNDACATION_LIMITED, SYNDACATION_PRIVATE, SYNDACATION_CLOSED]
OS_SYNDACATION_RIGHT_DEFAULT = SYNDACATION_OPEN

OS_ADULT_CONTENT_DEFAULT = False
OS_INPUT_ENCODING_DEFAULT = 'UTF-8'
OS_OUTPUT_ENCODING_DEFAULT = 'UTF-8' 

class OpenSearchRequest(object):
    '''
    classdocs
    '''

    NAMESPACE = 'http://a9.com/-/spec/opensearch/1.1/'
    PREFIX = ''
    ROOT_TAG = 'OpenSearchDescription'

    def __init__(self, query, responses, os_short_name, os_description, \
                 os_contact = None, os_tags = None, os_long_name = None, \
                 os_image = [], os_developer = None, os_attribution = None, \
                 os_syndacation_right = None, os_adult_content = None, \
                 os_language = ['*'], os_input_encoding = [OS_INPUT_ENCODING_DEFAULT], \
                 os_output_encoding = [OS_OUTPUT_ENCODING_DEFAULT]):
        '''
            @param query: an OSQuery implementation 
            @param responses: a list of OSResponse instances            
            @param oshelper: a list of OSResponse implementations 
        '''
        self.query = query
        self.responses = responses
        self.os_syndacation_right = None
        
        # should be set to True but because of 
        # http://code.google.com/p/gdata-python-client/issues/detail?id=611
        # we cannot (for now)
        self.os_adult_content = '1'

        if os_description is not None:
            self.os_description = os_description[:MAX_OS_DESCRIPTION_LEN]
        
        if os_short_name is not None:
            self.os_short_name = os_short_name[:MAX_OS_SHORT_NAME_LEN]
                    
        #Should check that is an email format
        if os_contact is not None:        
            self.os_contact = os_contact
         
        if os_tags is not None:
            self.os_tags = os_tags[:MAX_OS_TAGS_LEN]

        if os_long_name is not None:
            self.os_long_name = os_long_name[:MAX_OS_LONG_NAME_LEN]

        if os_developer is not None:
            self.os_developer = os_developer[:MAX_OS_DEVELOPER_LEN]

        if os_attribution is not None:
            self.os_attribution = os_attribution[:MAX_OS_ATTRIBUTION_LEN]            
            
        if os_syndacation_right and os_syndacation_right in OS_SYNDACATION_RIGHT:
            self.os_syndacation_right = os_syndacation_right            
            
        if os_adult_content  is not None and os_adult_content in ['false', 'FALSE', '0', 'no', 'NO']:
            # should be set to False but because of 
            # http://code.google.com/p/gdata-python-client/issues/detail?id=611
            # we cannot (for now)            
            self.os_adult_content = '0'                        
            
        self.os_image = os_image
        self.os_language = os_language
        self.os_input_encoding = os_input_encoding        
        self.os_output_encoding = os_output_encoding         
        
    def getDescription(self, ospath):
        top = Element(OpenSearchRequest.ROOT_TAG)
        top.set("xmlns", OpenSearchRequest.NAMESPACE)
       
        shortName = SubElement(top, 'ShortName')
        shortName.text = self.os_short_name
        
        description = SubElement(top, 'Description')
        description.text = self.os_description
        
        if hasattr(self, 'os_tags'):
            tags = SubElement(top, 'Tags')
            tags.text = self.os_tags
        
        if hasattr(self, 'os_contact'):
            contact = SubElement(top, 'Contact')
            contact.text = self.os_contact
            
        if hasattr(self, 'os_long_name'):
            long_name = SubElement(top, 'LongName')
            long_name.text = self.os_long_name         
            
        if hasattr(self, 'os_developer'):
            developer = SubElement(top, 'Developer')
            developer.text = self.os_developer            
            
        if hasattr(self, 'os_attribution'):
            attribution = SubElement(top, 'Attribution')
            attribution.text = self.os_attribution            
        
        if hasattr(self, 'os_image') and isinstance(self.os_image, list):
            for img in self.os_image:
                top.append(img.buildElement())            
        
        if hasattr(self, 'os_syndacation_right') and self.os_syndacation_right != OS_SYNDACATION_RIGHT_DEFAULT:
            syndacation_right = SubElement(top, 'SyndacationRight')
            syndacation_right.text = self.syndacation_right       
        
        if hasattr(self, 'os_adult_content'):
            adult_content = SubElement(top, 'AdultContent')
            adult_content.text = self.adult_content               
        
        if self.os_language and isinstance(self.os_language, list):
            for item in self.os_language:
                language = SubElement(top, 'Language')
                language.text = item        
        
        if self.os_input_encoding and isinstance(self.os_input_encoding, list):
            for item in self.os_input_encoding:
                ie = SubElement(top, 'InputEncoding')
                ie.text = item     
        
        if self.os_output_encoding and isinstance(self.os_output_encoding, list):
            for item in self.os_output_encoding:
                ie = SubElement(top, 'OuputEncoding')
                ie.text = item             
        
        for item in self.responses:            
            self._buildTemplateURL(top, item.extension, self.query.rel, self.query.indexOffset, self.query.pageOffset, ospath)
        
        reparsed = minidom.parseString(tostring(top))
        return reparsed.toprettyxml(indent="  ")

    def _assignPrefix(self, root, param):
        if param.namespace is None:
            return param.term_name
        
        for k,v in root.items():
            if v == param.namespace:
                return ("%s:%s") % (k[6:], param.term_name)
        
        index = 0
        while True:
            if "xmlns:a%d" % (index) not in root.keys():                
                break 
            index = index + 1
            
        root.set("xmlns:a%d" % (index), param.namespace)
        return ("a%d:%s") % (index, param.term_name)

    def _buildTemplateURL(self, root, response_type, rel, indexOffset, pageOffset, ospath):
        url = Element("Url")
        url.set("type", get_mimetype(response_type))
        
        template_query = self.query.createTemplateQuery(root)
           
        query_template = ("%s%s?%s") % (ospath, response_type, template_query[:-1])
        url.set("template", query_template)
        
        if rel  is not None and rel != URL_REL_DEFAULT:
            url.set("rel", rel)
        
        if indexOffset  is not None and indexOffset != URL_INDEX_OFFSET_DEFAULT:            
            url.set("indexOffset", str(indexOffset))
        
        if pageOffset  is not None and pageOffset != URL_PAGE_OFFSET_DEFAULT:                    
            url.set("pageOffset", str(pageOffset))        
        
        root.append(url) 