from django.db import models
from django.conf import settings
import uuid
from mptt.models import MPTTModel, TreeForeignKey
from apps.common.functions import get_webmaster
from django.contrib.auth.models import AbstractUser

class Node(MPTTModel):

  HAS_PERMISSIONS = False

  uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,)
  node_title = models.CharField(max_length=200,)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='objects_node_parent', db_index=True)
  url = models.CharField(max_length=2000, unique=True, db_index=True)
  node_type = models.CharField(max_length=200, editable=False, null=True, blank=True, db_index=True)
  content_type = models.CharField(max_length=200, editable=False, null=True, blank=True, db_index=True)
  menu_item = models.BooleanField(default=False, db_index=True)
  menu_title = models.CharField(max_length=200, null=True, blank=True)
  primary_contact = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=False, to_field='uuid', on_delete=models.PROTECT, related_name='objects_node_primary_contact')
  has_permissions = models.BooleanField(default=False,db_index=True)
  create_date = models.DateTimeField(auto_now_add=True, db_index=True)
  create_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, to_field='uuid', on_delete=models.DO_NOTHING, related_name='objects_node_create_user')
  update_date = models.DateTimeField(auto_now=True, db_index=True)
  update_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, to_field='uuid', on_delete=models.DO_NOTHING, related_name='objects_node_update_user')
  published = models.BooleanField(default=True,db_index=True)
  deleted = models.BooleanField(default=False,db_index=True)
  searchable = models.BooleanField(default=True,db_index=True)

  class Meta:
    db_table = 'objects_node'
    get_latest_by = 'create_date'
    verbose_name = 'Node'
    verbose_name_plural = 'Nodes'
    #unique_together = (('parent', 'node_title'),)

  def __str__(self):
    return self.node_title

class User(AbstractUser, Node):
  user_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  user_node = models.OneToOneField(Node, db_column='user_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_user'
    get_latest_by = 'create_date'
    verbose_name = 'User'
    verbose_name_plural = 'Users'
    default_manager_name = 'objects'

class Page(Node):
  page_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  page_node = models.OneToOneField(Node, db_column='page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_page'
    get_latest_by = 'create_date'
    verbose_name = 'Page'
    verbose_name_plural = 'Pages'
    default_manager_name = 'objects'

class Taxonomy(Node):
  taxonomy_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  taxonomy_node = models.OneToOneField(Node, db_column='taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_taxonomy'
    get_latest_by = 'create_date'
    verbose_name = 'Taxonomy'
    verbose_name_plural = 'Taxonomies'
    default_manager_name = 'objects'

class Image(Node):
  image_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  image_node = models.OneToOneField(Node, db_column='image_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_image'
    get_latest_by = 'create_date'
    verbose_name = 'Image'
    verbose_name_plural = 'Images'
    default_manager_name = 'objects'

class DirectoryEntry(Node):
  directoryentry_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  directoryentry_node = models.OneToOneField(Node, db_column='directoryentry_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_directoryentry'
    get_latest_by = 'create_date'
    verbose_name = 'Directory Entry'
    verbose_name_plural = 'Directory Entries'
    default_manager_name = 'objects'

class Link(Node):
  link_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  link_node = models.OneToOneField(Node, db_column='link_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_link'
    get_latest_by = 'create_date'
    verbose_name = 'Link'
    verbose_name_plural = 'Links'
    default_manager_name = 'objects'

class File(Node):
  file_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  file_node = models.OneToOneField(Node, db_column='file_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_file'
    get_latest_by = 'create_date'
    verbose_name = 'File'
    verbose_name_plural = 'Files'
    default_manager_name = 'objects'

class Document(Node):
  document_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  document_node = models.OneToOneField(Node, db_column='document_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_document'
    get_latest_by = 'create_date'
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'
    default_manager_name = 'objects'

class Event(Node):
  event_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  event_node = models.OneToOneField(Node, db_column='event_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_event'
    get_latest_by = 'create_date'
    verbose_name = 'Event'
    verbose_name_plural = 'Events'
    default_manager_name = 'objects'

class FAQ(Node):
  faq_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  faq_node = models.OneToOneField(Node, db_column='faq_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_faq'
    get_latest_by = 'create_date'
    verbose_name = 'FAQ'
    verbose_name_plural = 'FAQs'
    default_manager_name = 'objects'

class Message(Node):
  messagae_type = models.CharField(max_length=200, editable=False, null=True, blank=True)

  message_node = models.OneToOneField(Node, db_column='message_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'objects_message'
    get_latest_by = 'create_date'
    verbose_name = 'Message'
    verbose_name_plural = 'Messages'
    default_manager_name = 'objects'
