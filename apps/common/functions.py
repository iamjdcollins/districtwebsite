import os
import shutil
import re
import uuid
from django.conf import settings
from django.apps import apps
from django.core.mail import EmailMessage
from django.contrib.auth import get_permission_codename
from guardian.shortcuts import get_perms
from django.core.exceptions import FieldDoesNotExist
from django.utils import timezone
from datetime import timedelta
# Required for response change
import base64
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters


def contactmessage_confirm(self):
    email = EmailMessage(
        'THANK YOU: ' + self.message_subject,
        ('<p>We have received your message. '
         'We will get back to you shortly.</p>'
         '<br><p><strong>Original Message</strong>'
         '</p><br><p>' + self.your_message + '</p>'),
        'Salt Lake City School District <webmaster@slcschools.org>',
        [self.your_email],
        reply_to=['donotreply@slcschools.org'],
        headers={'Message-ID': str(self.pk) + '-' + str(uuid.uuid4())[0:8]},
    )
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except Exception:
        return False
    return True


def contactmessage_message(self):
    email = EmailMessage(
        'WEBSITE CONTACT: ' + self.message_subject,
        ('<p><strong>From:</strong> {0}</p><p><strong>Page:</strong> '
         '<a href="https://www.slcschools.org{1}">https://www.slcschools.org'
         '{1}</a></p><p><strong>Message:</strong><br>{2}</p>').format(
            self.your_name,
            self.parent.url,
            self.your_message
            ),
        '"{0}" <{1}>'.format(self.your_name, self.your_email),
        [self.primary_contact.email],
        bcc=['webmaster@slcschools.org'],
        reply_to=[self.your_email],
        headers={
            'Message-ID': str(self.pk) + '-' + str(uuid.uuid4())[0:8],
            'Sender': ('Salt Lake City School District'
                       '<webmaster@slcschools.org>'),
            },
    )
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except Exception:
        return False
    return True


def urlchanged_email(self, oldurl):
    email = EmailMessage(
        'Website URL Changed App {0} Type {1}'.format(
                self.node_type, self.content_type),
        ('<p><strong>Previous URL:</strong> ' + oldurl + '</p>'
         '<p><strong>New URL:</strong> ' + self.url + '</p>'),
        'Salt Lake City School District <webmaster@slcschools.org>',
        ['jordan.collins@slcschools.org'],
        reply_to=['donotreply@slcschools.org'],
        headers={'Message-ID': str(self.pk) + '-' + str(uuid.uuid4())[0:8]},
    )
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except Exception:
        return False
    return True


def filepath_email(self, oldpath, newpath):
    email = EmailMessage(
        'File Path Changed: App {0} Type {1}'.format(
                self.parent.node_type, self.parent.content_type),
        ('<p><strong>Previous Path:</strong> ' + oldpath + '</p>'
         '<p><strong>New Path:</strong> ' + newpath + '</p>'),
        'Salt Lake City School District <webmaster@slcschools.org>',
        ['jordan.collins@slcschools.org'],
        reply_to=['donotreply@slcschools.org'],
        headers={'Message-ID': str(self.pk) + '-' + str(uuid.uuid4())[0:8]},
    )
    email.content_subtype = 'html'
    try:
        email.send(fail_silently=False)
    except Exception:
        return False
    return True


def findfileext_media(media):
    media = media.split('/')[-1:]
    return os.path.splitext(media[0])


def urlclean_fileext(fileext):
    return re.sub(
        '-+', '-', re.sub(r'([\s+])', '-', re.sub(
            r'([^.a-z0-9\s-])', '', fileext.lower())))


def urlclean_objname(objname):
    return re.sub(
        '-+', '-', re.sub(r'([\s+])', '-', re.sub(
            r'([^a-z0-9\s-])', '', objname.lower())))


def urlclean_remdoubleslashes(objname):
    return re.sub('/+', '/', objname.lower())


def silentdelete_media(media):
    try:
        if os.path.isfile(media):
            os.remove(media)
        elif os.path.isdir(media):
            shutil.rmtree(media, ignore_errors=True)
    except OSError:
        pass


