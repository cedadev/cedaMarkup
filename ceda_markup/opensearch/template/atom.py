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

Created on 5 May 2012

@author: Maurizio Nagni
'''
from abc import abstractmethod
from xml.dom import minidom
from xml.etree.ElementTree import tostring

from ceda_markup.atom import REL_SELF, REL_FIRST, REL_NEXT,\
    REL_LAST, REL_PREV
from ceda_markup.atom.atom import createAtomDocument, ATOM_NAMESPACE, \
    ATOM_PREFIX, create_autodiscovery_link
from ceda_markup.opensearch.os_response import createOpenSearchRespose
from ceda_markup.opensearch.template.osresponse import OSEngineResponse


class OSAtomResponse(OSEngineResponse):
    '''
    classdocs
    '''

    def __init__(self):
        '''
            Constructor
        '''
        # type = "application/atom+xml"
        super(OSAtomResponse, self).__init__('atom')

    @abstractmethod
    def generate_entries(self, atomroot, subresults):
        """
        An implementation of this method should construct an XML element
        containing the subresults.

        @param atomroot (ElementTree.Element): the root tag of the document
                containing this element
        @param subresults (list): a list of results

        @return an ElementTree.Element  containing the atom entries

        """
        pass

    @abstractmethod
    def generate_url(self, os_host_url, context):
        """
        Returns the URL used to assemble the OSResponse links.

        @param os_host_url (str): the URL of the opensearch host
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.

        @return a URL including path

        """
        pass

    def generate_response(self, results, query, os_host_url,
                          params_model, context, os_description):
        url = self.generate_url(os_host_url, context)
        if not url.endswith('/'):
            url = '%s/' % url

        # Generates the ATOM document
        atomdoc = createAtomDocument(url + "atom", results.title,
                                     results.updated,
                                     subtitle=results.subtitle)

        # Generate description link
        atomdoc.append(os_description.get_xml_autodiscovery_link
                       (os_host_url, ATOM_PREFIX, ATOM_NAMESPACE, atomdoc))

        # Generate feed's links
        self._generate_feed_links(atomdoc, url, results,
                                  params_model, context)

        # Inserts the OpenSearchResponse elements
        createOpenSearchRespose(atomdoc, results.total_result,
                                results.start_index, results.count, query,
                                params_model)

        self.generate_entries(atomdoc, results.subresult)

        xml = ('<?xml version="1.0" encoding="utf-8"?>%s' %
               tostring(atomdoc, encoding='unicode'))

        reparsed = minidom.parseString(xml)
        return reparsed.toprettyxml()

    def _generate_feed_links(self, atomroot, path, result,
                             params_model, context):
        '''
        Appends a number of atom <links> tags
        '''
        atomroot.append(create_autodiscovery_link
                        (atomroot, path, params_model, context, self.extension,
                         rel=REL_SELF, start_index=result.start_index))
        atomroot.append(create_autodiscovery_link
                        (atomroot, path, params_model, context, self.extension,
                         rel=REL_FIRST, start_index=1))

        if result.total_result >= result.start_index + result.count:
            atomroot.append(create_autodiscovery_link
                            (atomroot, path, params_model, context,
                             self.extension, rel=REL_NEXT,
                             start_index=result.start_index + result.count))
        else:
            atomroot.append(create_autodiscovery_link
                            (atomroot, path, params_model, context,
                             self.extension, rel=REL_NEXT,
                             start_index=result.start_index))

        if result.start_index - result.count > 0:
            atomroot.append(create_autodiscovery_link
                            (atomroot, path, params_model, context,
                             self.extension, rel=REL_PREV,
                             start_index=result.start_index - result.count))
        else:
            atomroot.append(create_autodiscovery_link
                            (atomroot, path, params_model, context,
                             self.extension, rel=REL_PREV, start_index=1))

        last_index = (result.total_result - result.start_index) % result.count
        atomroot.append(create_autodiscovery_link
                        (atomroot, path, params_model, context, self.extension,
                         rel=REL_LAST,
                         start_index=result.total_result - last_index))
