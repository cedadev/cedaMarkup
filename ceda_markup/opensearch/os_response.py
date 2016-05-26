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
from ceda_markup.opensearch.constants import OS_ROOT_TAG, OS_NAMESPACE,\
    OS_PREFIX
from ceda_markup.markup import createSimpleMarkup, createMarkup
from ceda_markup.opensearch.helper import assign_prefix

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
OS_SYNDACATION_RIGHT = [
    SYNDACATION_OPEN,
    SYNDACATION_LIMITED,
    SYNDACATION_PRIVATE,
    SYNDACATION_CLOSED]
OS_SYNDACATION_RIGHT_DEFAULT = SYNDACATION_OPEN

OS_ADULT_CONTENT_DEFAULT = False
OS_INPUT_ENCODING_DEFAULT = 'UTF-8'
OS_OUTPUT_ENCODING_DEFAULT = 'UTF-8'


def createTotalResults(total_results, root=None, tagName=OS_ROOT_TAG,
                       ns=OS_NAMESPACE):
    tr = total_results
    if isinstance(total_results, int):
        tr = str(total_results)
    return createSimpleMarkup(tr, root, 'totalResults', ns, OS_PREFIX)


def createStartIndex(start_index, root=None, tagName=OS_ROOT_TAG,
                     ns=OS_NAMESPACE):
    tr = start_index
    if isinstance(start_index, int):
        tr = str(start_index)
    return createSimpleMarkup(tr, root, 'startIndex', ns, OS_PREFIX)


def createItemsPerPage(items_per_page, root=None, tagName=OS_ROOT_TAG,
                       ns=OS_NAMESPACE):
    tr = items_per_page
    if isinstance(items_per_page, int):
        tr = str(items_per_page)
    return createSimpleMarkup(tr, root, 'itemsPerPage', ns, OS_PREFIX)


def createOpenSearchRespose(root, totalResults=None, startIndex=None,
                            itemsPerPage=None, query=None, params_model=None):
    if totalResults is not None:
        markup = createTotalResults(totalResults, root)
        root.append(markup)

    if startIndex is not None:
        markup = createStartIndex(startIndex, root)
        root.append(markup)

    if itemsPerPage is not None:
        markup = createItemsPerPage(itemsPerPage, root)
        root.append(markup)

    markup = create_result_query(root, params_model, query)
    root.append(markup)


def create_result_query(root, params_model, query):
    '''
        Creates an XML element for the query.
        This is based on the search parameters that have been used. The root
        parameter is required in order to update the tag with the necessary
        namespaces
        @param root: the OpenSearchRequest.ROOT_TAG tag.
        @param params_model: a list of OSParam instances.
        @param query: an OSQuery instance.
        @return: a string describing the parameters query
    '''
    markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, root)
    markup.set("role", "request")
    for param in params_model:
        if param.par_name in query.attrib.keys():
            if param.namespace == OS_NAMESPACE:
                # these local parameter names are implicitly associated with
                # the OpenSearch 1.1 namespace
                term = param.term_name
            else:
                term = assign_prefix(root, param)
            markup.set(term, query.attrib[param.par_name])
    return markup
