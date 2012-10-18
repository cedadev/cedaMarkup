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

Created on 21 Jun 2012

@author: Maurizio Nagni
'''

__version__ = '0.0.15'

import mimetypes
if not mimetypes.inited:
    mimetypes.init()
    if not getattr(mimetypes, 'types_map').has_key('.atom'):
        mimetypes.add_type('application/atom+xml', '.atom')
    if not getattr(mimetypes, 'types_map').has_key('.opensearchdescription'):        
        mimetypes.add_type('application/opensearchdescription+xml', \
                           '.opensearchdescription')


def extend_element(element, collection_to_append):
    '''
        Manages the extention of an xml.etree.ElementTree instance.
        As the Element.extend function has been introduced in python2.7
        for backward compatibility this method chooses the best approach
        @param element: an instance of xml.etree.ElementTree
        @param collectionToAppend: a collection to append to the element  
    '''    
    if hasattr(element, 'extend'):
        getattr(element, 'extend')(collection_to_append)
        return

    for item in collection_to_append:
        getattr(element, 'append')(item)       

def get_mimetype(extension):
    """
        Returns the mimetypes for a given file extension. 
        For example 'xml' should return 'text/xml'
        @param extension: the file extension 
        @return: the associated mimetype
    """
    return getattr(mimetypes, 'types_map')[('.%s') % (extension)]