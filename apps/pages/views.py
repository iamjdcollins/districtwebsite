from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.http import HttpResponse
from django.template import Context, Template, RequestContext
from django.db.models import Prefetch
from django.utils import timezone

# Create your views here.

from django.http import HttpResponse

import apps.common.functions
from apps.objects.models import Node, User
from .models import Page, School, Department, Board, BoardSubPage, News, NewsYear, SubPage, BoardMeetingYear, DistrictCalendarYear,SuperintendentMessage,SuperintendentMessageYear
from apps.taxonomy.models import Location, City, State, Zipcode, Language, BoardPrecinct, BoardPolicySection
from apps.images.models import Thumbnail, NewsThumbnail, ContentBanner, ProfilePicture, DistrictLogo
from apps.directoryentries.models import Staff, SchoolAdministrator, Administrator,  BoardMember, StudentBoardMember, BoardPolicyAdmin
from apps.links.models import ResourceLink, ActionButton
from apps.documents.models import Document, BoardPolicy, Policy, AdministrativeProcedure, SupportingDocument
from apps.files.models import File
from apps.events.models import BoardMeeting, DistrictCalendarEvent
from apps.users.models import Employee
from apps.contactmessages.forms import ContactMessageForm

def home(request):
  page = get_object_or_404(Page, url='/home/')
  pageopts = page._meta
  supermessage = SuperintendentMessage.objects.filter(deleted=0).filter(published=1).order_by('-author_date').only('title','author_date','summary','url')[:1]
  news = News.objects.all().filter(deleted=0).filter(published=1).order_by('-pinned','-author_date').only('title','author_date','summary','url').prefetch_related(Prefetch('images_newsthumbnail_node', queryset = NewsThumbnail.objects.only('image_file','alttext','related_node_id')))[0:5]
  result = render(request, 'pages/home.html', {'page': page,'pageopts': pageopts,'news': news,'supermessage':supermessage})
  return result

