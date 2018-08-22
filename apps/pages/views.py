import json
import urllib.request
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.template import Context, Template, RequestContext
from django.db.models import Prefetch
from django.utils import timezone
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse
from collections import OrderedDict
import apps.common.functions as commonfunctions
from apps.objects.models import Node, User
from .models import Page, School, Department, Board, BoardSubPage, News, NewsYear, SubPage, BoardMeetingYear, DistrictCalendarYear,SuperintendentMessage,SuperintendentMessageYear, Announcement
from apps.taxonomy.models import Location, City, State, Zipcode, Language, BoardPrecinct, BoardPolicySection, SchoolType, SchoolOption, SchoolAdministratorType, SubjectGradeLevel
from apps.images.models import Thumbnail, NewsThumbnail, ContentBanner, ProfilePicture, DistrictLogo
from apps.directoryentries.models import (
    Staff,
    SchoolAdministrator,
    Administrator,
    BoardMember,
    StudentBoardMember,
    BoardPolicyAdmin,
    SchoolAdministration,
    SchoolStaff,
    SchoolFaculty,
)
from apps.links.models import ResourceLink, ActionButton
from apps.documents.models import Document, BoardPolicy, Policy, AdministrativeProcedure, SupportingDocument
from apps.files.models import File, AudioFile, VideoFile
from apps.events.models import BoardMeeting, DistrictCalendarEvent
from apps.users.models import Employee
from apps.contactmessages.forms import ContactMessageForm


def updates_school_reg_dates():

    reg_locations = {
        10: 'Online',
        20: 'Online/On-Site',
        30: 'On-Site',
    }
    reg_audience = {
        105: '1 - 5th Grade',
        6: '6th Grade',
        7: '7th Grade',
        8: '8th Grade',
        9: '9th Grade',
        199: 'All Students',
        99: 'All Unregistered Students',
        0: 'Kindergarten',
        13: 'New Students',
        21: 'Returning Students',
    }
    response = urllib.request.urlopen('https://apex.slcschools.org/apex/slcsd-apps/regcalendars/')
    jsonalldates = response.read()
    alldates = json.loads(jsonalldates.decode("utf-8"))
    groupeddates = {}
    for date in alldates['items']:
        if date['location'] in reg_locations:
            date['location'] = reg_locations[date['location']]
        if date['audience'] in reg_audience:
            date['audience'] = reg_audience[date['audience']]
        if date['school'] not in groupeddates:
            groupeddates[date['school']] = []
        groupeddates[date['school']].append(date)
    return groupeddates


def set_template(request, node):
    if request.site.domain == 'www.slcschools.org':
        if request.path == '/' or request.path == '/home/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'home.html',
            )
        if request.path == '/employees/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if request.path == '/schools/school-handbooks/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if request.path == '/schools/district-demographics/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if request.path == '/search/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if request.path == '/departments/department-structure/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/departmentstructure.html'
        if request.path == '/departments/superintendents-office/downloads/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if request.path == '/calendars/guidelines-for-developing-calendar-options/':
            return 'cmstemplates/{0}/pagelayouts/{1}'.format(
                request.site.dashboard_general_site.template.namespace,
                'page-wide.html',
            )
        if node.content_type == 'board' or node.content_type == 'boardsubpage':
            return 'cmstemplates/www_slcschools_org/pagelayouts/boarddetail.html'
        if node.content_type == 'newsyear':
            return 'cmstemplates/www_slcschools_org/pagelayouts/newsyeararchive.html'
        if node.content_type == 'news':
            return 'cmstemplates/www_slcschools_org/pagelayouts/articledetail.html'
        if request.path == '/schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/main-school-directory.html'
        if request.path == '/schools/elementary-schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if request.path == '/schools/k-8-schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if request.path == '/schools/middle-schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if request.path == '/schools/high-schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if request.path == '/schools/charter-schools/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if request.path == '/schools/community-learning-centers/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-directory.html'
        if node.content_type == 'school':
            return 'cmstemplates/www_slcschools_org/pagelayouts/schooldetail.html'
        if request.path == '/departments/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/department-directory.html'
        if node.content_type == 'superintendentmessageyear':
            return 'cmstemplates/www_slcschools_org/pagelayouts/supermessageyeararchive.html'
        if node.content_type == 'department':
            return 'cmstemplates/www_slcschools_org/pagelayouts/departmentdetail.html'
        if node.content_type == 'superintendentmessage':
            return 'cmstemplates/www_slcschools_org/pagelayouts/supermessagedetail.html'
        if request.path == '/directory/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/directory.html'
        if request.path.startswith('/directory/last-name-'):
            return 'cmstemplates/www_slcschools_org/pagelayouts/directory-letter.html'
        if node.content_type == 'districtcalendaryear':
            return 'cmstemplates/www_slcschools_org/pagelayouts/districtcalendaryears.html'
        if node.content_type == 'boardmeetingyear':
            return 'cmstemplates/www_slcschools_org/pagelayouts/boardmeetingyears.html'
        if request.path == '/contact-us/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/contact-us.html'
        if request.path == '/contact-us/inline/':
            return 'cmstemplates/www_slcschools_org/blocks/contact-us-inline.html'
        if request.path == '/schools/school-registration-dates/':
            return 'cmstemplates/www_slcschools_org/pagelayouts/school-registration-dates.html'
        if node.node_type == 'documents':
            if node.content_type == 'document':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'policy':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'administrativeprocedure':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'supportingdocument':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'boardmeetingagenda':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'boardmeetingminutes':
                return 'cmstemplates/www_slcschools_org/pagelayouts/document.html'
            if node.content_type == 'boardmeetingaudio':
                return 'cmstemplates/www_slcschools_org/pagelayouts/audio.html'
            if node.content_type == 'boardmeetingvideo':
                return 'cmstemplates/www_slcschools_org/pagelayouts/video.html'
        return 'cmstemplates/{0}/pagelayouts/{1}'.format(
            request.site.dashboard_general_site.template.namespace,
            'page.html',
        )
    else:
        return 'cmstemplates/{0}/pagelayouts/{1}'.format(
            request.site.dashboard_general_site.template.namespace,
            node.pagelayout.namespace,
        )


