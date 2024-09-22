from django.urls import path, include

from . import views
from .views import indexView
from rest_framework.authtoken.views import obtain_auth_token
from dynamiCITY_app import views as dynamiCITY_views
from dynamiCITY_app import router 

router = router.DocumentedRouter()
router.register(r'district', dynamiCITY_views.DistrictViewSet, basename='district')
router.register(r'county', dynamiCITY_views.CountyViewSet, basename='county')
router.register(r'location', dynamiCITY_views.LocationViewSet, basename='location')
router.register(r'area', dynamiCITY_views.AreaViewSet, basename='area')
router.register(r'polygon', dynamiCITY_views.PolygonViewSet, basename='polygon')
router.register(r'multipolygon', dynamiCITY_views.MultiPolygonViewSet, basename='multipolygon')
router.register(r'user', dynamiCITY_views.UserPolygonViewSet, basename='user')

urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/token-auth/', obtain_auth_token),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", views.register, name='register'),
    path("accounts/edit", views.edit_data, name='edit'),
    path('user',views.user_info, name='user'),
    path('logout', views.logout_view, name='logout'),
    path("admin_error",views.admin_error, name="admin_error"),
    #path("load_database",views.load_concelhos_temp),
    path('load_data',views.load_areas_data),
    path('clear_data',views.clear_areas_data),
    path('upload_file',views.upload_file),
]