def news(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    newsyears = NewsYear.objects.all().order_by('-yearend')
    return render(request, 'pages/news/newsyears.html', {'page': page,'pageopts': pageopts,'newsyears': newsyears})

def NewsYearArchive(request):
    page = NewsYear.objects.filter(url=request.path).first()
    pageopts = page._meta
    news = News.objects.filter(parent__url=request.path).filter(deleted=0).filter(published=1).only('title','author_date','summary','url').prefetch_related(Prefetch('images_newsthumbnail_node', queryset = NewsThumbnail.objects.only('image_file','alttext','related_node_id')))
    newsmonths = [
        {'month': 'June', 'news': [],},
        {'month': 'May', 'news': [],},
        {'month': 'April', 'news': [],},
        {'month': 'March', 'news': [],},
        {'month': 'February', 'news': [],},
        {'month': 'January', 'news': [],},
        {'month': 'December', 'news': [],},
        {'month': 'November', 'news': [],},
        {'month': 'October', 'news': [],},
        {'month': 'September', 'news': [],},
        {'month': 'August', 'news': [],},
        {'month': 'July', 'news': [],},
    ]
    for item in news:
        if item.author_date.month == 6:
            newsmonths[0]['news'].append(item)
        if item.author_date.month == 5:
            newsmonths[1]['news'].append(item)
        if item.author_date.month == 4:
            newsmonths[2]['news'].append(item)
        if item.author_date.month == 3:
            newsmonths[3]['news'].append(item)
        if item.author_date.month == 2:
            newsmonths[4]['news'].append(item)
        if item.author_date.month == 1:
            newsmonths[5]['news'].append(item)
        if item.author_date.month == 12:
            newsmonths[6]['news'].append(item)
        if item.author_date.month == 11:
            newsmonths[7]['news'].append(item)
        if item.author_date.month == 10:
            newsmonths[8]['news'].append(item)
        if item.author_date.month == 9:
            newsmonths[9]['news'].append(item)
        if item.author_date.month == 8:
            newsmonths[10]['news'].append(item)
        if item.author_date.month == 7:
            newsmonths[11]['news'].append(item)
    #newsmonths = [
    #    {'month': 'June', 'news': News.objects.filter(author_date__month=6).filter(parent__url=request.path).filter(deleted=0).filter(published=1)},
    #    {'month': 'May', 'news': News.objects.filter(author_date__month=5).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'April', 'news': News.objects.filter(author_date__month=4).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'March', 'news': News.objects.filter(author_date__month=3).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'February', 'news': News.objects.filter(author_date__month=2).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'January', 'news': News.objects.filter(author_date__month=1).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'December', 'news': News.objects.filter(author_date__month=12).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'November', 'news': News.objects.filter(author_date__month=11).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'October', 'news': News.objects.filter(author_date__month=10).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'September', 'news': News.objects.filter(author_date__month=9).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'August', 'news': News.objects.filter(author_date__month=8).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #    {'month': 'July', 'news': News.objects.filter(author_date__month=7).filter(parent__url=request.path).filter(deleted=0).filter(published=1),},
    #]
    return render(request, 'pages/news/yeararchive.html', {'page': page, 'pageopts': pageopts, 'news': news, 'newsmonths': newsmonths})

def NewsArticleDetail(request):
    pages =  News.objects.filter(published=1).filter(deleted=0)
    page = get_object_or_404(pages, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/news/articledetail.html', {'page': page, 'pageopts': pageopts})

def schools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  elementary_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Elementary Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  k8_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='K-8 Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  middle_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Middle Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  high_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='High Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  charter_schools_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Charter Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  community_learning_centers_directory = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Community Learning Centers').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/main_school_directory.html', {'page': page,'pageopts': pageopts, 'elementary_schools_directory': elementary_schools_directory, 'k8_schools_directory': k8_schools_directory,'middle_schools_directory': middle_schools_directory,'high_schools_directory': high_schools_directory,'charter_schools_directory': charter_schools_directory,'community_learning_centers_directory': community_learning_centers_directory})
  return result

# def temp(request):
#   schools = School.objects.filter(deleted=0).filter(published=1).order_by('title')
#   return render(request, 'pages/schools/temp.html', {'schools': schools,})

def elementaryschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Elementary Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def k8schools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='K-8 Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def middleschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Middle Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def highschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='High Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def charterschools(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Charter Schools').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def communitylearningcenters(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  schools = School.objects.filter(deleted=0).filter(published=1).filter(schooltype__title='Community Learning Centers').order_by('title').only('title','building_location','website_url','scc_url','calendar_url','boundary_map','url','main_phone').prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))),Prefetch('images_thumbnail_node', queryset = Thumbnail.objects.only('image_file','alttext','related_node_id')))
  result = render(request, 'pages/schools/school_directory.html', {'page': page,'pageopts': pageopts, 'schools': schools})
  return result

def school_handbooks(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def district_demographics(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def schooldetail(request):
  page = get_object_or_404(School, url=request.path)
  pageopts = page._meta
  return render(request, 'pages/schools/schooldetail.html', {'page': page,'pageopts': pageopts,})
  result = Template( template.content ).render(context=RequestContext(request, {'page': page,'pageopts': pageopts,}))
  return HttpResponse(result)

def departments(request):
  page = get_object_or_404(Page, url=request.path)
  pageopts = page._meta
  all_departments = Department.objects.filter(deleted=0).filter(published=1).order_by('title').only('title','building_location','url','main_phone','short_description','is_department',).prefetch_related(Prefetch('building_location',queryset=Location.objects.only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.only('title')),Prefetch('location_state', queryset = State.objects.only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.only('title')))))
  departments = {
      'departments':[],
      'programs':[]
  }
  for department in all_departments:
      if department.is_department:
          departments['departments'].append(department)
      else:
          departments['programs'].append(department)
  
  return render(request, 'pages/departments/department_directory.html', {'page': page,'pageopts': pageopts, 'departments': departments})

def departmentdetail(request):
    template = None
    context = {}

    department = Department.objects.filter(deleted=0).filter(published=1).filter(url=request.path).only('title','body','building_location','main_phone','main_fax').prefetch_related(Prefetch('building_location',queryset=Location.objects.filter(deleted=0).filter(published=1).only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_state', queryset = State.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('title')))),Prefetch('images_contentbanner_node', queryset = ContentBanner.objects.filter(deleted=0).filter(published=1).only('image_file','alttext','inline_order','related_node_id')),Prefetch('links_actionbutton_node', queryset = ActionButton.objects.filter(deleted=0).filter(published=1).only('title','link_url','inline_order','related_node')),Prefetch('directoryentries_administrator_node',queryset=Administrator.objects.filter(deleted=0).filter(published=1).only('employee','job_title','inline_order','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('last_name','first_name','email','job_title')))),Prefetch('directoryentries_staff_node',queryset=Staff.objects.filter(deleted=0).filter(published=1).only('employee','job_title','inline_order','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('last_name','first_name','email','job_title')))),Prefetch('links_resourcelink_node',queryset=ResourceLink.objects.filter(deleted=0).filter(published=1).only('title','link_url','inline_order','related_node')),Prefetch('documents_document_node',queryset=Document.objects.filter(deleted=0).filter(published=1).only('pk','title','inline_order','related_node').prefetch_related(Prefetch('files_file_node',queryset=File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))),Prefetch('pages_subpage_node', queryset = SubPage.objects.filter(deleted=0).filter(published=1).only('title','url','inline_order','related_node_id'))).first()
    subpage = SubPage.objects.filter(deleted=0).filter(published=1).filter(url=request.path).only('title','body','building_location','main_phone','main_fax').prefetch_related(Prefetch('building_location',queryset=Location.objects.filter(deleted=0).filter(published=1).only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_state', queryset = State.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('title')))),Prefetch('images_contentbanner_node', queryset = ContentBanner.objects.filter(deleted=0).filter(published=1).only('image_file','alttext','inline_order','related_node_id')),Prefetch('links_actionbutton_node', queryset = ActionButton.objects.filter(deleted=0).filter(published=1).only('title','link_url','inline_order','related_node')),Prefetch('directoryentries_administrator_node',queryset=Administrator.objects.filter(deleted=0).filter(published=1).only('employee','job_title','inline_order','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('last_name','first_name','email','job_title')))),Prefetch('directoryentries_staff_node',queryset=Staff.objects.filter(deleted=0).filter(published=1).only('employee','job_title','inline_order','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('last_name','first_name','email','job_title')))),Prefetch('links_resourcelink_node',queryset=ResourceLink.objects.filter(deleted=0).filter(published=1).only('title','link_url','inline_order','related_node')),Prefetch('documents_document_node',queryset=Document.objects.filter(deleted=0).filter(published=1).only('pk','title','inline_order','related_node').prefetch_related(Prefetch('files_file_node',queryset=File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title'))))))).first()
    if department:
        page = department
        context['page'] = page
    elif subpage:
        page = subpage
        context['page'] = page
    pageopts = page._meta
    context['pageopts'] = pageopts
    department_children = Department.objects.filter(deleted=0).filter(published=1).filter(parent__url=request.path).order_by('title').only('pk','title','short_description','main_phone','building_location','content_type','menu_title','url').prefetch_related(Prefetch('building_location',queryset=Location.objects.filter(deleted=0).filter(published=1).only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_state', queryset = State.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('title')))))
    context['department_children'] = department_children
    if request.path == '/departments/communications-and-community-relations/district-logo/':
        all_logos = DistrictLogo.objects.filter(deleted=0).filter(published=1).order_by('district_logo_group__lft','district_logo_style_variation__lft')
        districtlogos = {
            'primary':[],
            'primaryrev':[],
            'secondary':[],
            'secondaryrev':[],
            'wordmark':[],
        }
        for logo in all_logos:
            if logo.district_logo_group.title == 'Primary Logo':
                districtlogos['primary'].append(logo)
            if logo.district_logo_group.title == 'Primary Logo Reversed':
                districtlogos['primaryrev'].append(logo)
            if logo.district_logo_group.title == 'Secondary Logo':
                districtlogos['secondary'].append(logo)
            if logo.district_logo_group.title == 'Secondary Logo Reversed':
                districtlogos['secondaryrev'].append(logo)
            if logo.district_logo_group.title == 'Wordmark':
                districtlogos['wordmark'].append(logo)
        context['districtlogos'] = districtlogos
    if not template:
        template = 'pages/departments/departmentdetail.html'
    return render(request, template, context)

def superintendents_message(request):
    currentyear = apps.common.functions.currentyear()
    if request.path == '/departments/superintendents-office/superintendents-message/':
        try:
            year = SuperintendentMessageYear.objects.get(title=currentyear['currentyear']['long'])
        except SuperintendentMessageYear.DoesNotExist:
            message, created = SuperintendentMessage.objects.get_or_create(author_date=timezone.now())
            if created:
                message.save()
                message.delete()
                message.delete()
            year = SuperintendentMessageYear.objects.get(title=currentyear['currentyear']['long'])
        return redirect(year.url)

def superintendents_message_yeararchive(request):
    page = SuperintendentMessageYear.objects.filter(url=request.path).first()
    pageopts = page._meta
    superintendent_messages = SuperintendentMessage.objects.filter(parent__url=request.path).filter(deleted=0).filter(published=1).only('title','author_date','summary','url').prefetch_related(Prefetch('images_newsthumbnail_node', queryset = NewsThumbnail.objects.only('image_file','alttext','related_node_id')))
    messagemonths = [
        {'month': 'June', 'message': [],},
        {'month': 'May', 'message': [],},
        {'month': 'April', 'message': [],},
        {'month': 'March', 'message': [],},
        {'month': 'February', 'message': [],},
        {'month': 'January', 'message': [],},
        {'month': 'December', 'message': [],},
        {'month': 'November', 'message': [],},
        {'month': 'October', 'message': [],},
        {'month': 'September', 'message': [],},
        {'month': 'August', 'message': [],},
        {'month': 'July', 'message': [],},
    ]
    for item in superintendent_messages:
        if item.author_date.month == 6:
            messagemonths[0]['message'].append(item)
        if item.author_date.month == 5:
            messagemonths[1]['message'].append(item)
        if item.author_date.month == 4:
            messagemonths[2]['message'].append(item)
        if item.author_date.month == 3:
            messagemonths[3]['message'].append(item)
        if item.author_date.month == 2:
            messagemonths[4]['message'].append(item)
        if item.author_date.month == 1:
            messagemonths[5]['message'].append(item)
        if item.author_date.month == 12:
            messagemonths[6]['message'].append(item)
        if item.author_date.month == 11:
            messagemonths[7]['message'].append(item)
        if item.author_date.month == 10:
            messagemonths[8]['message'].append(item)
        if item.author_date.month == 9:
            messagemonths[9]['message'].append(item)
        if item.author_date.month == 8:
            messagemonths[10]['message'].append(item)
        if item.author_date.month == 7:
            messagemonths[11]['message'].append(item)
    return render(request, 'pages/news/yeararchive.html', {'page': page, 'pageopts': pageopts, 'superintendent_messages': superintendent_messages, 'messagemonths': messagemonths})

def superintendents_message_detail(request):
    pages =  SuperintendentMessage.objects.filter(published=1).filter(deleted=0)
    page = get_object_or_404(pages, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/news/articledetail.html', {'page': page, 'pageopts': pageopts})

def superintendents_downloads(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def directory(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    people = Employee.objects.filter(is_active=1).filter(is_staff=1).filter(in_directory=1).order_by('last_name').only('pk','last_name','first_name','job_title','email','department').prefetch_related(Prefetch('department',queryset=Node.objects.only('node_title','url')))
    return render(request, 'pages/directory/directory.html', {'page': page,'pageopts': pageopts, 'people': people})

def directory_letter(request, letter):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    people = Employee.objects.filter(is_active=1).filter(is_staff=1).filter(in_directory=1).filter(last_name__istartswith=letter).order_by('last_name').only('pk','last_name','first_name','job_title','email','department').prefetch_related(Prefetch('department',queryset=Node.objects.only('node_title','url')))
    return render(request, 'pages/directory/directory_letter.html', {'page': page,'pageopts': pageopts, 'people': people})

def calendars(request):
    currentyear = apps.common.functions.currentyear()
    if request.path == '/calendars/':
        try:
            year = DistrictCalendarYear.objects.get(title=currentyear['currentyear']['long'])
        except DistrictCalendarYear.DoesNotExist:
            event, created = DistrictCalendarEvent.objects.get_or_create(startdate=timezone.now())
            if created:
                event.save()
                event.delete()
                event.delete()
            year = DistrictCalendarYear.objects.get(title=currentyear['currentyear']['long'])
        return redirect(year.url)
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def calendarguide(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def districtcalendaryearsarchive(request):
    page = get_object_or_404(DistrictCalendarYear, url=request.path)
    pageopts = page._meta
    districtcalendaryears = DistrictCalendarYear.objects.filter(deleted=0).filter(published=1).order_by('-yearend')
    districtcalendarevents = DistrictCalendarEvent.objects.filter(deleted=0).filter(published=1).filter(parent__url=request.path)
    return render(request, 'pages/calendars/districtcalendaryears.html', {'page': page, 'pageopts': pageopts,'districtcalendaryears': districtcalendaryears,'districtcalendarevents': districtcalendarevents})

def employees(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def search(request):
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    return render(request, 'pages/pagedetail.html', {'page': page,'pageopts': pageopts})

def boarddetail(request):
  context = {}
  currentyear = apps.common.functions.currentyear()
  if request.path == '/board-of-education/board-meetings/':
      try:
          year = BoardMeetingYear.objects.get(title=currentyear['currentyear']['long'])
      except BoardMeetingYear.DoesNotExist:
          meeting, created = BoardMeeting.objects.get_or_create(startdate=timezone.now())
          if created:
              meeting.save()
              meeting.delete()
              meeting.delete() 
          year = BoardMeetingYear.objects.get(title=currentyear['currentyear']['long'])
      return redirect(year.url)
  board = Board.objects.filter(url=request.path).only('pk','title','body','building_location','main_phone','main_fax','mission_statement','vision_statement').prefetch_related(Prefetch('building_location',queryset=Location.objects.filter(deleted=0).filter(published=1).only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_state', queryset = State.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('title')))),Prefetch('images_contentbanner_node', queryset = ContentBanner.objects.filter(deleted=0).filter(published=1).only('image_file','alttext','related_node_id')),Prefetch('directoryentries_boardmember_node',queryset=BoardMember.objects.filter(deleted=0).filter(published=1).order_by('precinct__title').only('employee','precinct','phone','street_address','city','state','zipcode','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('last_name','first_name','email').prefetch_related(Prefetch('images_profilepicture_node',ProfilePicture.objects.filter(deleted=0).filter(published=1).only('image_file','alttext','related_node_id')))),Prefetch('precinct', queryset = BoardPrecinct.objects.filter(deleted=0).filter(published=1).only('pk','title').order_by('title')),Prefetch('city', queryset = City.objects.filter(deleted=0).filter(published=1).only('pk','title')),Prefetch('state', queryset = State.objects.filter(deleted=0).filter(published=1).only('pk','title')),Prefetch('zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('pk','title')))),Prefetch('directoryentries_studentboardmember_node',queryset=StudentBoardMember.objects.filter(deleted=0).filter(published=1).order_by('title').only('first_name','last_name','phone','building_location','related_node').prefetch_related(Prefetch('building_location',queryset=Location.objects.filter(deleted=0).filter(published=1).only('street_address','location_city','location_state','location_zipcode','google_place').prefetch_related(Prefetch('location_city', queryset = City.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_state', queryset = State.objects.filter(deleted=0).filter(published=1).only('title')),Prefetch('location_zipcode', queryset = Zipcode.objects.filter(deleted=0).filter(published=1).only('title')))),Prefetch('images_profilepicture_node',ProfilePicture.objects.filter(deleted=0).filter(published=1).only('image_file','alttext','related_node_id'))))).first()
  boardsubpage = BoardSubPage.objects.filter(url=request.path).first()
  if board:
    page = board
    context['page'] = page
  elif boardsubpage:
    page = boardsubpage
    context['page'] = page
  pageopts = page._meta
  context['pageopts'] = pageopts
  if request.path == '/board-of-education/policies/':
      district_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).order_by('section__lft','index').only('pk','policy_title','index','section','related_node').prefetch_related(Prefetch('section', queryset= BoardPolicySection.objects.filter(deleted=0).filter(published=1).only('pk','section_prefix','description')),Prefetch('directoryentries_boardpolicyadmin_node',queryset=BoardPolicyAdmin.objects.filter(deleted=0).filter(published=1).order_by('title').only('pk','employee','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('pk','last_name','first_name')))),Prefetch('documents_policy_node', queryset = Policy.objects.filter(deleted=0).filter(published=1).only('pk','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))),Prefetch('documents_administrativeprocedure_node', queryset = AdministrativeProcedure.objects.filter(deleted=0).filter(published=1).only('pk','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))),Prefetch('documents_supportingdocument_node', queryset = SupportingDocument.objects.filter(deleted=0).filter(published=1).only('pk','document_title','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))))
      board_policies = []
      community_policies = []
      financial_policies = []
      general_policies = []
      instructional_policies = []
      personnel_policies = []
      student_policies = []
      for policy in district_policies:
          if policy.section.title == 'Board Policies':
              board_policies.append(policy)
          if policy.section.title == 'Community Policies':
              community_policies.append(policy)
          if policy.section.title == 'Financial Policies':
              financial_policies.append(policy)
          if policy.section.title == 'General Policies':
              general_policies.append(policy)
          if policy.section.title == 'Instructional Policies':
              instructional_policies.append(policy)
          if policy.section.title == 'Personnel Policies':
              personnel_policies.append(policy)
          if policy.section.title == 'Student Policies':
              student_policies.append(policy)
      context['board_policies'] = board_policies
      context['community_policies'] = community_policies
      context['financial_policies'] = financial_policies
      context['general_policies'] = general_policies
      context['instructional_policies'] = instructional_policies
      context['personnel_policies'] = personnel_policies
      context['student_policies'] = student_policies
          
  #board_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Board Policies').order_by('section__lft','index')
  #community_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Community Policies').order_by('section__lft','index')
  #financial_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Financial Policies').order_by('section__lft','index')
  #general_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='General Policies').order_by('section__lft','index')
  #instructional_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Instructional Policies').order_by('section__lft','index')
  #personnel_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Personnel Policies').order_by('section__lft','index')
  #student_policies = BoardPolicy.objects.filter(deleted=0).filter(published=1).filter(section__title='Student Policies').order_by('section__lft','index')
  board_meeting_years = BoardMeetingYear.objects.filter(deleted=0).filter(published=1).order_by('-yearend')
  board_meetings = BoardMeeting.objects.filter(deleted=0).filter(published=1).filter(yearend=currentyear['currentyear']['short'])
  context['board_meeting_years'] = board_meeting_years
  context['board_meetings'] = board_meetings
  return render(request, 'pages/board/boarddetail.html', context)

