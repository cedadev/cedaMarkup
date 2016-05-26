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

Created on 29 Jun 2012

@author: mnagni
'''
import unittest
from ceda_markup.atom.atom import createAtom, createID, createUpdated,\
    createEntry, createAtomDocument
from xml.etree.ElementTree import tostring, Element
from ceda_markup.atom.info import createTitle


class AtomTest(unittest.TestCase):

    def test_atom(self):
        # atom tag as root
        atom = createAtom()
        self.assertEqual(
            tostring(atom), '<feed xmlns="http://www.w3.org/2005/Atom" />')

        # atom tag as SubElement of another root element
        root = Element('myCustomTag')
        atom = createAtom(root)
        root.append(atom)
        self.assertEqual(tostring(root), '<myCustomTag xmlns:atom="http://www.w3.org/2005/Atom">\
<atom:feed /></myCustomTag>')

    def test_entry(self):
        atom = createAtom()
        title = createTitle(root=atom, body='testEntry')
        iid = createID(1, root=atom)
        update = createUpdated('2012-0619T21:02:00.626Z', root=atom)
        entry = createEntry(iid, title, update, root=atom)
        atom.append(entry)
        self.assertEqual(tostring(atom), '<feed xmlns="http://www.w3.org/2005/Atom">\
<entry><id>1</id><title>testEntry</title><updated>2012-0619T21:02:00.626Z</updated>\
</entry></feed>')

        root = Element('myCustomTag')
        title = createTitle(root=root, body='testEntry')
        iid = createID(1, root=root)
        update = createUpdated('2012-0619T21:02:00.626Z', root=atom)
        atom = createEntry(iid, title, update, root=root)
        root.append(atom)
        self.assertEqual(tostring(root), '<myCustomTag xmlns:atom="http://www.w3.org/2005/Atom">\
<atom:entry><atom:id>1</atom:id><atom:title>testEntry</atom:title><updated>2012-0619T21:02:00.626Z</updated>\
</atom:entry></myCustomTag>')

        root = createAtomDocument(1, 'atomTitle', '2012-0619T21:02:00.626Z')
        iid = createID(2, root=root)
        title = createTitle(root=root, body='testEntry')
        update = createUpdated('2012-0619T21:02:00.626Z', root=root)
        entry = createEntry(iid, title, update, root=root)
        root.append(entry)
        self.assertEqual(tostring(root), '<feed xmlns="http://www.w3.org/2005\
/Atom"><id>1</id><title>atomTitle</title><updated>2012-0619T21:02:00.626Z\
</updated><entry><id>2</id><title>testEntry</title><updated\
>2012-0619T21:02:00.626Z</updated></entry></feed>', 'Error')
