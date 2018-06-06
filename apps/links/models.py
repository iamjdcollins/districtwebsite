from django.db import models
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Link


class ResourceLink(Link):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/resourcelinks/'
    HAS_PERMISSIONS = False

    title = models.CharField(max_length=200, help_text='')
    link_url = models.CharField(max_length=2000, db_index=True)
    related_locked = models.BooleanField(
        default=False,
        db_index=True,
    )

    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='links_resourcelink_node',
        editable=False,
    )

    resourcelink_link_node = models.OneToOneField(
        Link,
        db_column='resourcelink_link_node',
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
        db_table = 'links_resourcelink'
        ordering = ['inline_order', ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_resourcelink', 'Can soft delete resource link'),
            ('restore_resourcelink', 'Can restore resource link'),
        )
        verbose_name = 'Resource Link'
        verbose_name_plural = 'Resource Links'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class ActionButton(Link):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/actionbuttons/'
    HAS_PERMISSIONS = False

    title = models.CharField(max_length=200, help_text='')
    link_url = models.CharField(max_length=2000, db_index=True)
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='links_actionbutton_node',
        editable=False,
    )

    actionbutton_link_node = models.OneToOneField(
        Link,
        db_column='actionbutton_link_node',
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
        db_table = 'links_actionbutton'
        ordering = ['inline_order', ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_actionbutton', 'Can soft delete action button'),
            ('restore_resourcelink', 'Can restore action button'),
        )
        verbose_name = 'Action Button'
        verbose_name_plural = 'Action Buttons'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