def silentmove_media(oldpath, newpath):
    try:
        if not os.path.isdir(oldpath) & os.path.isdir(newpath):
            f = open('/tmp/movingfile.txt', 'a')
            f.write('Moving: ' + oldpath + ' To: ' + newpath + '\n')
            f.close()
            shutil.move(oldpath, newpath)
        else:
            try:
                f = open('/tmp/movingfile.txt', 'a')
                f.write('Removing: ' + oldpath + '\n')
                f.close()
                os.rmdir(oldpath)
            except OSError:
                pass
    except OSError:
        pass


def has_add_permission(self, request, obj=None):
    # Prevent showing the Save and Add Another Option
    if request.path.split('/')[-2:][0] == 'change':
        return False
    if request.user.has_perm(
        self.model._meta.app_label + '.' + get_permission_codename(
            'add', self.model._meta)):
        return True
    elif obj:
        if get_permission_codename(
                'add', self.model._meta) in get_perms(request.user, obj):
            return True
    return False


def has_change_permission(self, request, obj=None):
    if self is not None:
        # Check for regular global model permission
        if request.user.has_perm(
            self.model._meta.app_label + '.' + get_permission_codename(
                'change', self.model._meta)):
            return True
    if obj:
        if obj.has_permissions:
            # Check for object level permission through Guardian
            if get_permission_codename(
                    'change', obj._meta) in get_perms(request.user, obj):
                return True
        else:
            node = objectfindnode(obj)
            permission_point = nodefindobject(
                node.get_ancestors().filter(has_permissions=True).last())
            if get_permission_codename(
                    'change', permission_point._meta) in get_perms(
                    request.user, permission_point):
                return True
    return False


def has_delete_permission(self, request, obj=None):
    if request.user.has_perm(
        self.model._meta.app_label + '.' + get_permission_codename(
            'trash', self.model._meta)):
        return True
    elif obj:
        if obj.has_permissions:
            # Check for object level permission through Guardian
            if get_permission_codename(
                    'trash', self.model._meta) in get_perms(request.user, obj):
                return True
        else:
            node = objectfindnode(obj)
            permission_point = nodefindobject(
                node.get_ancestors().filter(has_permissions=True).last())
            if get_permission_codename(
                'trash', permission_point._meta) in get_perms(
                    request.user, permission_point):
                return True
    return False


def has_add_permission_inline(self, request, obj=None):
    # Allow if object is new (should always be new)
    if obj is None:
        return True
    return False


def has_change_permission_inline(self, request, obj=None):
    return True


def has_delete_permission_inline(self, request, obj=None):
    return True


def modeltrash(self, *args, **kwargs):
    if self.deleted == 0:
        self.deleted = True
        self.save()
    else:
        if self.url:
            silentdelete_media(settings.MEDIA_ROOT + self.url)
        super(self._meta.model, self).delete()


def movechildren(self):
    children = self.get_children()
    for child in children:
        if child.content_type == 'Board':
            child.board.save()
        elif child.content_type == 'BoardSubPage':
            child.boardsubpage.save()


# Upload Image Functions
def image_upload_to(instance, filename):
    url = instance.url[1:]
    title = urlclean_objname(instance.file_name(instance))
    original_file, original_extension = findfileext_media(filename)
    extension = urlclean_fileext(original_extension)
    full_path = '{0}{1}{2}'.format(url, title, extension)
    if not instance.image_file._committed:
        silentdelete_media(settings.MEDIA_ROOT + '/' + full_path)
    return full_path


# Upload File Functions
def file_upload_to(instance, filename):
    parentobject = nodefindobject(instance.parent)
    url = instance.url[1:]
    title = urlclean_objname(parentobject.file_name(instance))
    original_file, original_extension = findfileext_media(filename)
    extension = urlclean_fileext(original_extension)
    full_path = '{0}{1}{2}'.format(url, title, extension)
    if not instance.file_file._committed:
        silentdelete_media(settings.MEDIA_ROOT + '/' + full_path)
    return full_path


# Save Content Functions

