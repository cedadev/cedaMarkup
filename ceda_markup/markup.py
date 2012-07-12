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

Created on 29 Jun 2012

@author: mnagni
'''
from xml.etree.ElementTree import _ElementInterface, Element
def createMarkup(tagName, tagPrefix, tagNamespace, root = None):
        '''
            Returns an ElementTree.Element instance
            @param tagName: the tag name    
            @param tagPrefix: the prefix to use for this tag
            @param tagNamespace: the tag's namespace
            @param root: the root Element of the document containing this element
            @return: a new instance                       
        '''
        #attach gml namespace to the document root element
        _tag = tagName
        
        if root is not None:
            if isinstance(root, _ElementInterface): 
                if root.get('xmlns') == tagNamespace:
                    _tag = tagName            
                else:
                    root.set("xmlns:%s" % (tagPrefix), tagNamespace)
                    if tagName is not None and tagPrefix is not None:
                        _tag = "%s:%s" % (tagPrefix, tagName)
                                    
        markup = Element(_tag)
        if root is None:
            markup.set("xmlns", tagNamespace)
        return markup
    
def createSimpleMarkup(text, root, tagName, ns, prefix):
    """
        Returns a new markup filling only its 'text' attribute
    """
    markup = createMarkup(tagName, prefix, ns, root)
    markup.text = text
    return markup