import math
from ceda_markup.atom.link import REL_SEARCH, REL_SELF, REL_ALTERNATE
from ceda_markup import get_mimetype
from ceda_markup.atom.atom import ATOM_LINK_REL_SEARCH, createLink

def assign_prefix(root, param):
    if param.namespace is None:
        return param.term_name
    
    for key, value in root.items():
        if value == param.namespace:
            return ("%s:%s") % (key[6:], param.term_name)
    
    index = 0
    while True:
        if "xmlns:a%d" % (index) not in root.keys():                
            break 
        index = index + 1
        
    root.set("xmlns:a%d" % (index), param.namespace)
    return ("a%d:%s") % (index, param.term_name)

def create_template_query(root, query):
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
        term = assign_prefix(root, param)
        
        url_param = ""
        if param.required:             
            url_param = ("%s={%s}") % (param.par_name, term)
        else:
            url_param = ("%s={%s?}") % (param.par_name, term)
           
        template_query += ("%s&") % (url_param)
    return template_query

COUNT_DEFAULT = 10
START_INDEX_DEFAULT = 1
START_PAGE_DEFAULT = 1

def filter_results(results, count = COUNT_DEFAULT, \
                   start_index = START_INDEX_DEFAULT, \
                   start_page = START_PAGE_DEFAULT):
    """
        Returns the opensearch results list according to the 
        'count', 'startIndex', 'startPage' parameters
        @param results: an instance or a list of instances to be displayed in 
                        the opensearch response
        @param count: the number of search results per page desired by 
                        the search client
        @param start_index: the index of the first search result desired 
                        by the search client
        @param startPage: the page number of the set of search results 
                        desired by the search client
        @return: the selected results or None if the results is None 
                        or is not a list or is an empty list
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

    if start_index is not None and start_index > 1 and start_index <= tot_res:
        int_start_index = start_index
    else:
        int_start_index = START_INDEX_DEFAULT    
    
    if start_page is not None \
            and math.ceil((tot_res - int_start_index + 1)/float(int_count)) \
            >= start_page:
        int_start_page = start_page
    else:
        int_start_page = START_PAGE_DEFAULT
            
    first_result = int_start_index - 1
    last_result = first_result + int_count
    
    if int_start_page > 1 \
            and first_result + (int_start_page - 1)*int_count <= tot_res:
        first_result = first_result + (int_start_page - 1)*int_count
        
    if first_result + int_count <= tot_res:            
        last_result = first_result + int_count
    else:
        last_result = tot_res

    return _results[first_result:last_result]

def generate_autodiscovery_path(path, linkid, extension, \
                                rel = REL_SELF, \
                                count = None, start_index = None, \
                                start_page=None):
    """
        Assemble a path pointing to an opensearch engine 
        @param path: the host URL
        @param linkid: the search id
        @param extension: the extension
        @param rel: a Link type identificator. If None returns a generic ID 
        @param count: the number of search results per page 
                        desired by the search client        
        @param start_index: the first search result 
                        desired by the search client  
        @param start_page: the page number of the set of 
                            search results desired by the search client            
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

    ret = None
    if linkid:
        ret = "%s%s/%s/?" % (path, linkid, extension)
    else:
        ret = "%s%s/?" % (path, extension)
    
    return "%sstartIndex=%d&count=%d" % (ret, start_index, count)


def create_autodiscovery_link(root, path, extension = None, \
                              linkid = None, \
                              rel = REL_SELF, \
                              count=None, start_index=None, start_page=None):
    """
        Appends an autodiscovery link to the given 'root' document 
        @param path: the host URL
        @param extension: the extension
        @param linkid: the search id        
        @param rel: a Link type identificator. If None returns a generic ID
        @param count: the number of search results per page 
                        desired by the search client        
        @param start_index: the first search result 
                        desired by the search client  
        @param start_page: the page number of the set of 
                            search results desired by the search client        
    """
    href = generate_autodiscovery_path(path, linkid, \
                                       extension, rel, \
                                       count, start_index, start_page)    
    itype = get_mimetype(extension)
    if rel == ATOM_LINK_REL_SEARCH:
        itype = get_mimetype('opensearchdescription')      
    return createLink(href, rel, itype, root)                    
