from django.contrib import admin
from dynamiCITY_app.models import User,Log,Point,Line,Polygon,MultiPolygon,County,District,Town,Route,Location,Area,Area_property

# Register your models here.
admin.site.register(User)
admin.site.register(Log)
admin.site.register(Point)
admin.site.register(Line)
admin.site.register(Polygon)
admin.site.register(MultiPolygon)
admin.site.register(County)
admin.site.register(District)
admin.site.register(Town)
admin.site.register(Route)
admin.site.register(Location)
admin.site.register(Area)
admin.site.register(Area_property)