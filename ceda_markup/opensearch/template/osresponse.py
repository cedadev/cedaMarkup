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

Created on 21 May 2012

@author: Maurizio Nagni
'''
from abc import abstractmethod
from datetime import datetime

class OSEngineResponse(object):
    '''
    classdocs
    '''


    def __init__(self, extension):
        '''
            Constructor
        '''        
        self.extension = extension
        
    @abstractmethod
    def generateResponse(self, result, queries, ospath, context):
        '''
            @param result: the output from digestSearchResults method
            @param queries: the value returned by a QueryTag.queryWithRoleRequest invocation
            @param hostURL: the opensearch engine URL
            @param kwargs: a dictionary of custom parameters 
        '''
        pass
    
    @abstractmethod
    def digestSearchResults(self, results, context):
        '''
            @param results: the value returned from a OSQuery.doSearch instance invocation
            @param queries: the value returned by a QueryTag.queryWithRoleRequest invocation
            @param ospath: the host URL
            @param kwargs: a dictionary of custom parameters 
        '''
        pass    
     
    
class Result(object):
    def __init__(self, count, startIndex, startPage, totalResults, iid = None, title = "Discovery feed for Search Services", updated = datetime.now().isoformat(), subresult = []):
        '''
            Constructor
            @param count: the number of search results per page desired by the search client
            @param startIndex: the index of the first search result desired by the search client
            @param startPage: the page number of the set of search results desired by the search client            
            @param totalResults: the total number of results            
            @param iid: a unique identifier, eventually an URI
            @param title: an atom.Entry instance 
            @param updated: the last time the record was updated
            @param subresult: a Subresult list                       
        '''
        self.count = count
        self.startIndex = startIndex
        self.startPage = startPage
        self.totalResult = totalResults
        self.id = iid
        self.title = title
        self.updated = updated
        self.subresult = subresult
        
class Subresult(object):
    def __init__(self, iid = None, title = "Discovery feed for Search Services", updated = datetime.now().isoformat(), **kwargs):
        '''
            Constructor            
            @param iid: a unique identifier, eventually an URI
            @param title: an atom.Entry instance 
            @param updated: the last time the record was updated
            @param kwargs: a custom dictionary                       
        '''
        self.id = iid
        self.title = title
        self.updated = updated         