def modelsave(self, *args, **kwargs):
    if not self.site:
        raise Exception('site not set for object. cannot be saved.')
    else:
        settings.DATA_DIR = '/srv/nginx/' + self.site.domain
        settings.MEDIA_ROOT = os.path.join(settings.DATA_DIR)
        settings.STATIC_ROOT = os.path.join(settings.MEDIA_ROOT, 'static')
    Node = apps.get_model('objects', 'node')
    User = apps.get_model('objects', 'user')
    # Is this a new instance?
    is_new = self._state.adding
    # Set deleted prefix
    is_deleted = '_' if self.deleted is True else ''
    # Set UUID if None
    self.uuid = self.uuid if self.uuid else uuid.uuid4()
    # Set original date on event
    try:
        if self._meta.get_field('originaldate'):
            if (not self.originaldate) and self.startdate:
                self.originaldate = self.startdate
                self.originalinstance = len(self._meta.model.objects.filter(
                    originaldate=self.originaldate)) + 1
    except FieldDoesNotExist:
        pass
    # Create Parent
    if self.PARENT_TYPE:
        creator = User.objects.get(username='webmaster@slcschools.org')
        self.parent = self.create_parent(creator=creator)
    # Force Parent
    if self.PARENT_URL:
        try:
            self.parent = Node.objects.exclude(
                uuid=self.uuid).get(url=self.PARENT_URL)
        except Node.DoesNotExist:
            pass
    # Related Node matches Parent
    try:
        if self._meta.get_field('related_node'):
            self.related_node = self.parent
    except FieldDoesNotExist:
        pass
    # Force Title
    self.title = self.force_title()
    # Set Slug
    if not self.slug or not self.sluginstance:
        self.slug = urlclean_objname(self.title)
        self.sluginstance = 0
    # Set URL
    urlchanged = False
    parent_url = self.parent.url if self.parent else self.PARENT_URL
    oldurl = self.url
    self.url = urlclean_remdoubleslashes('/{0}/{1}/{2}{3}{4}/'.format(
        parent_url,
        self.URL_PREFIX,
        is_deleted,
        urlclean_objname(self.slug),
        '' if self.sluginstance == 0 else '-{0}'.format(self.sluginstance),
        )
    )
    while Node.objects.filter(site=self.site).filter(url=self.url).exclude(
            pk=self.pk).count() >= 1:
        self.sluginstance += 1
        self.url = urlclean_remdoubleslashes('/{0}/{1}/{2}{3}{4}/'.format(
            parent_url,
            self.URL_PREFIX,
            is_deleted,
            urlclean_objname(self.slug),
            '' if self.sluginstance == 0 else '-{0}'.format(self.sluginstance),
            )
        )
    if not is_new and (oldurl != self.url):
        urlchanged = True
        urlchanged_email(self, oldurl)
    # Set new name for file fields
    currentname = None
    newname = None
    # Image file field
    try:
        if self.image_file:
            currentname = findfileext_media(self.image_file.name)
            newname = image_upload_to(self, currentname[0] + currentname[1])
            currentname = '{0}/{1}{2}'.format(
                '/'.join(newname.split('/')[:-1]),
                currentname[0],
                currentname[1],
                )
            self.image_file.name = newname
    except AttributeError:
        pass
    # File file field
    try:
        if self.file_file:
            currentname = findfileext_media(self.file_file.name)
            newname = file_upload_to(self, currentname[0] + currentname[1])
            currentname = '{0}/{1}{2}'.format(
                '/'.join(newname.split('/')[:-1]),
                currentname[0],
                currentname[1],
                )
            self.file_file.name = newname
    except AttributeError:
        pass
    # Set the node_title for the node
    self.node_title = self.title
    # Set the node type
    self.node_type = self._meta.app_label
    # Set the content type
    self.content_type = self._meta.model_name
    # if not self.menu_title:
    #   self.menu_title = self.title
    # Set school year for events
    try:
        if self._meta.get_field('schoolyear'):
            self.schoolyear = str(
                currentyear(self.startdate)['currentyear']['long']
            )
    except FieldDoesNotExist:
        pass
    # Set yearend for events
    if self.node_type == 'events':
        try:
            if self._meta.get_field('yearend'):
                self.schoolyear = str(
                    currentyear(self.startdate)['currentyear']['short']
                )
        except FieldDoesNotExist:
            pass
    # Does this item have permissions?
    if self.HAS_PERMISSIONS:
        self.has_permissions = True
    else:
        self.has_permissions = False
    # Save the item
    super(self._meta.model, self).save(*args, **kwargs)
    # Move Directories for children then parent.
    if urlchanged:
        # Save Children to update their urls and move thier directories.
        for child in self.get_children():
            object = nodefindobject(child)
            object.save()
        # Move Directory
        silentmove_media(
            settings.MEDIA_ROOT + oldurl,
            settings.MEDIA_ROOT + self.url
        )
    # Move File
    if currentname != newname:
        oldpath = '{0}/{1}'.format(settings.MEDIA_ROOT, currentname)
        newpath = '{0}/{1}'.format(settings.MEDIA_ROOT, newname)
        silentmove_media(oldpath, newpath)
        # Commenting file moves because newly uploaded files
        # think they are moving on upload.
        # filepath_email(self, oldpath, newpath)
    clearcache(self)