def BoardMeetingYearArchive(request):
    page = get_object_or_404(BoardMeetingYear, url=request.path)
    pageopts = page._meta
    board_meeting_years = BoardMeetingYear.objects.filter(deleted=0).filter(published=1).order_by('-yearend')
    board_meetings = BoardMeeting.objects.filter(deleted=0).filter(published=1).filter(parent__url=request.path).order_by('-startdate')
    return render(request, 'pages/board/boardmeetingyears.html', {'page': page, 'pageopts': pageopts,'board_meeting_years': board_meeting_years,'board_meetings': board_meetings})

def contact(request):
    template = 'pages/contact/contact-us.html'
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            if request.user.is_anonymous:
                user = User.objects.get(username='AnonymousUser')
            else:
                user = User.objects.get(pk=request.user.pk)
            post = form.save(commit=False)
            message_parent = Node.objects.get(pk=post.parent.pk)
            if post.primary_contact == '':
                post.primary_contact = message_parent.primary_contact
            post.create_user = user
            post.update_user = user
            post.searchable = False
            post.save()
            return redirect(post.parent.url)
    else:
        form = ContactMessageForm()

        # Set parent initial value
        try:
            if request.GET['pid']:
                form.fields['parent'].initial = request.GET['pid']
        except:
                form.fields['parent'].initial = apps.common.functions.get_contactpage()
        # Set parent initial value
        try:
            if request.GET['cid']:
                form.fields['primary_contact'].initial = request.GET['cid']
        except:
                form.fields['primary_contact'].initial = ''
    return render(request, template, {'page': page,'pageopts': pageopts,'form': form,})

def contact_inline(request):
    template = 'pages/contact/contact-us-inline.html'
    page = get_object_or_404(Page, url=request.path)
    pageopts = page._meta
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            if request.user.is_anonymous:
                user = User.objects.get(username='AnonymousUser')
            else:
                user = User.objects.get(pk=request.user.pk)
            post = form.save(commit=False)
            message_parent = Node.objects.get(pk=post.parent.pk)
            if post.primary_contact == '':
                post.primary_contact = message_parent.primary_contact
            post.create_user = user
            post.update_user = user
            post.searchable = False
            post.save()
            return redirect(post.parent.url)
    else:
        form = ContactMessageForm()

        # Set parent initial value
        try:
            if request.GET['pid']:
                form.fields['parent'].initial = request.GET['pid']
        except:
                form.fields['parent'].initial = apps.common.functions.get_contactpage()
        # Set parent initial value
        try:
            if request.GET['cid']:
                form.fields['primary_contact'].initial = request.GET['cid']
        except:
                form.fields['primary_contact'].initial = ''
    return render(request, template, {'page': page,'pageopts': pageopts,'form': form,})