def redirect_request(request):
    currentyear = commonfunctions.currentyear()
    if request.path == '/board-of-education/board-meetings/':
        try:
            year = BoardMeetingYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        except BoardMeetingYear.DoesNotExist:
            meeting, created = BoardMeeting.objects.get_or_create(startdate=timezone.now(), site=request.site)
            if created:
                meeting.save()
                meeting.delete()
                meeting.delete() 
            year = BoardMeetingYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        return redirect(year.url)
    if request.path == '/calendars/':
        try:
            year = DistrictCalendarYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        except DistrictCalendarYear.DoesNotExist:
            event, created = DistrictCalendarEvent.objects.get_or_create(startdate=timezone.now(), site=request.site)
            if created:
                event.save()
                event.delete()
                event.delete()
            year = DistrictCalendarYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        return redirect(year.url)
    if request.path == '/news/':
        try:
            year = NewsYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        except NewsYear.DoesNotExist:
            news, created = News.objects.get_or_create(title='tempnews', site=request.site)
            if created:
                news.save()
                news.delete()
                news.delete()
            year = NewsYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        return redirect(year.url)
    if request.path == '/departments/superintendents-office/superintendents-message/':
        try:
            year = SuperintendentMessageYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        except SuperintendentMessageYear.DoesNotExist:
            message, created = SuperintendentMessage.objects.get_or_create(author_date=timezone.now(), site=request.site)
            if created:
                message.save()
                message.delete()
                message.delete()
            year = SuperintendentMessageYear.objects.get(title=currentyear['currentyear']['long'], site=request.site)
        return redirect(year.url)
    return None


def prefetch_building_location_detail(qs):
    prefetchqs = (
        Location
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .only(
            'street_address',
            'location_city',
            'location_state',
            'location_zipcode',
            'google_place',
            )
        .prefetch_related(
            Prefetch(
                'location_city',
                queryset=(
                    City
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only('title')
                    )
                ),
            Prefetch(
                'location_state',
                queryset=(
                    State
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only('title')
                    )
                ),
            Prefetch(
                'location_zipcode',
                queryset=(
                    Zipcode
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only('title')
                    )
                )
            )
        )
    return qs.prefetch_related(
        Prefetch(
            'building_location',
            queryset=prefetchqs,
        )
    )


def prefetch_boardmembers_detail(qs):
    prefetchqs = (
        BoardMember
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .order_by('precinct__title')
        .only(
            'employee',
            'is_president',
            'is_vicepresident',
            'precinct',
            'phone',
            'street_address',
            'city',
            'state',
            'zipcode',
            'term_ends',
            'related_node',
            )
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=1)
                    .filter(is_staff=1)
                    .only(
                        'last_name',
                        'first_name',
                        'email',
                        )
                    .prefetch_related(
                        Prefetch(
                            'images_profilepicture_node',
                            ProfilePicture.objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .only(
                                'image_file',
                                'alttext',
                                'related_node_id',
                                )
                            )
                        )
                    )
                ),
            Prefetch(
                'precinct',
                queryset=(
                    BoardPrecinct
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'pk',
                        'title',
                        )
                    .prefetch_related('files_precinctmap_node')
                    .order_by('title')
                    )
                ),
            Prefetch(
                'city',
                queryset=(
                    City
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'pk',
                        'title',
                        )
                    )
                ),
            Prefetch(
                'state',
                queryset=(
                    State
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'pk',
                        'title',
                        )
                    )
                ),
            Prefetch(
                'zipcode',
                queryset=(
                    Zipcode
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'pk',
                        'title',
                        )
                    )
                )
            )
        )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_boardmember_node',
            queryset=prefetchqs,
        )
    )


