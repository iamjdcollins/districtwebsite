from django.db import models
import apps.common.functions as commonfunctions
from apps.objects.models import Node, File as BaseFile
from apps.taxonomy.models import Language


class File(BaseFile):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    file_file = models.FileField(
        max_length=2000,
        upload_to=commonfunctions.file_upload_to,
        verbose_name='File',
        help_text='',
    )
    file_language = models.ForeignKey(
        Language,
        to_field='language_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='files_file_file_language',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='files_file_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    file_file_node = models.OneToOneField(
        BaseFile,
        db_column='file_file_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'files_file'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_file', 'Can soft delete file'),
            ('restore_file', 'Can restore file'),
        )
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.file_language.title

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class AudioFile(BaseFile):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    file_file = models.FileField(
        max_length=2000,
        upload_to=commonfunctions.file_upload_to,
        verbose_name='File',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='files_audiofile_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    audiofile_file_node = models.OneToOneField(
        BaseFile,
        db_column='audiofile_file_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'files_audiofile'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_audiofile', 'Can soft delete audio file'),
            ('restore_audiofile', 'Can restore audio file'),
        )
        verbose_name = 'Audio File'
        verbose_name_plural = 'Audio Files'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self._meta.model_name

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class VideoFile(BaseFile):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    file_file = models.FileField(
        max_length=2000,
        upload_to=commonfunctions.file_upload_to,
        verbose_name='File',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='files_videofile_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    videofile_file_node = models.OneToOneField(
        BaseFile,
        db_column='videofile_file_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'files_videofile'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_videofile', 'Can soft delete video file'),
            ('restore_videofile', 'Can restore video file'),
        )
        verbose_name = 'Video File'
        verbose_name_plural = 'Video Files'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self._meta.model_name

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class PrecinctMap(BaseFile):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    file_file = models.FileField(
        max_length=2000,
        upload_to=commonfunctions.file_upload_to,
        verbose_name='File',
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='files_precinctmap_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    file_file_node = models.OneToOneField(
        BaseFile,
        db_column='precinctmap_file_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'files_precinctmap'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_precinctmap', 'Can soft delete precinct map'),
            ('restore_file', 'Can restore precinct map'),
        )
        verbose_name = 'Precinct Map'
        verbose_name_plural = 'Precinct Maps'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.parent.node_title + ' Map'

    file_name = commonfunctions.file_name
    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
