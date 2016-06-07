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

Created on 4 May 2012

@author: Maurizio Nagni
'''
from abc import abstractmethod
from ceda_markup import get_mimetype
from ceda_markup.markup import createMarkup
from ceda_markup.opensearch.constants import OS_NAMESPACE, OS_PREFIX
from ceda_markup.opensearch.helper import assign_prefix


URL_REL_RESULTS = 'results'
URL_REL_SUGGESTIONS = 'suggestions'
URL_REL_SELF = 'self'
URL_REL_COLLECTIONS = 'collection'
URL_REL = [URL_REL_RESULTS, URL_REL_SUGGESTIONS,
           URL_REL_SELF, URL_REL_COLLECTIONS]

URL_REL_DEFAULT = URL_REL_RESULTS
URL_INDEX_OFFSET_DEFAULT = 1
URL_PAGE_OFFSET_DEFAULT = 1


class OSQuery(object):
    '''
    classdocs
    '''

    def __init__(self, params_model, rel=URL_REL_DEFAULT,
                 indexOffset=URL_INDEX_OFFSET_DEFAULT,
                 pageOffset=URL_PAGE_OFFSET_DEFAULT):
        """
            @param params_model: URL's params as OSParam instances array
            @param rel: URL's 'rel' attribute
            @param indexOffset: URL's 'indexOffset' attribute
            @param pageOffset: URL's 'pageOffset' attribute
        """
        self.params_model = params_model

        if rel is not None and rel in URL_REL:
            self.rel = rel
        else:
            self.rel = URL_REL_DEFAULT

        if (indexOffset is not None and
                isinstance(indexOffset, (int, int)) and indexOffset > 0):
            self.indexOffset = indexOffset
        else:
            self.indexOffset = URL_INDEX_OFFSET_DEFAULT

        if (pageOffset is not None and
                isinstance(pageOffset, (int, int)) and pageOffset > 0):
            self.pageOffset = pageOffset
        else:
            self.pageOffset = URL_PAGE_OFFSET_DEFAULT

    @abstractmethod
    def do_search(self, query, context):
        """
            Implements the search call.
            -ElementTree.Element **query** an OpenSearch Query element
            -dict **context**: a dictionary of custom parameters
            @return: a list of results items
        """
        pass

    def get_url_markup(self, url, response_type, root=None):
        """
        Create the URL element for a description document.

        """
        markup = createMarkup('Url', OS_PREFIX, OS_NAMESPACE, root)
        markup.set("type", get_mimetype(response_type))

        template_query = self._create_template_query(root)

        query_template = ("%s%s?%s") % (
            url, response_type, template_query[:-1])
        markup.set("template", query_template)

        if self.rel is not None and self.rel != URL_REL_DEFAULT:
            markup.set("rel", self.rel)

        if self.indexOffset is not None \
                and self.indexOffset != URL_INDEX_OFFSET_DEFAULT:
            markup.set("indexOffset", str(self.indexOffset))

        if self.pageOffset is not None \
                and self.pageOffset != URL_PAGE_OFFSET_DEFAULT:
            markup.set("pageOffset", str(self.pageOffset))
        return markup

    def _create_template_query(self, root):
        """
        Creates a string to be used as parameters template list in the
        description document.

        As this description is used in a OpenSearch URL tag, the root parameter
        is required in order to update the tag with the necessary namespaces.

        @param root: the root tag of the document containing this element

        @return: a string describing the parameters query

        """
        template_query = ""
        for param in self.params_model:
            term = assign_prefix(root, param)

            url_param = ""
            if param.required:
                url_param = ("%s={%s}") % (param.par_name, term)
            else:
                url_param = ("%s={%s?}") % (param.par_name, term)

            template_query += ("%s&") % (url_param)
        return template_query
