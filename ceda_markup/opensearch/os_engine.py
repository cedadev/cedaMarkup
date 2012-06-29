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

import mimetypes
from query import QueryTag
from os_engine_helper import OSEngineHelper

if not mimetypes.inited:
    mimetypes.init()
    if not mimetypes.types_map.has_key('.atom'):
        mimetypes.add_type('application/atom+xml', '.atom')
    if not mimetypes.types_map.has_key('.opensearchdescription'):        
        mimetypes.add_type('application/opensearchdescription+xml', '.opensearchdescription')

def get_mimetype(extension):
    return mimetypes.types_map[('.%s') % (extension)]  

class OSEngine(object):
    '''
    classdocs
    '''

    def __init__(self, osRequest, osEngineHelper = OSEngineHelper()):
        '''
        Constructor
            @param osRequest: an OSREquest instance 
            @param ospath: the URL where the OpenSearch service is hosted
            @param osEngineHelper: 
        '''
        self.osRequest = osRequest
        self.osEngineHelper = osEngineHelper
        self.osHostURL = 'http://localhost'             
        
    def doSearch(self, hostURL, mimetype, params_values, **kwargs):
        self.osHostURL = hostURL
        response = None
        for item in self.osRequest.responses:
            if item.extension == mimetype:
                response = item
        if response:
            kwargs['params_values'] = params_values
            queries = QueryTag.queryWithRoleRequest(mimetype, self.osRequest.query.params_model, params_values)
            results = self.osRequest.query.doSearch(**kwargs)
            return response.generateResponse(results, [queries], self.osHostURL, **kwargs)
        return None                
    
    def getDescription(self, ospath):
        reqDoc = self.osRequest.getDescription(ospath)
        self.osEngineHelper.additionalDescription(reqDoc)
        return reqDoc
