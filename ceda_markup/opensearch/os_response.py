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
from xml.etree.ElementTree import SubElement, Element

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

class OpenSearchResponse(object):
    '''
    classdocs
    '''

    NAMESPACE = 'http://a9.com/-/spec/opensearch/1.1/'
    PREFIX = 'os'
    ROOT_TAG = 'OpenSearchDescription'

    def __init__(self, root = None):               
        '''
            Constructor
        '''
        self._hasns = False
        self._root = root
        if self._root is not None:
            self._root.set("xmlns:%s" % (OpenSearchResponse.PREFIX), OpenSearchResponse.NAMESPACE)
            self._hasns = True
        else:
            self._root = Element(OpenSearchResponse.ROOT_TAG)
            self._root.set("xmlns", OpenSearchResponse.NAMESPACE)        

    @classmethod
    def assignPrefix(self, tag, is_response = True):
        if is_response:
            return "%s:%s" % (OpenSearchResponse.PREFIX, tag)
        else:
            return tag
        
    def createDocument(self, totalResults = None, startIndex = None, itemsPerPage = None, query = None):        
        if totalResults is not None:
            os_totalResults =  SubElement(self._root, OpenSearchResponse.assignPrefix('totalResults'))
            os_totalResults.text = totalResults
        
        if startIndex is not None:
            os_startIndex =  SubElement(self._root, OpenSearchResponse.assignPrefix('startIndex'))
            os_startIndex.text = startIndex

        if itemsPerPage is not None:
            os_itemsPerPage =  SubElement(self._root, OpenSearchResponse.assignPrefix('itemsPerPage'))
            os_itemsPerPage.text = itemsPerPage               
        '''
        Constructor
        '''            