# def usersave(self, *args, **kwargs):
#     Node = apps.get_model('objects', 'node')
#     # Setup New and Deleted Variables
#     is_new = self._state.adding
#     is_deleted = '_' if self.deleted is True else ''
#     # Set UUID if None
#     if self.uuid is None:
#         self.uuid = uuid.uuid4()
#     # Force Parent
#     if self.PARENT_URL:
#         try:
#             self.parent = Node.objects.exclude(
#                 uuid=self.uuid).get(url=self.PARENT_URL)
#         except Node.DoesNotExist:
#             pass
#     # Track URL Changes
#     urlchanged = False
#     parent_url = self.parent.url if self.parent else self.PARENT_URL
#     if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + urlclean_objname(str(self.email).split('@', 1)[0]) + '/'):
#         oldurl = self.url
#         self.url = urlclean_remdoubleslashes(
#             '/' + parent_url + '/' + urlclean_objname(str(self.email).split('@', 1)[0]) + '/')
#         if not is_new:
#             urlchanged = True
#     # Set Username
#     if self.username:
#         self.node_title = self.username
#     # Set the node type
#     self.node_type = self._meta.app_label
#     # Set the content type
#     self.user_type = self._meta.model_name
#     self.content_type = self._meta.model_name
#     # Does this item have permissions?
#     if self.HAS_PERMISSIONS:
#         self.has_permissions = True
#     else:
#         self.has_permissions = False
#     # Save the item
#     super(self._meta.model, self).save(*args, **kwargs)
#     # Set the user type node
#     #self.node_type = self.user._meta.model_name
#     if urlchanged:
#             # Save Children
#         for child in self.get_children():
#             object = nodefindobject(child)
#             object.save()
#         # Move Directory
#         silentmove_media(settings.MEDIA_ROOT + oldurl,
#                          settings.MEDIA_ROOT + self.url)


