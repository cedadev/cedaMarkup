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


from os_engine_helper import OSEngineHelper
from ceda_markup.opensearch.query import createQuery
from ceda_markup.opensearch.os_request import createOSDescription
from xml.etree.ElementTree import tostring
from xml.dom import minidom

  

class OSEngine(object):
    '''
    classdocs
    '''

    def __init__(self, query, osEnResponses, osDescription, osEngineHelper = OSEngineHelper()):
        '''
        Constructor
            @param osQuery: an OSQuery instance 
            @param osResponses: a list of OSEngineResponse instances
            @param osDescription: an OpenSearchDescription instance                        
            @param ospath: the URL where the OpenSearch service is hosted
            @param osEngineHelper: 
        '''
        self.osQuery = query
        self.osEnResponses = osEnResponses
        self.osDescription = osDescription        
        self.osEngineHelper = osEngineHelper
        self.osHostURL = 'http://localhost'             
        
    def doSearch(self, hostURL, mimetype, context):
        """
            Executes the Opensearch call.
            @param hostURL: the opensearch engine URL
            @param mimetype: the desired mimetype output
            @param context: a dictionary containing all the necessary information to exploit the request
            @return: a response in the required mimetype or None if the mimetype is not supported   
        """
        self.osHostURL = hostURL
        response = None
        for item in self.osEnResponses:
            if item.extension == mimetype:
                response = item
        if response is not None:
            queries = createQuery(mimetype, self.osQuery.params_model, context)
            result = self.osQuery.doSearch(context)
            packagedResults = response.digestSearchResults(result, context)
            return response.generateResponse(packagedResults, [queries], self.osHostURL, context)
        return None              
    
    def getDescription(self, ospath):
        reqDoc = createOSDescription(self.osEnResponses, self.osDescription, self.osQuery, ospath)
        self.osEngineHelper.additionalDescription(reqDoc)
        reparsed = minidom.parseString(tostring(reqDoc))
        return reparsed.toprettyxml(indent="  ")

    def createQueryDictionary(self):
        '''
            Returns a dictionary having as keys the query parameters. This method is 
            supposed to be used as utility to migrate the request parameters from the 
            http request to an internal neutral (not any django QueryDict) dictionary.
            @return: a dictionary
        '''        
        ret = {}
        for param in self.osQuery.params_model:
            ret[param.par_name] = None
        return ret 