def prefetch_studentboardmember_detail(qs):
    prefetchqs = (
        StudentBoardMember
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .order_by('title')
        .only(
            'first_name',
            'last_name',
            'phone',
            'building_location',
            'related_node',
            )
        .prefetch_related(
            Prefetch(
                'building_location',
                queryset=(
                    Location
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'street_address',
                        'location_city',
                        'location_state',
                        'location_zipcode',
                        'google_place',
                        )
                    .prefetch_related(
                        Prefetch(
                            'location_city',
                            queryset=(
                                City
                                .objects
                                .filter(deleted=0)
                                .filter(published=1)
                                .only('title')
                                )
                            ),
                        Prefetch(
                            'location_state',
                            queryset=(
                                State
                                .objects
                                .filter(deleted=0)
                                .filter(published=1)
                                .only('title')
                                )
                            ),
                        Prefetch(
                            'location_zipcode',
                            queryset=(
                                Zipcode
                                .objects
                                .filter(deleted=0)
                                .filter(published=1)
                                .only('title')
                                )
                            )
                        )
                    )
                ),
            Prefetch(
                'images_profilepicture_node',
                queryset=(
                    ProfilePicture
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .only(
                        'image_file',
                        'alttext',
                        'related_node_id',
                        )
                    )
                )
            )
        )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_studentboardmember_node',
            queryset=prefetchqs,
        )
    )


def prefetch_schooladministrators_detail(qs):
    prefetchqs = (SchoolAdministrator
                  .objects
                  .filter(deleted=False)
                  .filter(published=True)
                  .filter(employee__is_active=True)
                  .filter(employee__is_staff=True)
                  .order_by('inline_order')
                  .only(
                    'pk',
                    'employee',
                    'schooladministratortype',
                    'inline_order',
                    'related_node',
                    )
                  .prefetch_related(
                    Prefetch(
                        'employee',
                        queryset=(
                            Employee
                            .objects
                            .filter(is_active=True)
                            .filter(is_staff=True)
                            .only(
                                'pk',
                                'last_name',
                                'first_name',
                                'email',
                                'job_title',
                                )
                            .prefetch_related(
                                Prefetch(
                                    'images_profilepicture_node',
                                    queryset=(
                                        ProfilePicture
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only(
                                            'pk',
                                            'title',
                                            'image_file',
                                            'alttext',
                                            'related_node',
                                            )
                                        ),
                                    )
                                )
                            ),
                        ),
                    )
                  .prefetch_related(
                    Prefetch(
                        'schooladministratortype',
                        queryset=(
                            SchoolAdministratorType
                            .objects
                            .filter(deleted=False)
                            .filter(published=True)
                            .only(
                                'pk',
                                'title',
                                )
                            ),
                        ),
                    )
                  )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_schooladministrator_node',
            queryset=prefetchqs,
        )
    )


def prefetch_administrators_detail(qs):
    prefetchqs = (
        Administrator
        .objects
        .filter(deleted=False)
        .filter(published=True)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .order_by('inline_order')
        .only(
            'pk',
            'employee',
            'job_title',
            'inline_order',
            'related_node',
        )
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=True)
                    .filter(is_staff=True)
                    .only(
                        'pk',
                        'last_name',
                        'first_name',
                        'email',
                        'job_title',
                    )
                    .prefetch_related(
                        Prefetch(
                            'images_profilepicture_node',
                            queryset=(
                                ProfilePicture
                                .objects
                                .filter(deleted=0)
                                .filter(published=1)
                                .only(
                                    'pk',
                                    'title',
                                    'image_file',
                                    'alttext',
                                    'related_node',
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_administrator_node',
            queryset=prefetchqs,
        )
    )


def prefetch_staff_detail(qs):
    prefetchqs = (
        Staff
        .objects
        .filter(deleted=False)
        .filter(published=True)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .order_by('inline_order')
        .only(
            'pk',
            'employee',
            'job_title',
            'inline_order',
            'related_node',
        )
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=True)
                    .filter(is_staff=True)
                    .only(
                        'pk',
                        'last_name',
                        'first_name',
                        'email',
                        'job_title',
                    )
                )
            )
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_staff_node',
            queryset=prefetchqs,
        )
    )


def prefetch_documents_detail(qs):
    prefetchqs = (
        Document
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .order_by('inline_order')
        .only(
            'pk',
            'title',
            'inline_order',
            'related_node'
            )
        .prefetch_related(
            Prefetch(
                'files_file_node',
                queryset=(
                    File
                    .objects
                    .filter(deleted=0)
                    .filter(published=1)
                    .order_by(
                        'file_language__lft',
                        'file_language__title',
                        )
                    .only(
                        'title',
                        'file_file',
                        'file_language',
                        'related_node',
                        )
                    .prefetch_related(
                        Prefetch(
                            'file_language',
                            queryset=(
                                Language
                                .objects
                                .filter(deleted=0)
                                .filter(published=1)
                                .only('title')
                                )
                            )
                        )
                    )
                )
            )
        )
    return qs.prefetch_related(
        Prefetch(
            'documents_document_node',
            queryset=prefetchqs,
        )
    )


