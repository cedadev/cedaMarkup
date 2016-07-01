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
from ceda_markup.atom.atom import ATOM_NAMESPACE, ATOM_PREFIX
from ceda_markup.markup import createMarkup, createSimpleMarkup


def _create_person(markup, name, email, uri, root, ns):
    """"
    Returns an instance as ElementTree.

        @param markup (ElementTree): the ElementTree
        @param name (str): the name of the author
        @param email (str): the email of the author
        @param uri (str): the uri of the author
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace

        @return: a new ElementTree.Element instance
    """
    markup.append(createSimpleMarkup(str(name), root, 'name', ns, ATOM_PREFIX))
    if email:
        markup.append(
            createSimpleMarkup(str(email), root, 'email', ns, ATOM_PREFIX))
    if uri:
        markup.append(
            createSimpleMarkup(str(uri), root, 'uri', ns, ATOM_PREFIX))
    return markup


def createAuthor(name, root=None, ns=ATOM_NAMESPACE, uri=None, email=None):
    markup = createMarkup('author', ATOM_PREFIX, ns, root)
    return _create_person(markup, name, email, uri, root, ns)


def createContributor(name, root=None, ns=ATOM_NAMESPACE, uri=None,
                      email=None):
    markup = createMarkup('contributor', ATOM_PREFIX, ns, root)
    return _create_person(markup, name, email, uri, root, ns)