# def pagesave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   User = apps.get_model('objects','user')
#   f = open('/tmp/movingfile.txt', 'a')
#   f.write('Saving Page ' + '\n')
#   f.close()
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Title
#   if self._meta.model_name == 'superintendentmessage':
#       if not self.title:
#           self.title = 'Superintendent\'s Message ' + self.author_date.strftime('%Y-%m-%d')
#   if self._meta.model_name == 'news' or self._meta.model_name == 'superintendentmessage':
#     if self.author_date.month >= 7:
#       yearend = self.author_date.year + 1
#       yearstring = str(self.author_date.year) + '-' + str(self.author_date.year + 1)[2:]
#     else:
#       yearend=self.author_date.year
#       yearstring = str(self.author_date.year - 1) + '-' + str(self.author_date.year)[2:]
#     try:
#       yearobject = self.PARENT_TYPE.objects.get(yearend=yearend)
#     except self.PARENT_TYPE.DoesNotExist:
#       webmaster = User.objects.get(username='webmaster@slcschools.org')
#       parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL)
#       yearobject = self.PARENT_TYPE(title=yearstring, yearend=yearend, parent=parent, create_user=webmaster, update_user=webmaster)
#       yearobject.save()
#     self.parent = Node.objects.get(url=yearobject.url)
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else ''
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/'): 
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Related Node matches Parent
#   try:
#     if self._meta.get_field('related_node'):
#       self.related_node = self.parent
#   except FieldDoesNotExist:
#     pass
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.page_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # if not self.menu_title:
#   #   self.menu_title = self.title
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   f = open('/tmp/movingfile.txt', 'a')
#   f.write('Page URL Changed: ' + str(urlchanged) + ' From: ' + oldurl + ' To: ' + self.url +  '\n')
#   f.close()
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def taxonomysave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     oldurl = self.url 
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Related Node matches Parent
#   try:
#     if self._meta.get_field('related_node'):
#       self.related_node = self.parent
#   except FieldDoesNotExist:
#     pass
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.taxonomy_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def imagesave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   f = open('/tmp/movingfile.txt', 'a')
#   f.write('Saving Image ' + '\n')
#   f.close()
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Title
#   if self._meta.model_name == 'districtlogo':
#     self.title = self.district_logo_group.title + ' ' + self.district_logo_style_variation.title
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Move Files
#   currentname = None
#   newname = None
#   try:
#       if self.image_file:
#           currentname = findfileext_media(self.image_file.name)
#           newname = image_upload_to(self,currentname[0] + currentname[1])
#           currentname = '/'.join (newname.split('/')[:-1]) + '/' + currentname[0] + currentname[1]
#           self.image_file.name = newname
#   except AttributeError:
#       pass
      
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.image_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   f = open('/tmp/movingfile.txt', 'a')
#   f.write('Image URL Changed: ' + str(urlchanged) + ' From: ' + oldurl + ' To: ' + self.url +  '\n')
#   f.close()
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   # Move File
#   if currentname != newname:
#     silentmove_media(settings.MEDIA_ROOT + '/' + currentname, settings.MEDIA_ROOT + '/' + newname)
#   clearcache(self)


# def directoryentrysave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   if not self.title:
#     #Force Title
#     self.title = urlclean_objname(str(self.employee.email).split('@', 1)[0])
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.image_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def linksave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.link_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def filesave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   #Force Title
#   if self._meta.model_name == 'file':
#     self.title = self.parent.node_title + ' (' + self.file_language.title + ')'
#   if self._meta.model_name == 'audiofile':
#     self.title = self.parent.node_title
#   if self._meta.model_name == 'videofile':
#     self.title = self.parent.node_title 
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self._meta.model_name == 'file':
#     if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.file_language.title) + '/'):
#       self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.file_language.title) + '/')
#       if not is_new:
#         urlchanged = True
#   else:
#     if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self._meta.model_name) + '/'):
#       self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self._meta.model_name) + '/')
#       if not is_new:
#         urlchanged = True
#   # Move Files
#   currentname = None
#   newname = None
#   if self.file_file:
#       currentname = findfileext_media(self.file_file.name)
#       newname = file_upload_to(self,currentname[0] + currentname[1])
#       currentname = '/'.join (newname.split('/')[:-1]) + '/' + currentname[0] + currentname[1]
#       self.file_file.name = newname
      
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.link_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   # Move File
#   if currentname != newname:
#     silentmove_media(settings.MEDIA_ROOT + '/' + currentname, settings.MEDIA_ROOT + '/' + newname)
#   clearcache(self)


# def documentsave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Set Title
#   if self._meta.model_name == 'boardpolicy':
#     self.title = self.section.section_prefix + '-' + str(self.index)
#   if self._meta.model_name == 'policy':
#     self.title = self.parent.node_title + ' Policy'
#   if self._meta.model_name == 'administrativeprocedure':
#     self.title = self.parent.node_title + ' AP'
#   if self._meta.model_name == 'supportingdocument':
#     if (( not self.document_title ) and self.title) or self.title != self.node_title:
#         self.document_title = re.sub(r'^' + re.escape(self.parent.node_title) + '[ ]?','',self.title).strip()
#     self.title = self.parent.node_title + ' ' + self.document_title
#   if self._meta.model_name == 'boardmeetingagenda':
#     self.title = self.parent.node_title + ' Agenda'
#   if self._meta.model_name == 'boardmeetingminutes':
#     self.title = self.parent.node_title + ' Minutes'
#   if self._meta.model_name == 'boardmeetingaudio':
#     self.title = self.parent.node_title + ' Audio'
#   if self._meta.model_name == 'boardmeetingvideo':
#     self.title = self.parent.node_title + ' Video'
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.link_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)  


