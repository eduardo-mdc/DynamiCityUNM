#This script is purely here for historic reasons, these functions where used in an earlier version of the project for loading the initial json files.


from django.contrib.gis.geos import GEOSGeometry
import json
from ..models import Polygon, MultiPolygon, District,County

def load_concelhos(data):
    for feature in data['features']:

        concelho_name = feature['properties']['NAME_2']
        municipio = feature['properties']['NAME_2']
        geometry_data = feature['geometry']

        if geometry_data['type'] == 'Polygon':
            polygon = Polygon(polygon=GEOSGeometry(json.dumps(geometry_data)))
            polygon.save()
            concelho = County(county_name=concelho_name, polygon=polygon)
            concelho.save()
        elif geometry_data['type'] == 'MultiPolygon':
            multipolygon = MultiPolygon(multipolygon=GEOSGeometry(json.dumps(geometry_data)))
            multipolygon.save()
            concelho = County(county_name=concelho_name, multipolygon=multipolygon)
            concelho.save()


def load_distritos(data):
    for feature in data['features']:

        nome = feature['properties']['NAME_1']
        geometry_data = feature['geometry']

        if geometry_data['type'] == 'Polygon':
            polygon = Polygon(polygon=GEOSGeometry(json.dumps(geometry_data)))
            polygon.save()
            distrito = District(district_name=nome, polygon=polygon)
            distrito.save()
        elif geometry_data['type'] == 'MultiPolygon':
            multipolygon = MultiPolygon(multipolygon=GEOSGeometry(json.dumps(geometry_data)))
            multipolygon.save()
            distrito = District(district_name=nome, multipolygon=multipolygon)
            distrito.save()

def load_concelhos_temp(request):
    concelhos = County.objects.all()
    concelhos.delete()
    
    with open('dynamiCITY_app/concelhos.geojson') as f:
        data = json.load(f)

    load_concelhos(data)

    distritos = District.objects.all()
    distritos.delete()

    with open('dynamiCITY_app/distritos.geojson') as f:
        data = json.load(f)
    
    load_distritos(data)


    # Gerar a URL de destino usando o nome da view
    url = reverse('index')

    # Redirecionar para outra página

    return redirect(url)

