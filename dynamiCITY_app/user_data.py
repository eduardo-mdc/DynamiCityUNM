import json
import csv
import os
from django.contrib.gis.geos import GEOSGeometry

from .models import Polygon, MultiPolygon, Area, Area_property

class User_data:

  def csv_to_geojson(csv_file_path, geojson_file_path):
    data={}
    data["type"] = "FeatureCollection"
    features = []
    
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=';')
        for row in reader:
            dict = {}
            dict['type'] = "Feature"
            dict["geometry"] = {}
            geometryString = row["geometry"].split(",")
            geometry = []
            type = ""
            multipolygon =[]
            for s in geometryString:
                if s[0] == 'P':
                    type = "Polygon"
                    s2 = s.split('(')
                    s3 = s2[2].split(' ')
                    c1 = float(s3[0])
                    c2 = float(s3[1])
                    geometry.append((c1,c2))
                elif s[0] == 'M':
                    type = "MultiPolygon"
                    s2 = s.split('(')
                    s3 = s2[3].split(' ')
                    c1 = float(s3[0])
                    c2 = float(s3[1]) 
                    multipolygon.append((c1,c2))
                else:
                    if type == "Polygon":
                        if s[len(s)-1] == ')':
                            s2 = s.split(' ')
                            c1 = float(s2[1])
                            s3 = s2[2].split(')')
                            c2 = float(s3[0])
                        else:
                            s2 = s.split(' ')
                            c1 = float(s2[1])
                            c2 = float(s2[2])
                        geometry.append((c1,c2))
                    else:
                        if(s[len(s)-1]) == ')':
                            s2 = s.split(' ')
                            s3 = s2[2].split(')')
                            c1 = float(s2[1])
                            c2 = float(s3[0])
                            multipolygon.append((c1,c2))
                            geometry.append(multipolygon)
                            multipolygon = []
                        elif s[1] == '(':
                            s2 = s.split(' ')
                            s3 = s2[1].split('(')
                            c1 = float(s3[2])
                            c2 = float(s2[2])
                            multipolygon.append((c1,c2))
                        else:
                            s2 = s.split(' ')
                            c1 = float(s2[1])
                            c2 = float(s2[2])
                            multipolygon.append((c1,c2))
            dict["geometry"]["type"] = type
            dict["geometry"]["coordinates"] = [geometry]
            dict["properties"] = {}
            
            
            for key in row.keys():
                if key != "geometry":
                    dict["properties"][key] = row[key]
                    
            features.append(dict)

    data["features"] = features
           
    with open(geojson_file_path,'w') as jsonfile:
        jsonString = json.dumps(data, indent=4)
        jsonfile.write(jsonString)


  def load_geojson_data(geojson_file_path):
    Area_property.objects.all().delete()
    Area.objects.all().delete()
    with open(geojson_file_path,'r') as jsonFile:
        data = json.loads(jsonFile.read())
        
        for feature in data['features']:
            geometry_data = feature['geometry']
            nome = feature['properties']['sccode']

            if geometry_data['type'] == 'Polygon':
                polygon = Polygon(polygon=GEOSGeometry(json.dumps(geometry_data)))
                polygon.save()
                area = Area(area_name=nome, polygon=polygon)
                area.save()
            elif geometry_data['type'] == 'MultiPolygon':
                multipolygon = MultiPolygon(multipolygon=GEOSGeometry(json.dumps(geometry_data)))
                multipolygon.save()
                area = Area(area_name=nome, multipolygon=multipolygon)
                area.save()


  def csv_to_json(csv_file_path, json_file_path):
    data = {}
    data["type"] = "Area_list"
    data["Area_list"] = []
    with open(csv_file_path,'r') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        for row in reader:
            dict ={}
            dict["sccode"] = row["sccode"]
            dict["Properties"] = {}
            for key in row.keys():
                if key != "sccode":
                    dict["Properties"][key] = row[key]
            
            data["Area_list"].append(dict)

    with open(json_file_path, 'w')as jsonfile:
        jsonString = json.dumps(data, indent=4)
        jsonfile.write(jsonString)

  def load_properties_json(json_file_path):
    Area_property.objects.all().delete()
    with open(json_file_path,'r') as jsonFile:
        data = json.loads(jsonFile.read())
        
        for area in data['Area_list']:
            area_model = Area.objects.get(area_name = area['sccode'])
            for property in area['Properties'].keys():
                area_property = Area_property(property_name = property,area = area_model,property_value = area['Properties'][property])
                area_property.save()

  def remove_files():
    if os.path.exists('file.csv'):
        os.remove('file.csv')
    if os.path.exists('file.geojson'):
        os.remove('file.geojson')
    if os.path.exists('properties.csv'):
        os.remove('properties.csv')
    if os.path.exists('properties.json'):
        os.remove('properties.json')


  def load_user_data():
    User_data.csv_to_geojson('file.csv','file.geojson')
    User_data.load_geojson_data('file.geojson')
    User_data.csv_to_json('properties.csv','properties.json')
    User_data.load_properties_json('properties.json')
    User_data.remove_files()

  def clear_user_data():
      Area_property.objects.all().delete()
      Area.objects.all().delete()