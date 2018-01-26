from django.db import models
import apps.common.functions
from apps.objects.models import Node, Image
from apps.taxonomy.models import DistrictLogoGroup, DistrictLogoStyleVariation


class Thumbnail(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/thumbnails/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class NewsThumbnail(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/newsthumbnails/'

    title = models.CharField(
        max_length=200,
        help_text='',)
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class PageBanner(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/pagebanners/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class ContentBanner(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/contentbanners/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class ProfilePicture(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/profilepictures/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class DistrictLogoGIF(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/districtlogosgifs/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class DistrictLogoJPG(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/districtlogosjpgs/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class DistrictLogoPNG(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/districtlogospngs/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class DistrictLogoTIF(Image):

    PARENT_URL = ''
    URL_PREFIX = '/images/districtlogostifs/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    image_file = models.ImageField(
        max_length=2000,
        upload_to=apps.common.functions.image_upload_to,
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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash


class DistrictLogo(Image):

    PARENT_URL = ''
    URL_PREFIX = ''

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

    save = apps.common.functions.imagesave
    delete = apps.common.functions.modeltrash
