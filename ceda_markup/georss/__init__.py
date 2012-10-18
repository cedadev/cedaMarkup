from ceda_markup.gml.gml import createPosList, createLinearRing, createExterior,\
    createPolygon, createLowerCorner, createUpperCorner, createEnvelope,\
    createInterior
from ceda_markup.georss.georss import createWhere
import re

def create_where_from_postgis(geometry, root = None):
    '''
        Creates an georss:where instance from a postgis geometry text element.
        Postgis has a well defined list of geometries:
        * `LINESTRING(-71.160281 42.258729,
                        -71.160837 42.259113,
                        -71.161144 42.25932)`
        * `MULTILINESTRING((-71.160281 42.258729,
                            -71.160837 42.259113,
                            -71.161144 42.25932))`
        * `POINT(-71.064544 42.28787)`
        * `POLYGON(
        (0 0,4 0,4 4,0 4,0 0),
        (1 1, 2 1, 2 2, 1 2,1 1)
        )`
        * `MULTIPOLYGON(
        ((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), 
        ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1))
        )`
        * `BOX2D(220186.984375 150406,220288.25 150506.140625)`       
        For such types this method return the georss:where properly filled.
        Actually supports only BOX2D. POLYGON, MULTIPOLYGON
        
        **Parameters**
            * geometry: a postgis geometry as text
            * root: the root element of the XML document
            
        **Exception**
        If `geometry` is None or not a string     
    '''
    if geometry is None or not isinstance(geometry, str):
        raise Exception("Geometry not valid")
    
    geometry = geometry.strip()
    if geometry.startswith('MULTIPOLYGON') or geometry.startswith('POLYGON'):
        polygon = None 
        if geometry.startswith('MULTIPOLYGON'):
            polygon = _create_polygon_from_multi(geometry[13:-1], root = None)
        if geometry.startswith('POLYGON'):
            polygon = _create_polygon(geometry[8:-1], root = None)
        if polygon is not None:
            return createWhere(root = root, body = polygon)
    
    if geometry.startswith('BOX2D('):
        lc, uc = geometry[6:-1].split(',')
        lowerCorner = createLowerCorner(root, values = [float(item) 
                                                        for item in lc.split()])
        upperCorner = createUpperCorner(root, values = [float(item) 
                                                        for item in uc.split()])
        where_body = createEnvelope(lowerCorner, upperCorner, root)
        return createWhere(root = root, body = where_body)
        
def _create_polygon(geometry, root = None):    
    starts = [m.start() for m in re.finditer('\(', geometry)]
    end = [m.start() for m in re.finditer('\)', geometry)]
    
    interior = []
    exterior = None
    for index in range(len(starts)):        
        posList = createPosList(root = root, 
                        values = [float(val) for val 
                                  in geometry[starts[index] + 1:end[index]].\
                                  replace(',', ' ').split()], 
                        srsDimension = '2')
        linearRing = createLinearRing(root = root, body = posList)
        if len(starts) > 1:
            interior.append(createInterior(root = root, body = linearRing))
        elif len(starts) == 1:
            exterior = createExterior(root = root, body = linearRing)
    
    return createPolygon(root = root, exterior = exterior, interior = interior)            
        
def _create_polygon_from_multi(geometry, root = None):
    polygons = []
    starts = [m.start() for m in re.finditer('\(\(', geometry)]
    end = [m.start() for m in re.finditer('\)\)', geometry)]
    
    for index in range(len(starts)): 
        text_polygons = geometry[starts[index] + 1:end[index] + 1]
        polygons.append(_create_polygon(text_polygons, root))       
    
    if len(polygons) == 1:
        return polygons[0]
    
    if len(polygons) > 1:
        return polygons
    
    return None
                
        