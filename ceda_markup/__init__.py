'''
@package: ceda_markup
The CEDA Markup package provides markup for Open Search.

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

Created on 21 Jun 2012

@author: Maurizio Nagni
'''

import mimetypes


if not mimetypes.inited:
    mimetypes.init()
if '.atom' not in getattr(mimetypes, 'types_map').keys():
    mimetypes.add_type('application/atom+xml', '.atom')
if '.opensearchdescription' not in getattr(mimetypes, 'types_map').keys():
    mimetypes.add_type('application/opensearchdescription+xml',
                       '.opensearchdescription')

__version__ = '0.2.0.dev1'


def get_mimetype(extension):
    """
        Returns the mimetypes for a given file extension.
        For example 'xml' should return 'text/xml'
        @param extension: the file extension
        @return: the associated mimetype
    """
    return getattr(mimetypes, 'types_map')[('.%s') % (extension)]
