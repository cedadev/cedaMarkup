'''
BSD Licence Copyright (c) 2016, Science & Technology Facilities Council (STFC)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    * Neither the name of the Science & Technology Facilities Council (STFC)
    nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on 23 May 2016

@author: wilsona
'''

from abc import abstractmethod
import json

from ceda_markup.opensearch.template.osresponse import OSEngineResponse


# from json import dumps
class OSJsonResponse(OSEngineResponse):
    """"
    This class extends an OSEngineResponse class.

    Classes extending this class MUST implement the generate_rows method and
    the digest_search_results method from OSEngineResponse.
    """

    def __init__(self):
        """
        Constructor
        """
        super(OSJsonResponse, self).__init__('json')

    @abstractmethod
    def generate_rows(self, subresults):
        """
        An implementation of this method should construct a list containing the
        subresults.

        @param subresults (list): a list of results

        @return a list containing json serializable objects

        """
        pass

    def generate_response(self, results, query, os_host_url,
                          params_model, context, os_description):
        """
        Create a json object containing the results.

        Overrides abstract method from OSEngineResponse.


        @param results: an opensearch Result object
        @param query: an ElementTree.Element representing an OpenSearch.Query
                tag
        @param os_host_url: the URL of the opensearch host
        @param params_model: an OSQuery.params_model
        @param context: a dict with the param names as key and values from the
                request. May contain values of 'None'.
        @param os_description: an OpenSearchDescription object

        @return a json serialized object

        """

        jsondoc = {}
        jsondoc['totalResults'] = results.total_result
        jsondoc['startIndex'] = results.start_index

        subresults = self.generate_rows(results.subresult)
        if subresults:
            jsondoc['rows'] = subresults

        return json.dumps(jsondoc, indent=4, separators=(',', ': '))
