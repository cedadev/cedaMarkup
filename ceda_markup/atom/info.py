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

Created on 25 May 2012

@author: Maurizio Nagni
'''
from xml.etree.ElementTree import Element
from ceda_markup.atom.atom import ATOM_NAMESPACE, ATOM_PREFIX
from ceda_markup.markup import createMarkup

'''
classdocs
'''
TEXT_TYPE = 'text'
HTML_TYPE = 'html'
XHTML_TYPE = 'xhtml'
TYPES = [TEXT_TYPE, HTML_TYPE, XHTML_TYPE]

def _assignTypeAtribute(itype, markup, body):
    if itype not in TYPES:
        raise Exception("Type is not allowed")

    if itype != TEXT_TYPE:
        markup.set('type', itype)
    if itype == HTML_TYPE or itype == TEXT_TYPE:
        markup.text = body

    if itype == XHTML_TYPE and isinstance(body, Element):
        markup.append(body)
    return markup    


def createTitle(root = None, ns = ATOM_NAMESPACE, body = None, itype = TEXT_TYPE):
    markup = createMarkup('title', ATOM_PREFIX, ns, root = root)
    return _assignTypeAtribute(itype, markup, body)

def createSummary(root = None, ns = ATOM_NAMESPACE, body = None, itype = TEXT_TYPE):
    markup = createMarkup('summary', ATOM_PREFIX, ns, root = root)
    return _assignTypeAtribute(itype, markup, body)

def createContent(root = None, ns = ATOM_NAMESPACE, body = None, itype = TEXT_TYPE):
    markup = createMarkup('content', ATOM_PREFIX, ns, root = root)
    return _assignTypeAtribute(itype, markup, body)

def createRights(root = None, ns = ATOM_NAMESPACE, body = None, itype = TEXT_TYPE):
    markup = createMarkup('rights', ATOM_PREFIX, ns, root = root)
    return _assignTypeAtribute(itype, markup, body)