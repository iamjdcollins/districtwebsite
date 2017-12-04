from django.db import models
import apps.common.functions
from apps.objects.models import Node, Image

class Thumbnail(Image):

  PARENT_URL = ''
  URL_PREFIX = '/images/thumbnails/'

  title = models.CharField(max_length=200, help_text='')
  image_file = models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image', help_text='')
  alttext = models.CharField(max_length=200, verbose_name='Alternative Text', help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='images_thumbnail_node', editable=False)

  thumbnail_image_node = models.OneToOneField(Image, db_column='thumbnail_image_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'images_thumbnail'
    get_latest_by = 'update_date'
    permissions = (('trash_thumbnail', 'Can soft delete thumbnail'),('restore_thumbnail', 'Can restore thumbnail'))
    verbose_name = 'Thumbnail'
    verbose_name_plural = 'Thumbnails'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.imagesave
  delete = apps.common.functions.modeltrash

class NewsThumbnail(Image):

  PARENT_URL = ''
  URL_PREFIX = '/images/newsthumbnails/'

  title = models.CharField(max_length=200, help_text='')
  image_file = models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image', help_text='')
  alttext = models.CharField(max_length=200, verbose_name='Alternative Text', help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='images_newsthumbnail_node', editable=False)

  newsthumbnail_image_node = models.OneToOneField(Image, db_column='newsthumbnail_image_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'images_newsthumbnail'
    get_latest_by = 'update_date'
    permissions = (('trash_newsthumbnail', 'Can soft delete news thumbnail'),('restore_thumbnail', 'Can restore news thumbnail'))
    verbose_name = 'News Thumbnail'
    verbose_name_plural = 'News Thumbnails'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.imagesave
  delete = apps.common.functions.modeltrash

class PageBanner(Image):

  PARENT_URL = ''
  URL_PREFIX = '/images/pagebanners/'

  title = models.CharField(max_length=200, help_text='')
  image_file = models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image', help_text='')
  alttext = models.CharField(max_length=200, verbose_name='Alternative Text', help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='images_pagebanner_node', editable=False)

  pagebanner_image_node = models.OneToOneField(Image, db_column='pagebanner_image_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'images_pagebanner'
    get_latest_by = 'update_date'
    permissions = (('trash_pagebanner', 'Can soft delete page banner'),('restore_pagebanner', 'Can restore page banner'))
    verbose_name = 'Page Banner'
    verbose_name_plural = 'Page Banners'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.imagesave
  delete = apps.common.functions.modeltrash

class ContentBanner(Image):

  PARENT_URL = ''
  URL_PREFIX = '/images/contentbanners/'

  title = models.CharField(max_length=200, help_text='')
  image_file = models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image', help_text='')
  alttext = models.CharField(max_length=200, verbose_name='Alternative Text', help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='images_contentbanner_node', editable=False)

  contentbanner_image_node = models.OneToOneField(Image, db_column='contentbanner_image_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'images_contentbanner'
    get_latest_by = 'update_date'
    permissions = (('trash_contentbanner', 'Can soft delete content banner'),('restore_contentbanner', 'Can restore content banner'))
    verbose_name = 'Content Banner'
    verbose_name_plural = 'Content Banners'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.imagesave
  delete = apps.common.functions.modeltrash

class ProfilePicture(Image):

  PARENT_URL = ''
  URL_PREFIX = '/images/profilepictures/'

  title = models.CharField(max_length=200, help_text='')
  image_file = models.ImageField(max_length=2000, upload_to=apps.common.functions.image_upload_to, verbose_name='Image', help_text='')
  alttext = models.CharField(max_length=200, verbose_name='Alternative Text', help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='images_profilepicture_node', editable=False)

  profilepicture_image_node = models.OneToOneField(Image, db_column='profilepicture_image_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'images_profilepicture'
    get_latest_by = 'update_date'
    permissions = (('trash_profilepicture', 'Can soft delete profile picture'),('restore_profilepicture', 'Can restore profile picture'))
    verbose_name = 'Profile Picture'
    verbose_name_plural = 'Profile Pictures'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.imagesave
  delete = apps.common.functions.modeltrash
