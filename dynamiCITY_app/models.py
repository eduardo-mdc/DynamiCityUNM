from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
)

class User(
    AbstractUser,
    TimeStampedModel, 
	ActivatorModel,
    ):

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique= True)
    password = models.CharField(max_length=512)
    type = models.CharField(max_length=100 ,default='user')
    created = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
	    return f'{self.username}'


class Log(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank=True)
    created = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = 'Logs'
    
    def __str__(self):
	    return f'{self.user}' + ' ' + f'{self.content}'


class Point(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    point = gis_models.PointField()
    created = models.DateTimeField(default=timezone.now)

    
    class Meta:
        verbose_name_plural = 'Points'

class Line(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    line = gis_models.LineStringField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Lines'

class Polygon(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    polygon = gis_models.PolygonField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Polygons'

class MultiPolygon(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    multipolygon = gis_models.MultiPolygonField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'MultiPolygons'

class Area(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    area_name = models.CharField(max_length=100)
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, null=True, blank=True)
    multipolygon = models.ForeignKey(MultiPolygon, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = 'Areas'

    def __str__(self):
	    return f'{self.area_name}'

class County(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    county_name = models.CharField(max_length=100)
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, null=True, blank=True)
    multipolygon = models.ForeignKey(MultiPolygon, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = 'Counties'

    def __str__(self):
	    return f'{self.county_name}'

class District(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    district_name = models.CharField(max_length=100)
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, null=True, blank=True)
    multipolygon = models.ForeignKey(MultiPolygon, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Districts'
    
    def __str__(self):
	    return f'{self.district_name}'

class Town(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    town_name = models.CharField(max_length=100)
    polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE, null=True, blank=True)
    multipolygon = models.ForeignKey(MultiPolygon, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Towns'
    
    def __str__(self):
	    return f'{self.town_name}'
    

class Route(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):
    
    rounte_name = models.CharField(max_length=100)
    line = models.ForeignKey(Line, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Routes'
    
    def __str__(self):
	    return f'{self.rounte_name}'
    
class Location(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
    ):

    location_name = models.CharField(max_length=100)
    point = models.ForeignKey(Point, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Locations'
    
    def __str__(self):
	    return f'{self.location_name}'
    
class Area_property(
    TimeStampedModel, 
	ActivatorModel,
    models.Model,
):
    property_name = models.CharField(max_length=100)
    area = models.ForeignKey(Area,  on_delete=models.CASCADE)
    property_value = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Area_properties'
    
    def __str__(self):
	    return f'{self.property_name}'