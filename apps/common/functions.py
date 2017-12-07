import os
import shutil
import re
import uuid
from django.conf import settings
from django.contrib.auth import get_permission_codename
from guardian.shortcuts import get_perms
from apps.objects.models import Node, User
from django.core.cache import cache
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist

# Required for response change
import base64
from django.utils.translation import ugettext as _, ungettext
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.utils.http import urlencode, urlquote
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters

def findfileext_media(media):
  media = media.split('/')[-1:]
  return os.path.splitext(media[0])

def urlclean_fileext(fileext):
  return re.sub('-+','-',re.sub(r'([\s+])','-',re.sub(r'([^.a-z0-9\s-])','',fileext.lower())))

def urlclean_objname(objname):
  return re.sub('-+','-',re.sub(r'([\s+])','-',re.sub(r'([^a-z0-9\s-])','',objname.lower())))

def urlclean_remdoubleslashes(objname):
  return re.sub('/+','/',objname.lower())

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
  if request.user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('add',self.model._meta)):
    return True
  elif obj:
    if get_permission_codename('add',self.model._meta) in get_perms(request.user, obj):
      return True
  return False

def has_change_permission(self, request, obj=None):
  if self != None:
    # Check for regular global model permission
    if request.user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('change',self.model._meta)):
      return True
  if obj:
    if obj.has_permissions:
      # Check for object level permission through Guardian
      if get_permission_codename('change',obj._meta) in get_perms(request.user, obj):
        return True
    else:
      node = objectfindnode(obj)
      permission_point = nodefindobject(node.get_ancestors().filter(has_permissions=True).last())
      if get_permission_codename('change',permission_point._meta) in get_perms(request.user, permission_point):
        return True
  return False

def has_delete_permission(self, request, obj=None):
  if request.user.has_perm(self.model._meta.app_label + '.' + get_permission_codename('trash',self.model._meta)):
    return True
  elif obj:
    if obj.has_permissions:
      # Check for object level permission through Guardian
      if get_permission_codename('trash',self.model._meta) in get_perms(request.user, obj):
        return True
    else:
      node = objectfindnode(obj)
      permission_point = nodefindobject(node.get_ancestors().filter(has_permissions=True).last())
      if get_permission_codename('change',permission_point._meta) in get_perms(request.user, permission_point):
        return True
  return False

def has_add_permission_inline(self, request, obj=None):
  # Allow if object is new (should always be new)
  if obj == None:
    return True
  return False

def has_change_permission_inline(self, request, obj=None):
  if obj == None:
    return True
  if has_change_permission(self, request, obj):
    return True
  return False

def has_delete_permission_inline(self, request, obj=None):
  if obj == None:
    return True
  if  has_delete_permission(self, request, obj):
    return True
  return False

def modeltrash(self, *args, **kwargs):
    if self.deleted == 0:
      self.deleted = 1;
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
  title = urlclean_objname(instance.title)
  original_file, original_extension = findfileext_media(filename)
  extension = urlclean_fileext(original_extension)
  full_path = '{0}{1}{2}'.format(url,title, extension)
  if not instance.image_file._committed:
    silentdelete_media(settings.MEDIA_ROOT + '/' + full_path)
  return full_path

# Upload File Functions

def file_upload_to(instance, filename):
  url = instance.url[1:]
  title = urlclean_objname(instance.title)
  original_file, original_extension = findfileext_media(filename)
  extension = urlclean_fileext(original_extension)
  full_path = '{0}{1}{2}'.format(url,title, extension)
  if not instance.file_file._committed:
    silentdelete_media(settings.MEDIA_ROOT + '/' + full_path)
  return full_path

# Save Content Functions

def usersave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' +  urlclean_objname(str(self.email).split('@', 1)[0]) + '/'):
    oldurl = self.url 
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' +  urlclean_objname(str(self.email).split('@', 1)[0]) + '/')
    if not is_new:
      urlchanged = True
  # Set Username
  if self.username:
    self.node_title = self.username
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.user_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  # Set the user type node
  #self.node_type = self.user._meta.model_name
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)


