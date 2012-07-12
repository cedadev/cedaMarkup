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
from osquery import URL_REL_DEFAULT, URL_INDEX_OFFSET_DEFAULT,\
    URL_PAGE_OFFSET_DEFAULT
from ceda_markup.markup import createMarkup, createSimpleMarkup
from ceda_markup.opensearch import createTemplateQuery
from ceda_markup import get_mimetype

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

OS_NAMESPACE = 'http://a9.com/-/spec/opensearch/1.1/'
OS_PREFIX = 'os'
OS_ROOT_TAG = 'OpenSearchDescription'

def createURL(query, response_type, ospath, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    markup = createMarkup('Url', OS_PREFIX, ns, root)    
    markup.set("type", get_mimetype(response_type))
    
    template_query = createTemplateQuery(root, query)
       
    query_template = ("%s%s?%s") % (ospath, response_type, template_query[:-1])
    markup.set("template", query_template)
    
    if query.rel is not None and query.rel != URL_REL_DEFAULT:
        markup.set("rel", query.rel)
    
    if query.indexOffset  is not None and query.indexOffset != URL_INDEX_OFFSET_DEFAULT:            
        markup.set("indexOffset", str(query.indexOffset))
    
    if query.pageOffset  is not None and query.pageOffset != URL_PAGE_OFFSET_DEFAULT:                    
        markup.set("pageOffset", str(query.pageOffset))        
    return markup

def createShortName(shortName, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(shortName, root, 'ShortName', ns, OS_PREFIX)

def createDescription(description, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(description, root, 'Description', ns, OS_PREFIX)

def createTags(tags, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(tags, root, 'Tags', ns, OS_PREFIX)    

def createContact(contact, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(contact, root, 'Contact', ns, OS_PREFIX)

def createLongName(longName, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(longName, root, 'LongName', ns, OS_PREFIX)    

def createDeveloper(developer, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(developer, root, 'Developer', ns, OS_PREFIX)

def createAttribution(attribution, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(attribution, root, 'Attribution', ns, OS_PREFIX)    

def createSyndacationRight(syndacation_right, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(syndacation_right, root, 'SyndacationRight', ns, OS_PREFIX)

def createAdultContent(adult_content, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(adult_content, root, 'AdultContent', ns, OS_PREFIX)

def createLanguage(language, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(language, root, 'Language', ns, OS_PREFIX)    

def createInputEncoding(inputEncoding, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(inputEncoding, root, 'InputEncoding', ns, OS_PREFIX)

def createOutputEncoding(outputEncoding, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    return createSimpleMarkup(outputEncoding, root, 'OutputEncoding', ns, OS_PREFIX)

def createImage(url, height = None, width = None, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    markup = createSimpleMarkup(url, root, 'Image', ns, OS_PREFIX)
    if height  is not None and isinstance(height, (int, long)):
        markup.set("height", height)            

    if width  is not None and isinstance(width, (int, long)):
        markup.set("width", width) 
    return markup
    

def createOSDescription(osResponses, os_description, query, ospath, root = None, tagName = OS_ROOT_TAG, ns = OS_NAMESPACE):
    """
        @param osResponses: a list of OSResponse instances
        @param os_description: an OpenSearchDescription instance
        @param query: an OSQuery instance        
    """
    markup = createMarkup(OS_ROOT_TAG, OS_PREFIX, ns, root)
    markup.append(createShortName(os_description.os_short_name, root = markup))
    markup.append(createDescription(os_description.os_description, root = markup))    

    if hasattr(os_description, 'os_tags'):
        markup.append(createTags(os_description.os_tags, root = markup))        

    if hasattr(os_description, 'os_contact'):
        markup.append(createContact(os_description.os_contact, root = markup))
    
    if hasattr(os_description, 'os_long_name'):
        markup.append(createLongName(os_description.os_long_name, root = markup))    

    if hasattr(os_description, 'os_developer'):
        markup.append(createDeveloper(os_description.os_developer, root = markup))        
         
    if hasattr(os_description, 'os_attribution'):
        markup.append(createAttribution(os_description.os_attribution, root = markup))         
    
    if hasattr(os_description, 'os_image') and isinstance(os_description.os_image, list):
        for img in os_description.os_image:
            markup.append(createImage(img.url, img.height, img.width, root = markup))           
    
    if hasattr(os_description, 'os_syndacation_right') and os_description.os_syndacation_right != OS_SYNDACATION_RIGHT_DEFAULT:
        markup.append(createSyndacationRight(os_description.os_syndacation_right, root = markup))        
    
    if hasattr(os_description, 'os_adult_content'):
        markup.append(createAdultContent(os_description.os_adult_content, root = markup))               
    
    if os_description.os_language and isinstance(os_description.os_language, list):        
        for item in os_description.os_language:
            markup.append(createLanguage(item, root = markup))

    
    if os_description.os_input_encoding and isinstance(os_description.os_input_encoding, list):
        for item in os_description.os_input_encoding:
            markup.append(createInputEncoding(item, root = markup))     
    
    if os_description.os_output_encoding and isinstance(os_description.os_output_encoding, list):
        for item in os_description.os_output_encoding:
            markup.append(createOutputEncoding(item, root = markup))
    
    for item in osResponses:                    
        url = createURL(query, item.extension, ospath, root = markup)
        markup.append(url)

    return markup

class OpenSearchDescription(object):
    '''
    classdocs
    '''

    def __init__(self, os_short_name, os_description, \
                 os_contact = None, os_tags = None, os_long_name = None, \
                 os_image = [], os_developer = None, os_attribution = None, \
                 os_syndacation_right = None, os_adult_content = None, \
                 os_language = ['*'], os_input_encoding = [OS_INPUT_ENCODING_DEFAULT], \
                 os_output_encoding = [OS_OUTPUT_ENCODING_DEFAULT]):
        
        """
        
            @param os_image: a list of osImage instances
        """
        
        
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