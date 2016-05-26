""""
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

"""

from ceda_markup import get_mimetype
from ceda_markup.atom import REL_SEARCH, REL_SELF
from ceda_markup.markup import createMarkup, createSimpleMarkup
from ceda_markup.opensearch.constants import DESCRIPTION_FILE_NAME, \
    OS_NAMESPACE, OS_PREFIX, OS_ROOT_TAG


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

OS_ADULT_CONTENT_DEFAULT = 'False'
OS_INPUT_ENCODING_DEFAULT = 'UTF-8'
OS_OUTPUT_ENCODING_DEFAULT = 'UTF-8'

__all__ = ["OpenSearchDescription"]


class OpenSearchDescription(object):
    """
    This class encapsulates the Open Search Description.

    An XML encoded version of the document can be retrieved via the
    get_xml_markup method. A link to the document that can be included in
    search results can be obtained be the get_xml_autodiscovery_link method.

    """

    def __init__(self, short_name, description, path,
                 file_name=DESCRIPTION_FILE_NAME, contact=None, tags=None,
                 long_name=None, image=None, developer=None, attribution=None,
                 syndacation_right=None, adult_content=None, language=None,
                 input_encoding=None, output_encoding=None):
        """
        Construct an OpenSearchDescription.

        @param short_name: a brief human-readable title that identifies this
            search engine
        @param description: a human-readable text description of the search
            engine
        @param path: the path to the description document
        @param file_name: the name of the description document
        @param contact: an email address at which the maintainer of the
            description document can be reached
        @param tags: a set of words that are used as keywords to identify and
            categorize this search content. Tags must be a single word and are
            delimited by the space character (' ').
        @param long_name: an extended human-readable title that identifies this
            search engine
        @param image: a list of osImage instances
        @param developer: The human-readable name or identifier of the creator
            or maintainer of the description document
        @param attribution: a string containing list of all sources or entities
            that should be credited for the content contained in the search
            feed
        @param syndacation_right: a value that indicates the degree to which
            the search results provided by this search engine can be queried,
            displayed, and redistributed
        @param adult_content: a boolean value that should be set to true if
            the search results may contain material intended only for adults
        @param language: a list that indicates that the search engine supports
            search results in the specified language
        @param input_encoding: a list that indicates that the search engine
            supports search requests encoded with the specified character
            encoding
        @param output_encoding: a list that indicates that the search engine
            supports search responses encoded with the specified character
            encoding

        """

        self.description = description[:MAX_OS_DESCRIPTION_LEN]
        self.short_name = short_name[:MAX_OS_SHORT_NAME_LEN]

        if not path.endswith('/'):
            path = '%s/' % path
        self.path = path

        if file_name is not None:
            self.file_name = file_name
        else:
            self.file_name = DESCRIPTION_FILE_NAME

        # Should check that is an email format
        self.contact = contact

        if tags:
            self.tags = tags[:MAX_OS_TAGS_LEN]
        else:
            self.tags = None

        if long_name:
            self.long_name = long_name[:MAX_OS_LONG_NAME_LEN]
        else:
            self.long_name = None

        if developer:
            self.developer = developer[:MAX_OS_DEVELOPER_LEN]
        else:
            self.developer = None

        if attribution:
            self.attribution = attribution[:MAX_OS_ATTRIBUTION_LEN]
        else:
            self.attribution = None

        self.syndacation_right = None
        if syndacation_right and syndacation_right in OS_SYNDACATION_RIGHT:
            self.syndacation_right = syndacation_right

        self.adult_content = OS_ADULT_CONTENT_DEFAULT
        if adult_content is not None:
            if adult_content in [False, 'false', 'FALSE', '0', 'no', 'NO']:
                self.adult_content = 'False'
            else:
                self.adult_content = 'True'

        if image is None:
            self.image = []
        else:
            self.image = image

        if language is None:
            self.language = ['*']
        else:
            self.language = language

        if input_encoding is None:
            self.input_encoding = [OS_INPUT_ENCODING_DEFAULT]
        else:
            self.input_encoding = input_encoding

        if output_encoding is None:
            self.output_encoding = [OS_OUTPUT_ENCODING_DEFAULT]
        else:
            self.output_encoding = output_encoding

    def get_xml_markup(self, responses, query, host_url, root=None):
        """
        Get the description document in an ElementTree.

        @param responses: a list of OSResponse instances
        @param query: an OSQuery instance
        @param host_url: the host URL
        @param root: the root tag of the document containing this element

        @returns the description document

        """
        markup = createMarkup(OS_ROOT_TAG, OS_PREFIX, OS_NAMESPACE, root)
        markup.append(self._create_short_name(root=markup))
        markup.append(self._create_description(root=markup))

        if self.tags is not None:
            markup.append(self._create_tags(root=markup))

        if self.contact is not None:
            markup.append(self._create_contact(root=markup))

        if self.long_name is not None:
            markup.append(self._create_long_name(root=markup))

        if self.developer is not None:
            markup.append(self._create_developer(root=markup))

        if self.attribution is not None:
            markup.append(self._create_attribution(root=markup))

        if self.image is not None and isinstance(self.image, list):
            for img in self.image:
                markup.append(self._create_image(img.url, img.height,
                                                 img.width, root=markup))

        if self.syndacation_right is not None:
            markup.append(self._create_syndacation_right(root=markup))

        if self.adult_content is not None:
            markup.append(self._create_adult_content(root=markup))

        if self.language and isinstance(self.language, list):
            for item in self.language:
                markup.append(self._create_language(item, root=markup))

        if self.input_encoding and isinstance(self.input_encoding, list):
            for item in self.input_encoding:
                markup.append(self._create_input_encoding(item, root=markup))

        if self.output_encoding and isinstance(self.output_encoding, list):
            for item in self.output_encoding:
                markup.append(self._create_output_encoding(item, root=markup))

        url = self._get_path_url(host_url)

        for item in responses:
            markup.append(
                query.get_url_markup(url, item.extension, root=markup))

        markup.append(
            self._create_self_autodiscovery_url(host_url, root=markup))

        return markup

    def get_xml_autodiscovery_link(self, host_url, tag_prefix, tag_namespace,
                                   root=None):
        """
        Create an ElementTree.Element for an autodiscovery link to the
        description documents and append it to the given 'root' document.

        @param host_url: the host URL
        @param tag_prefix: the prefix to use for this tag
        @param tag_namespace: the tag's namespace
        @param root: the root tag of the document containing this element

        @returns an ElementTree.Element containing a link to the description
                document

        """
        uri = self._get_file_url(host_url)
        markup = createMarkup('link', tag_prefix, tag_namespace, root)
        markup.set('rel', REL_SEARCH)
        markup.set('href', uri)
        markup.set('type', get_mimetype('opensearchdescription'))
        return markup

    def _create_short_name(self, root=None):
        """
        Create a ShortName element.

        """
        return createSimpleMarkup(self.short_name, root, 'ShortName',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_description(self, root=None):
        """
        Create a Description element.

        """
        return createSimpleMarkup(self.description, root, 'Description',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_tags(self, root=None):
        """
        Create a Tags element.

        """
        return createSimpleMarkup(self.tags, root, 'Tags', OS_NAMESPACE,
                                  OS_PREFIX)

    def _create_contact(self, root=None):
        """
        Create a Contact element.

        """
        return createSimpleMarkup(self.contact, root, 'Contact',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_long_name(self, root=None):
        """
        Create a LongName element.

        """
        return createSimpleMarkup(self.long_name, root, 'LongName',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_developer(self, root=None):
        """
        Create a Developer element.

        """
        return createSimpleMarkup(self.developer, root, 'Developer',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_attribution(self, root=None):
        """
        Create an Attribution element.

        """
        return createSimpleMarkup(self.attribution, root, 'Attribution',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_syndacation_right(self, root=None):
        """
        Create a SyndacationRight element.

        """
        return createSimpleMarkup(self.syndacation_right, root,
                                  'SyndacationRight', OS_NAMESPACE, OS_PREFIX)

    def _create_adult_content(self, root=None):
        """
        Create an AdultContent element.

        """
        return createSimpleMarkup(self.adult_content, root, 'AdultContent',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_language(self, item, root=None):
        """
        Create a Language element.

        """
        return createSimpleMarkup(item, root, 'Language', OS_NAMESPACE,
                                  OS_PREFIX)

    def _create_input_encoding(self, item, root=None):
        """
        Create an InputEncoding element.

        """
        return createSimpleMarkup(item, root, 'InputEncoding',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_output_encoding(self, item, root=None):
        """
        Create an OutputEncoding element.

        """
        return createSimpleMarkup(item, root, 'OutputEncoding',
                                  OS_NAMESPACE, OS_PREFIX)

    def _create_image(self, url, height=None, width=None, root=None):
        """
        Create an Image element.

        """
        markup = createSimpleMarkup(
            url, root, 'Image', OS_NAMESPACE, OS_PREFIX)
        if height is not None and isinstance(height, (int, long)):
            markup.set("height", height)

        if width is not None and isinstance(width, (int, long)):
            markup.set("width", width)
        return markup

    def _create_self_autodiscovery_url(self, host_url, root=None):
        """
        Create the self URL element of a description document.

        """
        markup = createMarkup('Url', OS_PREFIX, OS_NAMESPACE, root)
        markup.set("type", get_mimetype('opensearchdescription'))
        markup.set("template", self._get_file_url(host_url))
        markup.set("rel", REL_SELF)
        return markup

    def _get_path_url(self, host_url):
        """
        Append the path to the host name

        @param host_url: the host URL

        """
        if host_url.endswith('/'):
            url = '%s%s' % (host_url, self.path)
        else:
            url = '%s/%s' % (host_url, self.path)
        return url

    def _get_file_url(self, host_url):
        """
        Get the URL of the description document.

        @param host_url: the host URL

        @return the the URL of the description document

        """
        if host_url.endswith('/'):
            url = '%s%s%s' % (host_url, self.path, self.file_name)
        else:
            url = '%s/%s%s' % (host_url, self.path, self.file_name)
        return url
