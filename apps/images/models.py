from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Image
from apps.taxonomy.models import DistrictLogoGroup, DistrictLogoStyleVariation


class Thumbnail(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/thumbnails/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_thumbnail_node',
        editable=False,
    )

    thumbnail_image_node = models.OneToOneField(
        Image,
        db_column='thumbnail_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_thumbnail'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_thumbnail', 'Can soft delete thumbnail'),
            ('restore_thumbnail', 'Can restore thumbnail'),
        )
        verbose_name = 'Thumbnail'
        verbose_name_plural = 'Thumbnails'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class NewsThumbnail(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/newsthumbnails/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',)
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_newsthumbnail_node',
        editable=False,
    )

    newsthumbnail_image_node = models.OneToOneField(
        Image,
        db_column='newsthumbnail_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_newsthumbnail'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_newsthumbnail', 'Can soft delete news thumbnail'),
            ('restore_thumbnail', 'Can restore news thumbnail'),
        )
        verbose_name = 'News Thumbnail'
        verbose_name_plural = 'News Thumbnails'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class PageBanner(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/pagebanners/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_pagebanner_node',
        editable=False,
    )

    pagebanner_image_node = models.OneToOneField(
        Image,
        db_column='pagebanner_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_pagebanner'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_pagebanner', 'Can soft delete page banner'),
            ('restore_pagebanner', 'Can restore page banner'),
        )
        verbose_name = 'Page Banner'
        verbose_name_plural = 'Page Banners'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class ContentBanner(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/contentbanners/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_contentbanner_node',
        editable=False,
    )

    contentbanner_image_node = models.OneToOneField(
        Image,
        db_column='contentbanner_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    inline_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        db_table = 'images_contentbanner'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_contentbanner', 'Can soft delete content banner'),
            ('restore_contentbanner', 'Can restore content banner'),
        )
        verbose_name = 'Content Banner'
        verbose_name_plural = 'Content Banners'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class ProfilePicture(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/profilepictures/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_profilepicture_node',
        editable=False,
    )

    profilepicture_image_node = models.OneToOneField(
        Image,
        db_column='profilepicture_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_profilepicture'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_profilepicture', 'Can soft delete profile picture'),
            ('restore_profilepicture', 'Can restore profile picture'),
        )
        verbose_name = 'Profile Picture'
        verbose_name_plural = 'Profile Pictures'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoGIF(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/districtlogosgifs/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_districtlogogif_node',
        editable=False,
    )

    districtlogogif_image_node = models.OneToOneField(
        Image,
        db_column='districtlogogif_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_districtlogogif'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogogif', 'Can soft delete district logo gif'),
            ('restore_districtlogogif', 'Can restore district logo gif'),
        )
        verbose_name = 'District Logo GIF'
        verbose_name_plural = 'District Logo GIFs'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoJPG(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/districtlogosjpgs/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_districtlogojpg_node',
        editable=False,
    )

    districtlogojpg_image_node = models.OneToOneField(
        Image,
        db_column='districtlogojpg_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_districtlogojpg'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogojpg', 'Can soft delete district logo jpg'),
            ('restore_districtlogojpg', 'Can restore district logo jpg'),
        )
        verbose_name = 'District Logo JPG'
        verbose_name_plural = 'District Logo JPGs'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoPNG(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/districtlogospngs/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_districtlogopng_node',
        editable=False,
    )

    districtlogopng_image_node = models.OneToOneField(
        Image,
        db_column='districtlogopng_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_districtlogopng'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogopng', 'Can soft delete district logo png'),
            ('restore_districtlogopng', 'Can restore district logo png'),
        )
        verbose_name = 'District Logo PNG'
        verbose_name_plural = 'District Logo PNGs'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoTIF(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/districtlogostifs/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_districtlogotif_node',
        editable=False,
    )

    districtlogotif_image_node = models.OneToOneField(
        Image,
        db_column='districtlogotif_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_districtlogotif'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogotif', 'Can soft delete district logo tif'),
            ('restore_districtlogotif', 'Can restore district logo tif'),
        )
        verbose_name = 'District Logo TIF'
        verbose_name_plural = 'District Logo TIFs'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogo(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    district_logo_group = models.ForeignKey(
        DistrictLogoGroup,
        limit_choices_to={
            'deleted': False,
            'published': True,
        },
        related_name='images_districtlogo_district_logo_group',
        on_delete=models.PROTECT,
        verbose_name='District Logo Group',
        help_text='',
    )
    district_logo_style_variation = models.ForeignKey(
        DistrictLogoStyleVariation,
        limit_choices_to={
            'deleted': False,
            'published': True,
        },
        related_name='images_districtlogo_district_logo_style_variation',
        on_delete=models.PROTECT,
        verbose_name='District Logo Style Variation',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_districtlogo_node',
    )

    districtlogo_image_node = models.OneToOneField(
        Image,
        db_column='districtlogo_image_node',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'images_districtlogo'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogo', 'Can soft delete district logo'),
            ('restore_districtlogo', 'Can restore district logo'),
        )
        verbose_name = 'District Logo'
        verbose_name_plural = 'District Logos'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.district_logo_group.title + \
            ' ' + self.district_logo_style_variation.title

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class PhotoGallery(Image):
    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/photogallery/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )

    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_photogallery_node',
    )

    photogallery_image_node = models.OneToOneField(
        Image,
        db_column='photogallery_image_node',
        on_delete=models.CASCADE,
    )

    inline_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        db_table = 'images_photogallery'
        ordering = ['inline_order', ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_photogallery', 'Can soft delete photo gallery'),
            ('restore_photogallery', 'Can restore photo gallery'),
        )
        verbose_name = 'Photo Gallery'
        verbose_name_plural = 'Photo Galleries'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return '{0}'.format(
                self.title,
            )

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class PhotoGalleryImage(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/photogalleryimage/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    thumbnail = ImageSpecField(
        source='image_file',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={
            'quality': 90,
            'specfield': 'thumbnail',
        },
    )
    isotope = ImageSpecField(
        source='image_file',
        processors=[ResizeToFit(width=320)],
        format='JPEG',
        options={
            'quality': 90,
            'specfield': 'isotope',
        },
    )
    alttext = models.CharField(
        max_length=200,
        verbose_name='Alternative Text',
        help_text='',
    )

    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_photogalleryimage_node',
    )

    photogallery_image_node = models.OneToOneField(
        Image,
        db_column='photogalleryimage_image_node',
        on_delete=models.CASCADE,
    )

    inline_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        db_table = 'images_photogalleryimage'
        ordering = ['inline_order', ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_photogalleryimage', 'Can soft delete photo gallery image'),
            ('restore_photogalleryimage', 'Can restore photo gallery image'),
        )
        verbose_name = 'Photo Gallery Image'
        verbose_name_plural = 'Photo Gallery Images'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return '{0}'.format(
                self.title,
            )

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class InlineImage(Image):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/inlineimage/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=commonfunctions.image_upload_to,
        verbose_name='Image',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='images_inlineimage_node',
        editable=False,
    )

    inlineimage_image_node = models.OneToOneField(
        Image,
        db_column='inlineimage_image_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'images_inlineimage'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_inlineimage', 'Can soft delete inline image'),
            ('restore_inlineimage', 'Can restore inline image'),
        )
        verbose_name = 'Inline Image'
        verbose_name_plural = 'Inline Images'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return str(self.uuid)

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
