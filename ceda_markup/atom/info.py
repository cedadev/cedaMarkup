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
from abc import abstractmethod
from xml.etree.ElementTree import Element


class Info(object):
    '''
    classdocs
    '''
    TEXT_TYPE = 'text'
    HTML_TYPE = 'html'
    XHTML_TYPE = 'xhtml'
    TYPES = [TEXT_TYPE, HTML_TYPE, XHTML_TYPE]

    def __init__(self, itype = TEXT_TYPE, body = ''):
        '''
        Constructor
        '''
        if type in Info.TYPES:
            self.type = itype
        else:
            raise Exception("Type is not allowed")
        self.body = body

    def buildElement(self):
        info = self._buildRoot()
        if self.type != Info.TEXT_TYPE:
            info.set('type', self.type)
        if self.type == Info.HTML_TYPE or self.type == Info.TEXT_TYPE:
            info.text = self.body

        if self.type == Info.XHTML_TYPE and isinstance(self.body, Element):
            info.append(self.body)
              
        return info

    @abstractmethod
    def _buildRoot(self):
        """
            Build the Element root for this instance
        """
        pass       
    
class Title(Info):
    '''
    classdocs
    '''

    def __init__(self, type, body):
        super(Title, self).__init__(type, body)
        
    def _buildRoot(self):
        return Element('title')      
    
class Summary(Info):
    '''
    classdocs
    '''

    def __init__(self, type, body):
        super(Summary, self).__init__(type, body)
        
    def _buildRoot(self):
        return Element('summary')
        
class Content(Info):
    '''
    classdocs
    '''

    def __init__(self, type, body):
        super(Content, self).__init__(type, body)
        
    def _buildRoot(self):
        return Element('content')        
    
class Rights(Info):
    '''
    classdocs
    '''

    def __init__(self, type, body):
        super(Rights, self).__init__(type, body)
        
    def _buildRoot(self):
        return Element('rights')    