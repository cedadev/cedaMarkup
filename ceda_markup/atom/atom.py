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

Created on 6 May 2012

@author: Maurizio Nagni
'''
from ceda_markup import get_mimetype
from ceda_markup.atom import REL_SEARCH, REL_SELF, REL_ALTERNATE
from ceda_markup.markup import createMarkup, createSimpleMarkup


ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
ATOM_PREFIX = 'atom'
ATOM_ROOT_TAG = 'feed'


def createAtomDocument(iid, title, updated, subtitle=None, rights=None):
    '''
        Returns an ElementTree.Element representing an Atom document
        @param iid: a string
        @param title: a string
        @param updated: a string
        @param subtitle: a string
        @param rights: a string
        @return: a new ElementTree.Element instance
    '''
    atom = createAtom()

    _id = createID(iid, atom)
    atom.append(_id)

    _title = createTitle(title, atom)
    atom.append(_title)

    _updated = createUpdated(updated, atom)
    atom.append(_updated)

    if subtitle is not None:
        _subtitle = createSubTitle(subtitle, atom)
        atom.append(_subtitle)

    if rights is not None:
        _rights = createRigths(rights, atom)
        atom.append(_rights)

    return atom


def createEntry(iid, title, updated,
                author=None, content=None, link=None,
                published=None, root=None,
                ns=ATOM_NAMESPACE):
    '''
        Constructor
        @param iid: an atom.ID instance
        @param title: an atom.Title instance
        @param updated: an atom.Update instance
        @param author: one or more atom.Author instances
        @param content: an atom.Content instance
        @param link: one or more atom.Link instances
        @param published: an atom.Published instance
        @param root: the document root element where attach the
                prefix:namespace for this element
    '''
    markup = createMarkup('entry', ATOM_PREFIX, ns, root)
    markup.append(iid)
    markup.append(title)
    markup.append(updated)

    if author is not None:
        if isinstance(author, list):
            getattr(markup, 'extend')(author)
        else:
            markup.append(author)

    if content is not None:
        markup.append(content)

    if link is not None:
        markup.append(link)

    if published is not None:
        markup.append(published)

    return markup


def createAtom(root=None, tagName=ATOM_ROOT_TAG, ns=ATOM_NAMESPACE):
    '''
        Returns an ElementTree.Element representing an Atom tag
        @param root: the root tag of the document containing this element
        @param tagName: the tagName
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createMarkup(tagName, ATOM_PREFIX, ns, root)


def createID(iid, root=None, ns=ATOM_NAMESPACE):
    '''
        Returns an Atom.id instance as ElementTree
        @param iid: a unique identifier, eventually an URI
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createSimpleMarkup(str(iid), root, 'id', ns, ATOM_PREFIX)


def createTitle(title, root=None, ns=ATOM_NAMESPACE):
    '''
        Returns an Atom.title instance as ElementTree
        @param title: the title's text
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createSimpleMarkup(title, root, 'title', ns, ATOM_PREFIX)


def createSubTitle(subtitle, root=None, ns=ATOM_NAMESPACE):
    '''
        Returns an Atom.subtitle instance as ElementTree
        @param title: the title's text
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    markup = createSimpleMarkup(str(subtitle), root, 'subtitle', ns,
                                ATOM_PREFIX)
    markup.set('type', 'html')
    return markup


def createRigths(rigths, root=None, ns=ATOM_NAMESPACE):
    '''
        Returns an Atom.title instance as ElementTree
        @param rigths: the rigths's text
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createSimpleMarkup(str(rigths), root, 'rigths', ns, ATOM_PREFIX)


def createUpdated(updated, root=None, ns=ATOM_NAMESPACE):
    '''
        Returns an Atom.updated instance as ElementTree
        @param updated: is a Date construct indicating the most
   recent instant in time when an entry or feed was modified in a way
   the publisher considers significant.
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createSimpleMarkup(str(updated), root, 'updated', ns, ATOM_PREFIX)


def createPublished(published, root=None, ns=ATOM_NAMESPACE):
    '''
        @param published: is a Date construct indicating an
   instant in time associated with an event early in the life cycle of
   the entry
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    return createSimpleMarkup(str(published), root, 'published', ns,
                              ATOM_PREFIX)

ATOM_LINK_REL_SELF = 'self'
ATOM_LINK_REL_FIRST = 'first'
ATOM_LINK_REL_LAST = 'last'
ATOM_LINK_REL_SEARCH = 'search'
ATOM_LINK_REL = [ATOM_LINK_REL_SELF, ATOM_LINK_REL_FIRST,
                 ATOM_LINK_REL_LAST, ATOM_LINK_REL_SEARCH]


def createLink(iri, rel=None, itype=None, root=None, ns=ATOM_NAMESPACE):
    '''
        @param iri: contains the link's IRI
        @param rel: a string like 'self', 'first', 'last', ...
        @param itype: an advisory media type as 'application/atom+xml'
        @param root: the root tag of the document containing this element
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance
    '''
    markup = createMarkup('link', ATOM_PREFIX, ns, root)
    markup.set('href', iri)
    if rel is not None:
        markup.set('rel', rel)
    if itype is not None:
        markup.set('type', itype)
    return markup


def create_autodiscovery_link(root, path,
                              params_model, context,
                              extension=None,
                              rel=REL_SELF,
                              start_index=None):
    """
        Appends an autodiscovery link to the given 'root' document
        @param path: the host URL
        @param extension: the extension
        @param rel: a Link type identificator. If None returns a generic ID
        @param params_model: a list of OSParam instances
        @param context: a dictionary containing one value or None to pair with
                the params_model
    """
    href = _generate_autodiscovery_path(path, extension,
                                        params_model, context,
                                        rel, start_index)

    itype = get_mimetype(extension)
    return createLink(href, rel, itype, root)


def _generate_autodiscovery_path(path, extension,
                                 params_model, context,
                                 rel=REL_SELF, start_index=None):
    """
        Assemble a path pointing to an opensearch engine
        @param path: the host URL
        @param extension: the extension
        @param params_model: a list of OSParam instances
        @param context: a dictionary containing one value or None to pair with
                the params_model
        @param rel: a Link type identificator. If None returns a generic ID
        @param startIndex:
    """
    if rel is None:
        return path

    if rel == REL_SEARCH:
        return path

    if not path.endswith('/'):
        path = '%s/' % path

    if rel == REL_ALTERNATE:
        return "%s%s" % (path, extension)

    ret = "%s%s?" % (path, extension)

    for param in params_model:
        if param.par_name == 'startIndex':
            if start_index is None:
                ret = ret + \
                    "&%s=%s" % (param.par_name, context[param.par_name])
            else:
                ret = ret + "&%s=%s" % (param.par_name, start_index)
        else:
            if param.par_name in context \
                    and context[param.par_name] is not None:
                ret = ret + "&%s=%s" \
                    % (param.par_name, context[param.par_name])
    return ret