def prefetch_contentbanner_detail(qs):
    prefetchqs = (
        ContentBanner
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .only(
            'image_file',
            'alttext',
            'related_node_id',
            )
        )
    return qs.prefetch_related(
        Prefetch(
            'images_contentbanner_node',
            queryset=prefetchqs,
        )
    )


def prefecth_actionbuttons_detail(qs):
    prefetchqs = (
        ActionButton
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .only(
            'pk',
            'title',
            'link_url',
            'inline_order',
            'related_node',
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'links_actionbutton_node',
            queryset=prefetchqs,
        )
    )


def prefecth_resourcelinks_detail(qs):
    prefetchqs = (
        ResourceLink
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .only(
            'pk',
            'title',
            'link_url',
            'inline_order',
            'related_node',
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'links_resourcelink_node',
            queryset=prefetchqs,
        )
    )

def prefecth_announcement_detail(qs):
    prefetchqs = (
        Announcement
        .objects
        .filter(deleted=0)
        .filter(published=1)
    )
    return qs.prefetch_related(
        Prefetch(
            'pages_announcement_node',
            queryset=prefetchqs,
        )
    )

def prefecth_subjectgradelevel_detail(qs):
    activesubjects = []
    page = qs[0]
    for person in page.directoryentries_schoolfaculty_node.all():
        if person.primary_subject.pk not in activesubjects:
            activesubjects.append(person.primary_subject.pk)
    prefetchqs = (
        SubjectGradeLevel
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .filter(pk__in=activesubjects)
    )
    return qs.prefetch_related(
        Prefetch(
            'taxonomy_subjectgradelevel_node',
            queryset=prefetchqs,
        )
    )


def prefecth_schooladministration_detail(qs):
    prefetchqs = (
        SchoolAdministration
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=True)
                    .filter(is_staff=True)
                    .only(
                        'pk',
                        'last_name',
                        'first_name',
                        'email',
                        'job_title',
                    )
                )
            )
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_schooladministration_node',
            queryset=prefetchqs,
        )
    )


def prefecth_schoolstaff_detail(qs):
    prefetchqs = (
        SchoolStaff
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=True)
                    .filter(is_staff=True)
                    .only(
                        'pk',
                        'last_name',
                        'first_name',
                        'email',
                        'job_title',
                    )
                )
            )
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_schoolstaff_node',
            queryset=prefetchqs,
        )
    )


def prefecth_schoolfaculty_detail(qs):
    prefetchqs = (
        SchoolFaculty
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .filter(employee__is_active=True)
        .filter(employee__is_staff=True)
        .prefetch_related(
            Prefetch(
                'employee',
                queryset=(
                    Employee
                    .objects
                    .filter(is_active=True)
                    .filter(is_staff=True)
                    .only(
                        'pk',
                        'last_name',
                        'first_name',
                        'email',
                        'job_title',
                    )
                )
            )
        )
        .order_by(
            'employee__first_name',
            'employee__last_name',
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'directoryentries_schoolfaculty_node',
            queryset=prefetchqs,
        )
    )

def prefetch_subpage_detail(qs):
    prefetchqs = (
        SubPage
        .objects
        .filter(deleted=0)
        .filter(published=1)
        .only(
            'title',
            'url',
            'inline_order',
            'related_node_id',
        )
    )
    return qs.prefetch_related(
        Prefetch(
            'pages_subpage_node',
            queryset=prefetchqs,
        )
    )


