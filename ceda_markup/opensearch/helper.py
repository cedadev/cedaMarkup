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

Created on 18 May 2016

@author: wilsona
'''


def assign_prefix(root, param):
    """
    Assign a prefix to a parameter.

    If a prefix is available in the parameter object use that otherwise
    generate a prefix. Add the namespace for the parameter to the root object
    using the prefix.

    @param root: the root tag of the document
    @param param: an os_param object

    @return: a string containing the prefix:tern_name

    """
    if param.namespace is None or param.namespace == root.attrib['xmlns']:
        return param.term_name

    for key, value in root.items():
        if value == param.namespace:
            return ("%s:%s") % (key[6:], param.term_name)

    # use the user defined prefix for the namespace
    if param.namespace_prefix:
        root.set("xmlns:%s" % (param.namespace_prefix), param.namespace)
        return ("%s:%s") % (param.namespace_prefix, param.term_name)

    index = 0
    while True:
        if "xmlns:a%d" % (index) not in root.keys():
            break
        index = index + 1

    root.set("xmlns:a%d" % (index), param.namespace)
    return ("a%d:%s") % (index, param.term_name)