# def eventsave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   User = apps.get_model('objects','user')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   if self._meta.model_name == 'boardmeeting' or self._meta.model_name == 'districtcalendarevent':
#     if self.startdate.month >= 7:
#       yearend = self.startdate.year + 1
#       yearstring = str(self.startdate.year) + '-' + str(self.startdate.year + 1)[2:]
#     else:
#       yearend=self.startdate.year
#       yearstring = str(self.startdate.year - 1) + '-' + str(self.startdate.year)[2:]
#     try:
#       yearobject = self.PARENT_TYPE.objects.get(yearend=yearend)
#     except self.PARENT_TYPE.DoesNotExist:
#       webmaster = User.objects.get(username='webmaster@slcschools.org')
#       parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL)
#       yearobject = self.PARENT_TYPE(title=yearstring, yearend=yearend, parent=parent, create_user=webmaster, update_user=webmaster)
#       yearobject.save()
#     self.parent = Node.objects.get(url=yearobject.url)
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Set Original Date & Original Instance
#   if (not self.originaldate) and self.startdate:
#     self.originaldate = self.startdate
#     self.originalinstance = len(self._meta.model.objects.filter(originaldate=self.originaldate)) + 1
#   # Set Title & Prefix
#   if self._meta.model_name == 'boardmeeting':
#     self.title = timezone.localtime(self.originaldate).strftime('%Y%m%d-%H%M') + '-' +  str(self.originalinstance)
#     #self.URL_PREFIX = str(self.pk)[0:8]
#   elif self._meta.model_name == 'districtcalendarevent':
#     self.title = timezone.localtime(self.originaldate).strftime('%Y%m%d-%H%M') + '-' +  str(self.originalinstance)
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.link_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Set Event School Year and Year End fields
#   self.schoolyear = str(currentyear(self.startdate)['currentyear']['long'])
#   self.yearend = str(currentyear(self.startdate)['currentyear']['short'])
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def faqsave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   # Set title to uuid
#   self.title = str(self.uuid)
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.image_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# def contactmessagesave(self, *args, **kwargs):
#   Node = apps.get_model('objects','node')
#   # Setup New and Deleted Variables
#   is_new = self._state.adding
#   is_deleted = '_' if self.deleted == True else ''
#   # Set UUID if None
#   if self.uuid is None:
#     self.uuid = uuid.uuid4()
#   # Set title to uuid
#   self.title = str(self.uuid)
#   #Force Parent
#   if self.PARENT_URL:
#     try:
#       self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
#     except Node.DoesNotExist:
#       pass
#   # Related Node matches Parent
#   self.related_node = self.parent
#   # Track URL Changes
#   urlchanged = False
#   parent_url = self.parent.url if self.parent else self.PARENT_URL
#   if not self.url.startswith(parent_url):
#     try:
#       self.url = Node.objects.get(pk=self.pk).url
#     except Node.DoesNotExist:
#       pass
#   oldurl = self.url
#   if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
#     self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
#     if not is_new:
#       urlchanged = True
#   # Set the node_title for the node
#   self.node_title = self.title
#   # Set the node type
#   self.node_type = self._meta.app_label
#   # Set the content type
#   self.image_type = self._meta.model_name
#   self.content_type = self._meta.model_name
#   # Does this item have permissions?
#   if self.HAS_PERMISSIONS:
#     self.has_permissions = True
#   else:
#     self.has_permissions = False
#   # Save the item
#   super(self._meta.model, self).save(*args, **kwargs)
#   if urlchanged:
#       # Save Children
#       for child in self.get_children():
#         object = nodefindobject(child)
#         object.save()
#       # Move Directory
#       silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
#   clearcache(self)


# Model Inheritance Object
def nodefindobject(node):
    return apps.get_model(
        node.node_type + '.' + node.content_type).objects.get(pk=node.pk)