def add_additional_context(request, context, node):
    if request.path == '/' or request.path == '/home/':
        context['supermessage'] = (
            SuperintendentMessage
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('-author_date')
            .only(
                'title',
                'author_date',
                'summary',
                'url',
                )[:1]
            )
        context['news'] = (
            News
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by(
                '-pinned',
                '-author_date',
                )
            .only(
                'title',
                'author_date',
                'summary',
                'url',
                )
            .prefetch_related(
                Prefetch(
                    'images_newsthumbnail_node',
                    queryset=(
                        NewsThumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                            )
                        )
                    )
                )[0:5]
            )
    if request.path == '/departments/department-structure/':
        context['departments'] = (
            prefetch_building_location_detail(
                Department
                .objects
                .filter(deleted=0)
                .filter(published=1)
                .order_by('lft')
                )
            )
    if request.path == '/board-of-education/policies/':
        district_policies = (
            BoardPolicy
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('section__lft','index')
            .only('pk','policy_title','index','section','related_node')
            .prefetch_related(
                Prefetch('section', queryset= BoardPolicySection.objects.filter(deleted=0).filter(published=1).only('pk','section_prefix','description')),Prefetch('directoryentries_boardpolicyadmin_node',queryset=BoardPolicyAdmin.objects.filter(deleted=0).filter(published=1).order_by('title').only('pk','employee','related_node').prefetch_related(Prefetch('employee',queryset=Employee.objects.filter(is_active=1).filter(is_staff=1).only('pk','last_name','first_name')))),Prefetch('documents_policy_node', queryset = Policy.objects.filter(deleted=0).filter(published=1).only('pk','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))),Prefetch('documents_administrativeprocedure_node', queryset = AdministrativeProcedure.objects.filter(deleted=0).filter(published=1).only('pk','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))),Prefetch('documents_supportingdocument_node', queryset = SupportingDocument.objects.filter(deleted=0).filter(published=1).only('pk','document_title','related_node').prefetch_related(Prefetch('files_file_node', queryset = File.objects.filter(deleted=0).filter(published=1).order_by('file_language__lft','file_language__title').only('title','file_file','file_language','related_node').prefetch_related(Prefetch('file_language',queryset=Language.objects.filter(deleted=0).filter(published=1).only('title')))))))
            )
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
    if request.path == '/board-of-education/policies/policy-review-schedule/':
        context['policy_review'] = OrderedDict()
        policy_review = (
            BoardPolicy
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .exclude(subcommittee_review=None)
            .exclude(boardmeeting_review=None)
            .order_by(
                'subcommittee_review',
                'section__lft',
                'index')
            .only(
                'pk',
                'policy_title',
                'index',
                'section',
                'subcommittee_review',
                'boardmeeting_review',
                'last_approved',
                'related_node',
                )
            .prefetch_related(
                Prefetch(
                    'section',
                    queryset=(
                        BoardPolicySection
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'section_prefix',
                            )
                        )
                    )
                )
            )
        for policy in policy_review:
            strdate = '{0}{1}'.format(
                policy.subcommittee_review.strftime('%Y%m%d'),
                policy.boardmeeting_review.strftime('%Y%m%d'),
                )
            if strdate not in context['policy_review']:
                context['policy_review'][strdate] = {}
                context['policy_review'][strdate]['subcommittee_review'] = (
                    policy.subcommittee_review.strftime('%m/%d/%Y')
                    )
                context['policy_review'][strdate]['boardmeeting_review'] = (
                    policy.boardmeeting_review.strftime('%m/%d/%Y')
                    )
                context['policy_review'][strdate]['policies'] = []
            context['policy_review'][strdate]['policies'].append(policy)
    if node.content_type == 'newsyear':
        context['newsyears'] = NewsYear.objects.all().order_by('-yearend')
        context['news'] = (
            News.
            objects
            .filter(parent__url=request.path)
            .filter(deleted=0)
            .filter(published=1)
            .only(
                'title',
                'author_date',
                'summary',
                'url',
            )
            .prefetch_related(
                Prefetch(
                    'images_newsthumbnail_node',
                    queryset=(
                        NewsThumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        newsmonths = [
            {'month': 'June', 'news': [], },
            {'month': 'May', 'news': [], },
            {'month': 'April', 'news': [], },
            {'month': 'March', 'news': [], },
            {'month': 'February', 'news': [], },
            {'month': 'January', 'news': [], },
            {'month': 'December', 'news': [], },
            {'month': 'November', 'news': [], },
            {'month': 'October', 'news': [], },
            {'month': 'September', 'news': [], },
            {'month': 'August', 'news': [], },
            {'month': 'July', 'news': [], },
        ]
        for item in context['news']:
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
        context['newsmonths'] = newsmonths
    if request.path == '/schools/' or request.path == '/schools/school-registration-dates/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'school_number',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['elementary_schools_directory'] = []
        context['k8_schools_directory'] = []
        context['middle_schools_directory'] = []
        context['high_schools_directory'] = []
        context['charter_schools_directory'] = []
        context['community_learning_centers_directory'] = []
        for school in schools:
            if school.schooltype.title == 'Elementary Schools':
                context['elementary_schools_directory'].append(school)
            if school.schooltype.title == 'K-8 Schools':
                context['k8_schools_directory'].append(school)
            if school.schooltype.title == 'Middle Schools':
                context['middle_schools_directory'].append(school)
            if school.schooltype.title == 'High Schools':
                context['high_schools_directory'].append(school)
            if school.schooltype.title == 'Charter Schools':
                context['charter_schools_directory'].append(school)
            if school.schooltype.title == 'Community Learning Centers':
                context['community_learning_centers_directory'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
        context['school_reg_dates'] = cache.get_or_set('school_reg_dates', updates_school_reg_dates(), 120)
    if request.path == '/schools/elementary-schools/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'Elementary Schools':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/schools/k-8-schools/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'K-8 Schools':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/schools/middle-schools/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'Middle Schools':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/schools/high-schools/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'High Schools':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/schools/charter-schools/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'Charter Schools':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/schools/community-learning-centers/':
        schools = (
            School
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'pk',
                'title',
                'building_location',
                'schooltype',
                'schooloptions',
                'website_url',
                'scc_url',
                'calendar_url',
                'donate_url',
                'boundary_map',
                'url',
                'main_phone',
            )
            .prefetch_related(
                Prefetch(
                    'schooltype',
                    queryset=(
                        SchoolType
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'schooloptions',
                    queryset=(
                        SchoolOption
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'pk',
                            'title',
                        )
                    )
                ),
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                ),
                Prefetch(
                    'images_thumbnail_node',
                    queryset=(
                        Thumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        context['schools'] = []
        for school in schools:
            if school.schooltype.title == 'Community Learning Centers':
                context['schools'].append(school)
        context['learningoptions'] = SchoolOption.objects.filter(deleted=0).filter(published=1).order_by('title')
    if request.path == '/departments/':
        all_departments = (
            Department
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('title')
            .only(
                'title',
                'building_location',
                'url',
                'main_phone',
                'short_description',
                'is_department',
            )
            .prefetch_related(
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .only('title')
                                )
                            )
                        )
                    )
                )
            )
        )
        departments = {
            'departments': [],
            'programs': [],
        }
        for department in all_departments:
            if department.is_department:
                departments['departments'].append(department)
            else:
                departments['programs'].append(department)
        context['departments'] = departments
    if node.content_type == 'superintendentmessageyear':
        context['messageyears'] = SuperintendentMessageYear.objects.all().order_by('-yearend')
        context['superintendent_messages'] = (
            SuperintendentMessage
            .objects
            .filter(parent__url=request.path)
            .filter(deleted=0)
            .filter(published=1)
            .only(
                'title',
                'author_date',
                'summary',
                'url',
            )
            .prefetch_related(
                Prefetch(
                    'images_newsthumbnail_node',
                    queryset=(
                        NewsThumbnail
                        .objects
                        .only(
                            'image_file',
                            'alttext',
                            'related_node_id',
                        )
                    )
                )
            )
        )
        messagemonths = [
            {'month': 'June', 'message': [], },
            {'month': 'May', 'message': [], },
            {'month': 'April', 'message': [], },
            {'month': 'March', 'message': [], },
            {'month': 'February', 'message': [], },
            {'month': 'January', 'message': [], },
            {'month': 'December', 'message': [], },
            {'month': 'November', 'message': [], },
            {'month': 'October', 'message': [], },
            {'month': 'September', 'message': [], },
            {'month': 'August', 'message': [], },
            {'month': 'July', 'message': [], },
        ]
        for item in context['superintendent_messages']:
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
        context['messagemonths'] = messagemonths
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
    if node.content_type == 'department':
        context['department_children'] = (
            Department
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .filter(parent__url=request.path)
            .order_by('title')
            .only(
                'pk',
                'title',
                'short_description',
                'main_phone',
                'building_location',
                'content_type',
                'menu_title',
                'url',
            )
            .prefetch_related(
                Prefetch(
                    'building_location',
                    queryset=(
                        Location
                        .objects
                        .filter(deleted=0)
                        .filter(published=1)
                        .only(
                            'street_address',
                            'location_city',
                            'location_state',
                            'location_zipcode',
                            'google_place',
                        )
                        .prefetch_related(
                            Prefetch(
                                'location_city',
                                queryset=(
                                    City
                                    .objects
                                    .filter(deleted=0)
                                    .filter(published=1)
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_state',
                                queryset=(
                                    State
                                    .objects
                                    .filter(deleted=0)
                                    .filter(published=1)
                                    .only('title')
                                )
                            ),
                            Prefetch(
                                'location_zipcode',
                                queryset=(
                                    Zipcode
                                    .objects
                                    .filter(deleted=0)
                                    .filter(published=1)
                                    .only('title')
                                )
                            )
                        )
                    )
                )
            )
        )
    if request.path == '/directory/':
        context['people'] = (
            Employee
            .objects
            .filter(is_active=1)
            .filter(is_staff=1)
            .filter(in_directory=1)
            .order_by('last_name')
            .only(
                'pk',
                'last_name',
                'first_name',
                'job_title',
                'email',
                'department',
            )
            .prefetch_related(
                Prefetch(
                    'department',
                    queryset=(
                        Node
                        .objects
                        .only(
                            'node_title',
                            'url',
                        )
                    )
                )
            )
        )
    if request.path.startswith('/directory/last-name-'):
        letter = request.path[-2]
        context['people'] = (
            Employee
            .objects
            .filter(is_active=1)
            .filter(is_staff=1)
            .filter(in_directory=1)
            .filter(last_name__istartswith=letter)
            .order_by('last_name')
            .only(
                'pk',
                'last_name',
                'first_name',
                'job_title',
                'email',
                'department',
            )
            .prefetch_related(
                Prefetch(
                    'department',
                    queryset=(
                        Node
                        .objects
                        .only(
                            'node_title',
                            'url',
                        )
                    )
                )
            )
        )
    if node.content_type == 'districtcalendaryear':
        context['districtcalendaryears'] = (
            DistrictCalendarYear
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('-yearend')
        )
        context['districtcalendarevents'] = (
            DistrictCalendarEvent
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .filter(parent__url=request.path)
        )
    if node.content_type == 'boardmeetingyear':
        context['board_meeting_years'] = (
            BoardMeetingYear
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .order_by('-yearend')
        )
        context['board_meetings'] = (
            BoardMeeting
            .objects
            .filter(deleted=0)
            .filter(published=1)
            .filter(parent__url=request.path)
            .order_by('-startdate')
        )
    if (
        request.method != 'POST' and
        (
            request.path == '/contact-us/' or
            request.path == '/contact-us/inline/'
        )
    ):
        context['form'] = contactmessage_get(request)
        context['from_page'] = (
            commonfunctions
            .nodefindobject(
                Node.objects
                .get(pk=context['form'].fields['parent'].initial)
            )
        )
    context['in_this_section'] = (
        node
        .get_root()
        .get_descendants(include_self=True)
        .filter(
            node_type='pages',
            content_type='page',
            published=True,
            deleted=False,
        )
    )
    return context


def process_post(request):
    if (
        request.method == 'POST' and
        (
            request.path == '/contact-us/' or
            request.path == '/contact-us/inline/'
        )
    ):
        post = contactmessage_post(request)
        return post.parent.url


def contactmessage_post(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        if request.user.is_anonymous:
            user = User.objects.get(username='AnonymousUser')
        else:
            user = User.objects.get(pk=request.user.pk)
        post = form.save(commit=False)
        message_parent = Node.objects.get(pk=post.parent.pk)
        if post.primary_contact == '':
            if message_parent.primary_contact:
                post.primary_contact = message_parent.primary_contact
            else:
                post.primary_contact = request.site.dashboard_general_site.primary_contact
        post.create_user = user
        post.update_user = user
        post.site = request.site
        post.searchable = False
        post.remote_addr = request.META['HTTP_X_FORWARDED_FOR']
        post.user_agent = request.META['HTTP_USER_AGENT']
        post.http_headers = json.dumps(request.META, default=str)
        if not post.our_message:
            post.save()
            messages.success(
                request,
                'Thank you for contacting us. '
                'Someone will get back to you shortly.')
        else:
            messages.error(
                request,
                'Something was wrong with your message. Please try again.')
        return post


def contactmessage_get(request):
    form = ContactMessageForm()
    try:
        if request.GET['pid']:
            form.fields['parent'].initial = request.GET['pid']
    except:
        form.fields['parent'].initial = commonfunctions.get_contactpage(request)
    try:
        if request.GET['cid']:
            form.fields['primary_contact'].initial = request.GET['cid']
    except:
        try:
            form.fields['primary_contact'].initial = str(Node.objects.get(pk=form.fields['parent'].initial).primary_contact.pk)
        except:
            try:
                form.fields['primary_contact'].initial = str(request.site.dashboard_general_site.primary_contact.pk)
            except:
                form.fields['primary_contact'].initial = str(User.objects.get(username='webmaster@slcschools.org').pk)
    try:
        message_to = User.objects.get(
            pk=form.fields['primary_contact'].initial
        )
    except User.DoesNotExist:
        message_to = User.objects.get(
            username='webmaster@slcschools.org',
        )
    form.fields['message_to'].initial = '{0} {1}'.format(
        message_to.first_name,
        message_to.last_name,
    )
    form.fields['message_to'].disabled = True
    return form


# def contact(request):
#     template = 'cmstemplates/www_slcschools_org/pagelayouts/contact-us.html'
#     context = {}
#     context['page'] = get_object_or_404(Page, url=request.path)
#     context['pageopts'] = context['page']._meta
#     if request.method == "POST":
#         post = contactmessage_post(request)
#         return redirect(post.parent.url)
#     else:
#         context['form'] = contactmessage_get(request)
#         context['from_page'] = commonfunctions.nodefindobject(Node.objects.get(pk=context['form'].fields['parent'].initial))
#     return render(request, template, context)


# def contact_inline(request):
#     template = 'cmstemplates/www_slcschools_org/blocks/contact-us-inline.html'
#     context = {}
#     context['page'] = get_object_or_404(Page, url=request.path)
#     context['pageopts'] = context['page']._meta
#     if request.method == "POST":
#         post = contactmessage_post(request)
#         return redirect(post.parent.url)
#     else:
#         context['form'] = contactmessage_get(request)
#         context['from_page'] = commonfunctions.nodefindobject(Node.objects.get(pk=context['form'].fields['parent'].initial))
#     return render(request, template, context)


def node_lookup(request):
    if redirect_request(request) is not None:
        return redirect_request(request)
    try:
        if request.path == '/':
            node = Node.objects.get(url='/home/', site=request.site)
        else:
            node = Node.objects.get(url=request.path, site=request.site)
    except Node.DoesNotExist:
        raise Http404('Page not found.')
    Model = apps.get_model(node.node_type, node.content_type)
    if node.node_type == 'pages':
        if request.method == 'POST':
            return redirect(process_post(request))
        template = set_template(request, node)
        context = {}
        context['page'] = (Model
                           .objects
                           .filter(pk=node.pk)
                           )
        fields = context['page'].model._meta.get_fields(include_hidden=True)
        # Add prefetch function calls here
        if 'building_location' in fields:
            context['page'] = (
                prefetch_building_location_detail(context['page'])
                )
        context['page'] = prefetch_contentbanner_detail(context['page'])
        context['page'] = prefecth_actionbuttons_detail(context['page'])
        context['page'] = prefetch_boardmembers_detail(context['page'])
        context['page'] = prefetch_studentboardmember_detail(context['page'])
        context['page'] = prefetch_schooladministrators_detail(context['page'])
        context['page'] = prefetch_administrators_detail(context['page'])
        context['page'] = prefetch_staff_detail(context['page'])
        context['page'] = prefecth_resourcelinks_detail(context['page'])
        context['page'] = prefetch_documents_detail(context['page'])
        context['page'] = prefetch_subpage_detail(context['page'])
        context['page'] = prefecth_announcement_detail(context['page'])
        context['page'] = prefecth_schooladministration_detail(context['page'])
        context['page'] = prefecth_schoolstaff_detail(context['page'])
        context['page'] = prefecth_schoolfaculty_detail(context['page'])
        context['page'] = prefecth_subjectgradelevel_detail(context['page'])
        # Add additional context here
        context = add_additional_context(request, context, node)
        # Change Queryset into object
        context['page'] = context['page'].first()
        context['pageopts'] = context['page']._meta
        return render(request, template, context)
    if node.node_type == 'documents':
        if node.content_type == 'document':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardpolicy':
            return HttpResponse(status=200)
        if node.content_type == 'policy':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'administrativeprocedure':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'supportingdocument':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardmeetingagenda':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardmeetingminutes':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_file_node',
                        queryset=(
                            File
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .order_by(
                                'file_language__lft',
                                'file_language__title',
                            )
                            .only(
                                'title',
                                'file_file',
                                'file_language',
                                'related_node',
                            )
                            .prefetch_related(
                                Prefetch(
                                    'file_language',
                                    queryset=(
                                        Language
                                        .objects
                                        .filter(deleted=0)
                                        .filter(published=1)
                                        .only('title')
                                    )
                                )
                            )
                        )
                    )
                )
            )
            item = item.first()
            if item.files_file_node.all().count() == 1:
                return redirect(item.files_file_node.first().url)
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardmeetingaudio':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_audiofile_node',
                        queryset=(
                            AudioFile
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .only(
                                'title',
                                'file_file',
                                'related_node',
                            )
                        )
                    )
                )
            )
            item = item.first()
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardmeetingvideo':
            item = (
                Model
                .objects
                .filter(pk=node.pk)
                .prefetch_related(
                    Prefetch(
                        'files_videofile_node',
                        queryset=(
                            VideoFile
                            .objects
                            .filter(deleted=0)
                            .filter(published=1)
                            .only(
                                'title',
                                'file_file',
                                'related_node',
                            )
                        )
                    )
                )
            )
            item = item.first()
            template = set_template(request, node)
            context = {}
            context['page'] = item
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
        if node.content_type == 'boardmeetingexhibit':
            return HttpResponse(status=200)
        if node.content_type == 'boardmeetingagendaitem':
            return HttpResponse(status=200)
    if node.node_type == 'files':
        item = (
            Model
            .objects
            .get(pk=node.pk)
        )
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = item.file_file.url
        response['Content-Disposition'] = 'filename={0}'.format(
            item.file_name()
        )
        return response
    if node.node_type == 'images':
        item = (
            Model
            .objects
            .get(pk=node.pk)
        )
        response = HttpResponse()
        response['Content-Type'] = ''
        response['X-Accel-Redirect'] = item.image_file.url
        response['Content-Disposition'] = 'filename={0}'.format(
            item.file_name()
        )
        return response
    if node.node_type == 'directoryentries':
        if node.content_type == 'schoolfaculty':
            item = (
                Model
                .objects
                .filter(deleted=0)
                .filter(published=1)
                .filter(pk=node.pk)
            )
            template = set_template(request, node)
            context = {}
            context = add_additional_context(request, context, node)
            context['page'] = item.first()
            context['pageopts'] = context['page']._meta
            return render(request, template, context)
    return HttpResponse(status=404)