def pagesave(self, *args, **kwargs):
  f = open('/tmp/movingfile.txt', 'a')
  f.write('Saving Page ' + '\n')
  f.close()
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  if self._meta.model_name == 'news':
    if self.author_date.month >= 7:
      yearend = self.author_date.year + 1
      yearstring = str(self.author_date.year) + '-' + str(self.author_date.year + 1)[2:]
    else:
      yearend=self.author_date.year
      yearstring = str(self.author_date.year - 1) + '-' + str(self.author_date.year)[2:]
    try:
      newsyear = self.PARENT_TYPE.objects.get(yearend=yearend)
    except self.PARENT_TYPE.DoesNotExist:
      webmaster = User.objects.get(username='webmaster@slcschools.org')
      parent = Node.objects.get(node_title='News', content_type='page')
      newsyear = self.PARENT_TYPE(title=yearstring, yearend=yearend, parent=parent, create_user=webmaster, update_user=webmaster)
      newsyear.save()
    self.parent = Node.objects.get(url=newsyear.url)
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else ''
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/'): 
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Related Node matches Parent
  try:
    if self._meta.get_field('related_node'):
      self.related_node = self.parent
  except FieldDoesNotExist:
    pass
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.page_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # if not self.menu_title:
  #   self.menu_title = self.title
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  f = open('/tmp/movingfile.txt', 'a')
  f.write('Page URL Changed: ' + str(urlchanged) + ' From: ' + oldurl + ' To: ' + self.url +  '\n')
  f.close()
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)

def taxonomysave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    oldurl = self.url 
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Related Node matches Parent
  try:
    if self._meta.get_field('related_node'):
      self.related_node = self.parent
  except FieldDoesNotExist:
    pass
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.taxonomy_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)

def imagesave(self, *args, **kwargs):
  f = open('/tmp/movingfile.txt', 'a')
  f.write('Saving Image ' + '\n')
  f.close()
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Related Node matches Parent
  self.related_node = self.parent
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Move Files
  currentname = None
  newname = None
  if self.image_file:
      currentname = findfileext_media(self.image_file.name)
      newname = image_upload_to(self,currentname[0] + currentname[1])
      currentname = '/'.join (newname.split('/')[:-1]) + '/' + currentname[0] + currentname[1]
      self.image_file.name = newname
      
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.image_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  f = open('/tmp/movingfile.txt', 'a')
  f.write('Image URL Changed: ' + str(urlchanged) + ' From: ' + oldurl + ' To: ' + self.url +  '\n')
  f.close()
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  # Move File
  if currentname != newname:
    silentmove_media(settings.MEDIA_ROOT + '/' + currentname, settings.MEDIA_ROOT + '/' + newname)
  clearcache(self)

def directoryentrysave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  if not self.title:
    #Force Title
    self.title = urlclean_objname(str(self.employee.email).split('@', 1)[0])
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Related Node matches Parent
  self.related_node = self.parent
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.image_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)

def linksave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.link_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)

def filesave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  #Force Title
  self.title = self.parent.node_title + ' (' + self.file_language.title + ')'
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Related Node matches Parent
  self.related_node = self.parent
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.file_language.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.file_language.title) + '/')
    if not is_new:
      urlchanged = True
  # Move Files
  currentname = None
  newname = None
  if self.file_file:
      currentname = findfileext_media(self.file_file.name)
      newname = file_upload_to(self,currentname[0] + currentname[1])
      currentname = '/'.join (newname.split('/')[:-1]) + '/' + currentname[0] + currentname[1]
      self.file_file.name = newname
      
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.link_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  # Move File
  if currentname != newname:
    silentmove_media(settings.MEDIA_ROOT + '/' + currentname, settings.MEDIA_ROOT + '/' + newname)
  clearcache(self)

def documentsave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  # Related Node matches Parent
  self.related_node = self.parent
  # Set Title
  if self._meta.model_name == 'boardpolicy':
    self.title = self.section.section_prefix + '-' + str(self.index)
  if self._meta.model_name == 'policy':
    self.title = self.parent.node_title + ' Policy'
  if self._meta.model_name == 'administrativeprocedure':
    self.title = self.parent.node_title + ' AP'
  if self._meta.model_name == 'supportingdocument':
    if (( not self.document_title ) and self.title) or self.title != self.node_title:
        self.document_title = re.sub(r'^' + re.escape(self.parent.node_title) + '[ ]?','',self.title).strip()
    self.title = self.parent.node_title + ' ' + self.document_title
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.link_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)  

