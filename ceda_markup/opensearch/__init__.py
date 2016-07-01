'''
@package: opensearch
The Open Search package provides Open Search methods.

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
'''

import math

from ceda_markup.opensearch.constants import OS_PREFIX, OS_NAMESPACE
from ceda_markup.opensearch.os_description import OpenSearchDescription
from ceda_markup.opensearch.os_param import OSParam
from ceda_markup.opensearch.osquery import OSQuery
from ceda_markup.opensearch.template.atom import OSAtomResponse
from ceda_markup.opensearch.template.json_response import OSJsonResponse
from ceda_markup.opensearch.template.osresponse import Person, Result


COUNT_DEFAULT = 10
START_INDEX_DEFAULT = 1
START_PAGE_DEFAULT = 1


__all__ = ['OSAtomResponse', 'OSJsonResponse', 'OSParam', 'OSQuery',
           'OpenSearchDescription', 'Person', 'Result', 'OS_PREFIX',
           'OS_NAMESPACE', 'filter_results']


def filter_results(results, count=COUNT_DEFAULT,
                   start_index=START_INDEX_DEFAULT,
                   start_page=START_PAGE_DEFAULT):
    """
        Returns the opensearch results list according to the
        'count', 'startIndex', 'startPage' parameters.

        @param results: an instance or a list of instances to be displayed in
                        the opensearch response
        @param count: the number of search results per page desired by
                        the search client
        @param start_index: the index of the first search result desired
                        by the search client
        @param startPage: the page number of the set of search results
                        desired by the search client

        @return: the selected results or None if the results is None
                        or is not a list or is an empty list
    """
    if results is None:
        return []
    elif isinstance(results, list) and len(results) == 0:
        return []
    elif not isinstance(results, list):
        _results = [results]
    else:
        _results = results

    tot_res = len(_results)

    if count is not None and count > 0:
        int_count = count
    else:
        int_count = COUNT_DEFAULT

    if start_index is not None and start_index > 1 and start_index <= tot_res:
        int_start_index = start_index
    else:
        int_start_index = START_INDEX_DEFAULT

    if start_page is not None \
            and math.ceil((tot_res - int_start_index + 1) / float(int_count)) \
            >= start_page:
        int_start_page = start_page
    else:
        int_start_page = START_PAGE_DEFAULT

    first_result = int_start_index - 1
    last_result = first_result + int_count

    if int_start_page > 1 \
            and first_result + (int_start_page - 1) * int_count <= tot_res:
        first_result = first_result + (int_start_page - 1) * int_count

    if first_result + int_count <= tot_res:
        last_result = first_result + int_count
    else:
        last_result = tot_res

    return _results[first_result:last_result]
