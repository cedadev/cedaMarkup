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

Created on 24 May 2012

@author: Maurizio Nagni
'''
from ceda_markup.opensearch.os_request import OS_PREFIX, OS_ROOT_TAG,\
    OS_NAMESPACE
from ceda_markup.markup import createMarkup

def create_query(mimetype, params_model, params_values, is_response = True, root = None, tag_name = OS_ROOT_TAG, ns = OS_NAMESPACE):
    '''
        Returns an ElementTree.Element representing an OpenSearch.Query tag
        @param mimetype:
        @param params_model: a list of OSParam instances
        @param params_values: a dictionary containing one value or None to pair with the params_model 
        @param root: the root tag of the document containing this element
        @param tagName: the tagName 
        @param ns: the tag namespace
        @return: a new ElementTree.Element instance     
    '''
    markup = createMarkup('Query', OS_PREFIX, ns, root)
    markup.set("role", "request")
    for param in params_model:
        if param.par_name in params_values and params_values[param.par_name] is not None:
            if param.term_name == 'searchTerms':
                markup.set(param.term_name, ' '.join(str(x) for x in params_values[param.par_name]))
            else:
                markup.set(param.par_name, params_values[param.par_name])
    return markup       