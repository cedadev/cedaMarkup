import math
from ceda_markup.atom.link import REL_SEARCH, REL_SELF, REL_ALTERNATE
from ceda_markup import get_mimetype
from ceda_markup.atom.atom import ATOM_LINK_REL_SEARCH, createLink

def assignPrefix(root, param):
    if param.namespace is None:
        return param.term_name
    
    for k,v in root.items():
        if v == param.namespace:
            return ("%s:%s") % (k[6:], param.term_name)
    
    index = 0
    while True:
        if "xmlns:a%d" % (index) not in root.keys():                
            break 
        index = index + 1
        
    root.set("xmlns:a%d" % (index), param.namespace)
    return ("a%d:%s") % (index, param.term_name)

def createTemplateQuery(root, query):
    '''
        Creates a string to be used as parameters template list in the "description".
        As this description is used in a OpenSearch URL tag, the root parameter is required 
        in order to update the tag with the necessary namespaces
        @param root: the OpenSearchRequest.ROOT_TAG tag.
        @param query: an OSQuery instance.        
        @return: a string describing the parameters query
    '''
    template_query = ""
    for param in query.params_model:
        term = assignPrefix(root, param)
        
        urlParam = ""
        if param.required:             
            urlParam = ("%s={%s}") % (param.par_name, term)
        else:
            urlParam = ("%s={%s?}") % (param.par_name, term)
           
        template_query += ("%s&") % (urlParam)
    return template_query

COUNT_DEFAULT = 10
START_INDEX_DEFAULT = 1
START_PAGE_DEFAULT = 1

def filterResults(results, count = COUNT_DEFAULT, startIndex = START_INDEX_DEFAULT, startPage = START_PAGE_DEFAULT):
    """
        Returns the opensearch results list according to the 
        'count', 'startIndex', 'startPage' parameters
        @param results: an instance or a list of instances to be displayed in the opensearch response
        @param count: the number of search results per page desired by the search client
        @param startIndex: the index of the first search result desired by the search client
        @param startPage: the page number of the set of search results desired by the search client
        @return: the selected results or None if the results is None or is not a list or is an empty list
    """
    if results is None:
        return None
    elif isinstance(results, list) and len(results) == 0:
        return None
    elif not isinstance(results, list):
        _results = [results]
    else:
        _results = results
        
    tot_res = len(_results)
        
    if count is not None and count > 0:
        int_count = count
    else:
        int_count = COUNT_DEFAULT

    if startIndex is not None and startIndex > 1 and startIndex <= tot_res:
        int_startIndex = startIndex
    else:
        int_startIndex = START_INDEX_DEFAULT    
    
    if startPage is not None and math.ceil((tot_res - int_startIndex + 1)/float(int_count)) >= startPage:
        int_startPage = startPage
    else:
        int_startPage = START_PAGE_DEFAULT
            
    firstResult = int_startIndex - 1
    lastResult = firstResult + int_count
    
    if int_startPage > 1 and firstResult + (int_startPage - 1)*int_count <= tot_res:
        firstResult = firstResult + (int_startPage - 1)*int_count
        
    if firstResult + int_count <= tot_res:            
        lastResult = firstResult + int_count
    else:
        lastResult = tot_res

    return _results[firstResult:lastResult]

def generateAutodiscoveryPath(path, linkid, extension, startIndex = None, rel = REL_SELF):
    """
        Assemble a path pointing to an opensearch engine 
        @param path: the host URL
        @param linkid: the search id
        @param extension: the extension
        @param startIndex: the starting index
        @param rel: a Link type identificator. If None returns a generic ID   
    """
    if rel == None:
        if linkid:
            return "%s/search/%s/" % (path, linkid)
        else:
            return "%s/search/" % (path)

    if rel == REL_SEARCH:
        if linkid:
            return "%s%s/description" % (path, linkid)    
        else:
            return "%sdescription" % (path)
    
    if rel == REL_ALTERNATE:
        if linkid:
            return "%s%s/%s" % (path, linkid, extension)
        else:
            return "%s%s" % (path, extension)

    if linkid:
        return "%s%s/%s/?startIndex=%d" % (path, linkid, extension, startIndex)
    else:
        return "%s%s/?startIndex=%d" % (path, extension, startIndex)


def createAutodiscoveryLink(root, path, extension = None, linkid = None, startIndex = 0, rel = REL_SELF):
    """
        Appends an autodiscovery link to the given 'root' document 
        @param path: the host URL
        @param extension: the extension
        @param linkid: the search id        
        @param startIndex: the starting index
        @param rel: a Link type identificator. If None returns a generic ID  
    """
    href = generateAutodiscoveryPath(path, linkid, extension, startIndex, rel)    
    itype = get_mimetype(extension)
    if rel == ATOM_LINK_REL_SEARCH:
        itype = get_mimetype('opensearchdescription')      
    return createLink(href, rel, itype, root)                    
