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

Created on 24 May 2012

@author: Maurizio Nagni
'''


from xml.dom import minidom
from xml.etree.ElementTree import tostring

from ceda_markup.opensearch.constants import DESCRIPTION_FILE_NAME
from ceda_markup.opensearch.os_engine_helper import OSEngineHelper
from ceda_markup.opensearch.query import create_query


class OSEngine(object):
    """
    - :ref:`OSQuery <ceda_markup.opensearch.osquery.OSQuery>` **os_query**
        an OSQuery instance
    - :ref:`OSEngineResponse <ceda_markup.opensearch.template.osresponse.OSEngineResponse>` **os_responses**
        a list of OSEngineResponse instances
    - :ref:`OpenSearchDescription <ceda_markup.opensearch.os_description.OpenSearchDescription>` **os_description**
        an OpenSearchDescription instance
    - string **ospath**
        the URL where the OpenSearch service is hosted
    - :ref:`OSEngineHelper <ceda_markup.opensearch.os_engine_helper.OSEngineHelper>` **os_engine_helper**
        to write
    """

    def __init__(self, os_query, os_responses, os_description,
                 os_engine_helper=None, os_file_name=None):

        self.os_query = os_query
        self.os_responses = os_responses
        self.os_description = os_description
        self.os_engine_helper = os_engine_helper
        if os_engine_helper is None:
            self.os_engine_helper = OSEngineHelper()
        self.os_host_url = 'http://localhost'
        if os_file_name is not None:
            self.os_file_name = os_file_name
        else:
            self.os_file_name = DESCRIPTION_FILE_NAME

    def do_search(self, host_url, mimetype, context):
        """
        Executes the Opensearch call.
        Returns a response in the required mimetype or None if the mimetype is
        not supported

        - string **os_host_url**
            the opensearch engine URL
        - string **mimetype**
            the desired mimetype output
        - dict **context**
            a dictionary containing all the necessary information to exploit
            the request
        """
        self.os_host_url = host_url
        response = None
        for item in self.os_responses:
            if item.extension == mimetype:
                response = item
        if response is not None:
            xml_query = create_query(
                mimetype, self.os_query.params_model, context)
            result = self.os_query.do_search(xml_query, context)
            packaged_results = response.digest_search_results(result, context)
            return response.generate_response(packaged_results, xml_query,
                                              self.os_host_url,
                                              self.os_query.params_model,
                                              context, self.os_description)
        return None

    def get_description(self, host_url):
        """
        Returns a string representation of the Open Search description document.
        <http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_description_document>

        - string host_url
            The engine host URL.
        """
        markup = self.os_description.get_xml_markup(
            self.os_responses, self.os_query, host_url)
        self.os_engine_helper.additional_description(markup)
        reparsed = minidom.parseString(tostring(markup))
        return reparsed.toprettyxml(indent="  ")

    def create_query_dictionary(self):
        '''
        Returns a dictionary having as keys the query parameters. Default
        values are set from the params.models. This method is supposed to be
        used as utility to migrate the request parameters from the http request
        to an internal neutral (not any django QueryDict) dictionary.
        '''
        ret = {}
        for param in self.os_query.params_model:
            if param.default:
                ret[param.par_name] = param.default
            else:
                ret[param.par_name] = None
        return ret
