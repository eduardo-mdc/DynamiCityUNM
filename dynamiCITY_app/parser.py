import json
from shapely import wkt
import math

class EndpointParser():
    def __init__(self, data):
        self.data = data

    def transform_geometry(self, geometry, geometry_type):
        if geometry_type is 'Polygon':
            return self.transform_polygon(geometry)
        elif geometry_type is 'MultiPolygon':
            return self.transform_multipolygon(geometry)
        elif geometry_type is 'Point':
            return self.transform_point(geometry)
        
    def transform_polygon(self, polygon_string):
        polygon = wkt.loads(polygon_string)
        coordinates = [[]]
        for point in polygon.exterior.coords:
            coordinates[0].append([point[0], point[1]])
        return coordinates
    
    def transform_point(self, polygon_string):
        point = wkt.loads(polygon_string)
        point = point.coords
        coordinates = [point[0], point[1]]
        return coordinates

    def transform_multipolygon(self, multipolygon_string):
        multipolygon = wkt.loads(multipolygon_string)
        coordinates = [[] for _ in range(len(multipolygon.geoms))]  # Create a list for each polygon

        for idx, polygon in enumerate(multipolygon.geoms):
            for point in polygon.exterior.coords:
                coordinates[idx].append([point[0], point[1]])  # Append point to the current polygon

        coordinates = [coordinates]
        return coordinates
    
    def geometry_parser(self,geometry_type, feature, row):
        geometry = row['attributes'][geometry_type.lower()]
        if geometry is not None:
            feature['geometry'] = {
                'type': geometry_type,
                'coordinates': self.transform_geometry(geometry, geometry_type)
            }
            return feature
      
        return None
    
    def parse(self):
        feature_collection = {
            'type': 'FeatureCollection',
            'features': []
        }
        
        for row in self.data:
                feature = self.parse_line(row)
                if feature:
                    # Add the Feature to the Feature Collection
                    feature_collection['features'].append(json.loads(feature))

        return feature_collection

class CountyParser(EndpointParser):
    def __init__(self, data):
        super().__init__(data)

    def parse_line(self,row):
        # Create a Feature for the county
        feature = {
            'type': 'Feature',
            'properties': {
                'county_name': row['attributes']['county_name'],
                'created': row['attributes']['created']
            },
            'geometry': None
        }
    
        # Check if the county has a polygon
        if row['attributes']['polygon'] is not None:
            feature = self.geometry_parser('Polygon',feature,row)
        # Check if the county has a multipolygon
        elif row['attributes']['multipolygon'] is not None:
            feature = self.geometry_parser('MultiPolygon',feature,row)
        
        if feature:
            return json.dumps(feature)
        

class DistrictParser(EndpointParser):
    def __init__(self, data):
        super().__init__(data)

    def parse_line(self,row):
        # Create a Feature for the county
        feature = {
            'type': 'Feature',
            'properties': {
                'county_name': row['attributes']['district_name'],
                'created': row['attributes']['created']
            },
            'geometry': None
        }

        # Check if the county has a polygon
        if row['attributes']['polygon'] is not None:
            feature = self.geometry_parser('Polygon',feature,row)
        # Check if the county has a multipolygon
        elif row['attributes']['multipolygon'] is not None:
            feature = self.geometry_parser('MultiPolygon',feature,row)
        
        if feature:
            return json.dumps(feature)

class AreaParser(EndpointParser):
    def __init__(self, data):
        super().__init__(data)
    
    def parse_line(self,row):
        # Create a Feature for the county
        feature = {
            'type': 'Feature',
            'properties': {
                'nome': row['attributes']['area_name'],
                'created': row['attributes']['created']
            },
            'geometry': None
        }

        # Check if the county has a polygon
        if row['attributes']['polygon'] is not None:
            feature = self.geometry_parser('Polygon',feature,row)
        # Check if the county has a multipolygon
        elif row['attributes']['multipolygon'] is not None:
            feature = self.geometry_parser('MultiPolygon',feature,row)
        
        if feature:
            return json.dumps(feature)
        

class LocationParser(EndpointParser):
    def __init__(self, data):
        super().__init__(data)

    def parse_line(self,row):
        # Create a Feature for the Location
        feature = {
            'type': 'Feature',
            'properties': {
                'nome': row['attributes']['location_name'],
                'created': row['attributes']['created']
            },
            'geometry': None
        }
        
        # Check if the county has a polygon
        if row['attributes']['point'] is not None:
            feature = self.geometry_parser('Point',feature,row)
       
        if feature:
            return json.dumps(feature)
        
    
