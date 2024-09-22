from django.template.loader import render_to_string
from django.shortcuts import render
import json
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import connection
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .serializers import UserSerializer, LocationSerializer,AreaSerializer, DistrictSerializer, CountySerializer, PolygonSerializer, MultiPolygonSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.authtoken.models import Token
from django.views import View
from django.core.files.storage import FileSystemStorage

from .user_data import User_data
from .fetcher import Fetcher
from .models import User,Point, Line, Polygon, MultiPolygon, District,County, Town, Route, Location,Area, Area_property
from .forms import RegisterForm, EditForm

import requests

def update_county(county_name,value):
    County.objects.filter(county_name=county_name).update(pop = value)


def get_properties():
    data = []
    for row in Area_property.objects.all():
        properties = {
            'nome': row.property_name,
            'area_nome': row.area.area_name,
            'value' : row.property_value
        }
        

        data.append(properties)
     
    return data



class indexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts/login')
        
        self.user = request.user
        fetcher = Fetcher(Token.objects.get(user = request.user))
        
        context = {
            'concelhos': fetcher.counties(),
            'distritos': fetcher.districts(),
            'locations' : fetcher.locations(),
            'areas' : fetcher.areas(),
            'properties' : get_properties(),
            'navbar' : render_to_string('essentials/map_navbar.html'),
        }
        
        return render(request, 'dynamiCITY_app/index.html', context)
  

def user_info(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    context = {
        'user' : User.objects.get(pk=request.user.id),
        'mapModalPopUp' : render_to_string('essentials/map_modal_pop_up.html')
    }

    return render(request,'dynamiCITY_app/user_info.html',context)

def register(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.method == 'GET':
        form = { 'form' : RegisterForm() }
        return render(request,'registration/register.html', form)
    elif request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password != confirm_password:
                context = {
                    'form': form, 
                    'message': 'The passwords are not the same, please correct them.',
                }
                return render(request,'registration/register.html', context)
            
            username = request.POST['username']
            password = make_password(password)
            email = request.POST['email']
            is_admin_value = request.POST.get('is_admin')
            if is_admin_value == 'on':
                is_admin = True
            else:
                is_admin = False
            
            
            try:
                if (is_admin):
                    user = User.objects.create(username = username,password=password,email=email,is_superuser=True,is_staff=True,type='admin')
                else:
                    user = User.objects.create(username = username,password=password,email=email)
                
                Token.objects.create(user=user)
                messages.success(request, ('User has been registered!'))
                return redirect('/user')
            except:
                print('error')
                context = {
                    'form': form, 
                    'message': 'Username or Email already exist',
                }
                return render(request,'registration/register.html', context)

def edit_data(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.method == 'GET':
        form = { 'form' : EditForm() }
        return render(request, 'dynamiCITY_app/edit_data.html', form)
    elif request.method == 'POST':
        
        form = EditForm(request.POST)

        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            confirm_password = request.POST['confirm_password']
            user_type = user.type

            if password != confirm_password:
                context = {
                    'form': form,
                    'user': user,
                    'message': 'The passwords are not the same, please correct them.',
                }
                return render(request, 'dynamiCITY_app/edit_data.html', context)
                

            # Modify the user object with the updated data
            if(username != ''):
                user.username = username
            if(email != ''):
                user.email = email
            if(password != '' and password == confirm_password):
                user.password = make_password(password)

            try:
                if user_type == 'admin':
                    # Update additional fields for admin users
                    user.is_superuser = True
                    user.is_staff = True
                    user.type = 'admin'
                else:
                    # Clear additional fields for non-admin users
                    user.is_superuser = False
                    user.is_staff = False
                    user.type = 'user'

                # Save the updated user object
                user.save()

                messages.success(request, 'User updated successfully.')
                return redirect('/user')
            except:
                context = {
                    'form': form,
                    'user': user,
                    'message': 'Username or email already exists.',
                }
                return render(request, 'dynamiCITY_app/edit_data.html', context)



def admin_error(request):
    return render(request,'dynamiCITY_app/admin_error.html')

def show_locations(request):
    context={
        'locations' : Location.objects.all()
    }
    return render(request,'dynamiCITY_app/show_locations.html',context)

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

def request_data():
    url = "https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd=0008273&Dim1=S7A2021&Dim2=1190312&Dim3=T&Dim4=T&lang=PT"
    x = requests.get(url)
    x = x.json()
    x = json.dumps(x, indent=4)
    with open("test.json", "w") as d:
        d.write(x)

def load_areas_data(request):
    User_data.load_user_data()
    return redirect('/')

def clear_areas_data(request):
    User_data.clear_user_data()
    return redirect('/')

def upload_user_data(request):
    return render(request,'user_files/upload.html')


def upload_file(request):
    if 'file' not in request.FILES or 'file2' not in request.FILES:
        context = {
        'message' : 'No file selected',
        }
        return render(request, 'user_files/upload.html',context)
        
         
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        fs.save('file.csv', uploaded_file)
        uploaded_file = request.FILES['file2']
        fs = FileSystemStorage()
        fs.save('properties.csv', uploaded_file)
        User_data.load_user_data()
        return redirect('/')
    context = {
        'message' : 'error uploading file',
    }
    
    return render(context, 'user_files/upload.html')
        




            
#----------------------------- API VIEWS BEGIN -----------------------------
#----------------------------- API VIEW SETS BEGIN -----------------------------
class DistrictViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class CountyViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = County.objects.all()
    serializer_class = CountySerializer

class LocationViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class AreaViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class PolygonViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer

class MultiPolygonViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = MultiPolygon.objects.all()
    serializer_class = MultiPolygonSerializer

class UserPolygonViewSet(
        ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet
        ):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer



#----------------------------- API VIEW SETS END -----------------------------
        
