from ceda_markup.gml.gml import createPosList, createLinearRing, createExterior,\
    createPolygon, createLowerCorner, createUpperCorner, createEnvelope
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
        * `POLYGON((-71.1776585052917 42.3902909739571,
                    -71.1776820268866 42.3903701743239,
                    -71.1776063012595 42.3903825660754,
                    -71.1775826583081 42.3903033653531,
                    -71.1776585052917 42.3902909739571))`
        * `MULTIPOLYGON(
                    ((-71.1776585052917 42.3902909739571,
                    -71.1776820268866 42.3903701743239,
                    -71.1776063012595 42.3903825660754,
                    -71.1775826583081 42.3903033653531,
                    -71.1776585052917 42.3902909739571)),
                    ((-71.1043632495873 42.315113108546,
                    -71.1043583974082 42.3151211109857,
                    -71.1043443253471 42.3150676015829,
                    -71.1043850704575 42.3150793250568,
                    -71.1043632495873 42.315113108546))
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
            polygon = _create_polygon(geometry[13:-1], root = None)
        if geometry.startswith('POLYGON'):
            polygon = _create_polygon(geometry[7:], root = None)
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
    polygons = []
    starts = [m.start() for m in re.finditer('\(\(', geometry)]
    end = [m.start() for m in re.finditer('\)\)', geometry)]
    
    for index in range(len(starts)):        
        posList = createPosList(root = root, 
                        values = [float(val) for val 
                                  in geometry[starts[index]+2:end[index]].\
                                  replace(',', ' ').split()], 
                        srsDimension = '2')
        linearRing = createLinearRing(root = root, body = posList)
        exterior = createExterior(root = root, body = linearRing)
        polygons.append(createPolygon(root = root, body = exterior))
    
    if len(polygons) == 1:
        return polygons[0]
    
    if len(polygons) > 1:
        return polygons
    
    return None
        