from django.conf.urls import url

from . import views
from .models import Page

Pages = Page.objects.filter(deleted=0).filter(published=1)

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^home/$', views.home, name='home'),
  url(r'^news/$', views.news, name='news'),
  url(r'^news/\d\d\d\d-\d\d\/$', views.NewsYearArchive, name='newsyeararchive'),
  url(r'^news/\d\d\d\d-\d\d\/.*\/$', views.NewsArticleDetail, name='newsarticledetail'),
  url(r'^schools/$', views.schools, name='schools'),
  url(r'^schools/elementary-schools/$', views.elementaryschools, name='elementaryschools'),
  url(r'^schools/k-8-schools/$', views.k8schools, name='k8schools'),
  url(r'^schools/middle-schools/$', views.middleschools, name='middleschools'),
  url(r'^schools/high-schools/$', views.highschools, name='highschools'),
  url(r'^schools/charter-schools/$', views.charterschools, name='charterschools'),
  url(r'^schools/community-learning-centers/$', views.communitylearningcenters, name='communitylearningcenters'),
  url(r'^schools/school-handbooks/$', views.school_handbooks, name='school_handbooks'),
  url(r'^schools/district-demographics/$', views.district_demographics, name='district_demographics'),
  url(r'^schools/[a-z0-9-]+\/[a-z0-9-]+\/$', views.schooldetail, name='schooldetail'),
  url(r'^departments/$', views.departments, name='departments'),
  url(r'^departments/superintendents-office/superintendents-message/$', views.superintendents_message, name='superintendents_message'),
  url(r'^departments/superintendents-office/superintendents-message/\d\d\d\d-\d\d\/$', views.superintendents_message_yeararchive, name='superintendents_message_yeararchive'),
  url(r'^departments/superintendents-office/superintendents-message/\d\d\d\d-\d\d\/.*\/$', views.superintendents_message_detail, name='superintendents_message_detail'),
  url(r'^departments/superintendents-office/downloads/$', views.superintendents_downloads, name='superintendents_downloads'),
  url(r'^departments/(?:[a-z0-9-]+\/)+$', views.departmentdetail, name='departmentdetail'),
  url(r'^directory/$', views.directory, name='directory'),
  url(r'^directory/last-name-(?P<letter>[a-z])/$', views.directory_letter, name='directory_letter'),
  url(r'^calendars/$', views.calendars, name='calendars'),
  url(r'^calendars/\d\d\d\d-\d\d\/$', views.districtcalendaryearsarchive, name='districtcalendaryearsarchive'),
  url(r'^calendars/guidelines-for-developing-calendar-options/$', views.calendarguide, name='calendarguide'),
  url(r'^board-of-education/board-meetings/\d\d\d\d-\d\d\/$', views.BoardMeetingYearArchive, name='boardmeetingyeararchive'),
  url(r'^board-of-education/(?:[a-z0-9-]+\/)*$', views.boarddetail, name='board'),
  url(r'^search/$', views.search, name='search'),
  url(r'^employees/$', views.employees, name='employees'),
  url(r'^contact-us/$', views.contact, name='contact'),
  url(r'^contact-us/inline/$', views.contact_inline, name='contact_inline'),
  url(r'^(?:[a-z0-9-]+\/)+$', views.node_lookup, name='node_lookup'),
]
