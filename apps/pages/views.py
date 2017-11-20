from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.http import HttpResponse
from django.template import Context, Template, RequestContext
from django.db.models import Prefetch

# Create your views here.

from django.http import HttpResponse

import apps.common.functions
from apps.objects.models import Node
from .models import Page, School, Department
from apps.taxonomy.models import Location, City, State, Zipcode
from apps.images.models import Thumbnail

# from apps.schools.models import School
# from apps.departments.models import Department
# from apps.news.models import News, NewsYear
from apps.users.models import Employee

def home(request):
  page = get_object_or_404(Page, url='/home/')
  pageopts = page._meta
  # news = News.objects.all().filter(deleted=0).filter(published=1).order_by('-pinned','-author_date')[0:5]
  result = render(request, 'pages/home.html', {'page': page,'pageopts': pageopts,})
  return result

# def news(request):
#   page = get_object_or_404(Page, url=request.path)
#   pageopts = page._meta
#   newsyears = NewsYear.objects.all().order_by('-yearend')
#   return render(request, 'pages/news/newsyears.html', {'page': page,'pageopts': pageopts,'newsyears': newsyears})

def schools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  elementary_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Elementary Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  k8_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='K-8 Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  middle_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Middle Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  high_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='High Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  charter_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Charter Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/main_school_directory.html', {'page': page,'pageopts': pageopts, 'elementary_schools_directory': elementary_schools_directory, 'k8_schools_directory': k8_schools_directory,'middle_schools_directory': middle_schools_directory,'high_schools_directory': high_schools_directory,'charter_schools_directory': charter_schools_directory})
  return result

# def temp(request):
#   schools = School.objects.filter(deleted=0).filter(published=1).order_by('title')
#   return render(request, 'pages/schools/temp.html', {'schools': schools,})

def elementaryschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Elementary Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def k8schools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='K-8 Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def middleschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Middle Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def highschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='High Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def charterschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Charter Schools').order_by('title').only('title','building_location','website_url','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def schooldetail(request):
  page = get_object_or_404(School, url=request.path)
  pageopts = page._meta
  return render(request, 'pages/schools/schooldetail.html', {'page': page,'pageopts': pageopts,})
  result = Template( template.content ).render(context=RequestContext(request, {'page': page,'pageopts': pageopts,}))
  return HttpResponse(result)

def departments(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  departments = Department.objects.filter(deleted=0).filter(published=1).order_by('title')
  return render(request, 'pages/departments/department_directory.html', {'page': page,'pageopts': pageopts, 'departments': departments})

def departmentdetail(request):
    page = get_object_or_404(Department, url=request.path)
    pageopts = page._meta
    department_children = Department.objects.filter(parent__url=request.path)
    return render(request, 'pages/departments/departmentdetail.html', {'page': page,'pageopts': pageopts,'department_children': department_children})

def directory(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    people = Employee.objects.filter(is_active=1).filter(is_staff=1).filter(in_directory=1).order_by('last_name').only('last_name','first_name','job_title','email','department').prefetch_related(Prefetch('department',queryset=Node.objects.only('node_title','url')))
    return render(request, 'pages/directory/directory.html', {'page': page,'pageopts': pageopts, 'people': people})

def directory_letter(request, letter):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    people = Employee.objects.filter(is_active=1).filter(is_staff=1).filter(in_directory=1).filter(last_name__istartswith=letter).order_by('last_name').only('last_name','first_name','job_title','email','department').prefetch_related(Prefetch('department',queryset=Node.objects.only('node_title','url')))
    return render(request, 'pages/directory/directory_letter.html', {'page': page,'pageopts': pageopts, 'people': people})

# def calendars(request):
#   page = get_object_or_404(Page, url=request.path)
#   pageopts = page._meta
#   return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})
