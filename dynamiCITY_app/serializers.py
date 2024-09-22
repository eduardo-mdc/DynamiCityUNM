from . import models
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from django.contrib.gis.geos import GEOSGeometry

from django.contrib.gis.db.models.fields  import PointField, LineStringField, PolygonField, MultiPolygonField


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = (
			'username',
			'type',
			'email'
		)


class PolygonSerializer(serializers.Serializer):
    polygon = serializers.SerializerMethodField()

    def get_polygon(self, polygon_obj):
        return polygon_obj.polygon.wkt

    class Meta:
        model = models.Polygon
        fields = (
            'polygon',
        )
	
class MultiPolygonSerializer(serializers.Serializer):
    multipolygon = serializers.SerializerMethodField()

    def get_multipolygon(self, multipolygon_obj):
        return multipolygon_obj.multipolygon.wkt

    class Meta:
        model = models.MultiPolygon
        fields = (
            'multipolygon',
        )

class CountySerializer(serializers.ModelSerializer):
    
    polygon = serializers.SerializerMethodField()
    multipolygon = serializers.SerializerMethodField()
    
    def get_polygon(self, county):
        if county.polygon is not None:
            return GEOSGeometry(county.polygon.polygon).wkt
        else:
            return None
    
    def get_multipolygon(self, county):
        if county.multipolygon is not None:
            return GEOSGeometry(county.multipolygon.multipolygon).wkt
        else:
            return None
    
    class Meta:
        model = models.County
        fields = (
            'id',
            'county_name',
            'created',
            'polygon',
            'multipolygon',
        )


class DistrictSerializer(serializers.ModelSerializer):
    
    polygon = serializers.SerializerMethodField()
    multipolygon = serializers.SerializerMethodField()
    
    def get_polygon(self, district):
        if district.polygon is not None:
            return GEOSGeometry(district.polygon.polygon).wkt
        else:
            return None
    
    def get_multipolygon(self, district):
        if district.multipolygon is not None:
            return GEOSGeometry(district.multipolygon.multipolygon).wkt
        else:
            return None
    
    class Meta:
        model = models.District
        fields = (
            'id',
            'district_name',
            'created',
            'polygon',
            'multipolygon',
        )
	

class TownSerializer(serializers.ModelSerializer):
    polygon = serializers.SerializerMethodField()
    multipolygon = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Town
        fields = (
            'id',
            'town_name',
            'created',
            'polygon',
            'multipolygon',
        )

class AreaSerializer(serializers.ModelSerializer):
    polygon = serializers.SerializerMethodField()
    multipolygon = serializers.SerializerMethodField()
     
    def get_polygon(self, area):
        if area.polygon is not None:
            return GEOSGeometry(area.polygon.polygon).wkt
        else:
            return None
    
    def get_multipolygon(self, area):
        if area.multipolygon is not None:
            return GEOSGeometry(area.multipolygon.multipolygon).wkt
        else:
            return None

    class Meta:
        model = models.Area
        fields = (
            'id',
            'area_name',
            'created',
            'polygon',
            'multipolygon',
        )
	
class LocationSerializer(serializers.ModelSerializer):
    point = serializers.SerializerMethodField()

    def get_point(self, location):
        if location.point is not None:
            return GEOSGeometry(location.point.point).wkt
        else:
            return None

    class Meta:
        model = models.Location
        fields = (
            'id',
            'location_name',
            'created',
            'point',
        )