def objectfindnode(object):
    Node = apps.get_model('objects', 'node')
    return Node.objects.get(pk=object.pk)


# MPTT Tree Functions
def resetchildrentoalphatitle():
    Node = apps.get_model('objects', 'node')
    top = Node.objects.filter(node_type='pages').get(
        node_title='Charter Schools')
    children = top.get_children()
    children = children.order_by('node_title')
    parent = children[0]
    parent.move_to(top, position='first-child')
    for child in children[1:]:
        parent = Node.objects.get(pk=parent.pk)
        child = Node.objects.get(pk=child.pk)
        child.move_to(parent, position='right')
        'Moving {0} after {1}'.format(child, parent)
        parent = child


# Cache Functions
def clearcache(object):
    pass


def save_formset(self, request, form, formset, change):
    # formset.save() returns instances but
    # I do not need them so I am not storing them.
    formset.save(commit=False)
    for obj in formset.deleted_objects:
        obj.delete()
    for obj in formset.new_objects:
        obj.create_user = request.user
        obj.update_user = request.user
        obj.site = request.site
        obj.primary_contact = request.user
        obj.save()
    for obj in formset.changed_objects:
        obj[0].update_user = request.user
        obj[0].save()
    formset.save_m2m()


def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
        obj.create_user = request.user
    obj.update_user = request.user
    if getattr(obj, 'site', None) is None:
        obj.site = request.site
    super(self.__class__, self).save_model(request, obj, form, change)


def response_change(self, request, obj):
    if 'next' in request.GET:
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            'name': force_text(opts.verbose_name),
            'obj': format_html(
                '<a class="editlink" href="{}">{}</a>',
                urlquote(request.path), obj),
        }

        if "_continue" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully.'
                  'You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.get_full_path()
            redirect_url = add_preserved_filters({
                'preserved_filters': preserved_filters,
                'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        if '_continue' not in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect(
                base64.b64decode(request.GET['next']).decode('utf-8'))
    return super(self.__class__, self).response_change(request, obj)


def get_district_office():
    Location = apps.get_model('taxonomy', 'location')
    try:
        return Location.objects.get(title='District Office').pk
    except Location.DoesNotExist:
        return ''


def get_districtcalendareventcategory_general():
    DistrictCalendarEventCategory = apps.get_model(
        'taxonomy',
        'districtcalendareventcategory'
    )
    try:
        return DistrictCalendarEventCategory.objects.get(
            title='General Event').pk
    except DistrictCalendarEventCategory.DoesNotExist:
        return ''


def get_webmaster(pk=True):
    User = apps.get_model('objects', 'user')
    try:
        webmaster = User.objects.get(username='webmaster@slcschools.org')
        if pk:
            return webmaster.pk
        else:
            return webmaster
    except User.DoesNotExist:
        return ''


def get_contactpage(pk=True):
    Node = apps.get_model('objects', 'node')
    try:
        page = Node.objects.get(node_title='Contact Us')
        if pk:
            return page.pk
        else:
            return page
    except Node.DoesNotExist:
        return ''


def currentyear(date=timezone.now()):
    if date.month >= 7:
        currentyearkey = date.year + 1
        currentyearstring = str(date.year) + '-' + str(date.year + 1)[2:]
    else:
        currentyearkey = date.year
        currentyearstring = str(date.year-1) + '-' + str(date.year)[2:]
    currentyear = {"short": currentyearkey, "long": currentyearstring}
    return {'currentyear': currentyear}


def next_tuesday_sixthrity():
    now = timezone.datetime.strptime(
        timezone.datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
    while now.weekday() != 1:
        now += timedelta(days=1)
    now += timedelta(hours=18-int(now.strftime('%H')))
    now += timedelta(minutes=30-int(now.strftime('%M')))
    return timezone.make_aware(now)


def tomorrow_midnight():
    now = timezone.datetime.strptime(
        timezone.datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
    now += timedelta(days=1)
    now += timedelta(hours=0-int(now.strftime('%H')))
    now += timedelta(minutes=0-int(now.strftime('%M')))
    return timezone.make_aware(now)