def eventsave(self, *args, **kwargs):
  # Setup New and Deleted Variables
  is_new = self._state.adding
  is_deleted = '_' if self.deleted == True else ''
  # Set UUID if None
  if self.uuid is None:
    self.uuid = uuid.uuid4()
  #Force Parent
  if self.PARENT_URL:
    try:
      self.parent = Node.objects.exclude(uuid=self.uuid).get(url=self.PARENT_URL)
    except Node.DoesNotExist:
      pass
  if self._meta.model_name == 'boardmeeting':
    if self.author_date.month >= 7:
      yearend = self.startdate.year + 1
      yearstring = str(self.startdate.year) + '-' + str(self.startdate.year + 1)[2:]
    else:
      yearend=self.startdate.year
      yearstring = str(self.startdate.year - 1) + '-' + str(self.startdate.year)[2:]
    try:
      newsyear = self.PARENT_TYPE.objects.get(yearend=yearend)
    except self.PARENT_TYPE.DoesNotExist:
      webmaster = User.objects.get(username='webmaster@slcschools.org')
      parent = Node.objects.get(node_title='Board Meetings', content_type='boardsubpage')
      boardmeetingyear = self.PARENT_TYPE(title=yearstring, yearend=yearend, parent=parent, create_user=webmaster, update_user=webmaster)
      boardmeeting.save()
    self.parent = Node.objects.get(url=newsyear.url)
  # Related Node matches Parent
  self.related_node = self.parent
  # Set Title
  if self._meta.model_name == 'boardmeeting':
    self.title = self.section.section_prefix + '-' + str(self.index)
  # Track URL Changes
  urlchanged = False
  parent_url = self.parent.url if self.parent else self.PARENT_URL
  if not self.url.startswith(parent_url):
    try:
      self.url = Node.objects.get(pk=self.pk).url
    except Node.DoesNotExist:
      pass
  oldurl = self.url
  if self.url != urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/'):
    self.url = urlclean_remdoubleslashes('/' + parent_url + '/' + self.URL_PREFIX + '/' + is_deleted + urlclean_objname(self.title) + '/')
    if not is_new:
      urlchanged = True
  # Set the node_title for the node
  self.node_title = self.title
  # Set the node type
  self.node_type = self._meta.app_label
  # Set the content type
  self.link_type = self._meta.model_name
  self.content_type = self._meta.model_name
  # Does this item have permissions?
  if self.HAS_PERMISSIONS:
    self.has_permissions = True
  else:
    self.has_permissions = False
  # Save the item
  super(self._meta.model, self).save(*args, **kwargs)
  if urlchanged:
      # Save Children
      for child in self.get_children():
        object = nodefindobject(child)
        object.save()
      # Move Directory
      silentmove_media(settings.MEDIA_ROOT + oldurl, settings.MEDIA_ROOT + self.url)
  clearcache(self)

# Model Inheritance Object
def nodefindobject(node):
  return apps.get_model(node.node_type + '.' + node.content_type).objects.get(pk=node.pk)

def objectfindnode(object):
  return Node.objects.get(pk=object.pk)

# MPTT Tree Functions
def resetchildrentoalphatitle():
  top = Node.objects.filter(node_type='pages').get(node_title='Charter Schools')
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
    sleep(1)

# Cache Functions
def clearcache(object):
  pass

def response_change(self, request, obj):
    if 'next' in request.GET:
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            'name': force_text(opts.verbose_name),
            'obj': format_html('<a class="editlink" href="{}">{}</a>', urlquote(request.path), obj),
        }

        if "_continue" in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully. You may edit it again below.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.get_full_path()
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)
        if '_continue' not in request.POST:
            msg = format_html(
                _('The {name} "{obj}" was changed successfully.'),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponseRedirect(base64.b64decode(request.GET['next']).decode('utf-8'))
    return super(self.__class__, self).response_change(request, obj)
