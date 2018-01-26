from django.db import models
from ckeditor.fields import RichTextField
import apps.common.functions
from apps.objects.models import Node, FAQ as BaseFAQ


class FAQ(BaseFAQ):

    PARENT_URL = ''
    URL_PREFIX = '/faqs/'

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    question = models.CharField(
        max_length=2000,
        help_text='',
    )
    answer = RichTextField(
        null=True,
        blank=True,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='faqs_faq_node',
        editable=False,
    )

    faq_faq_node = models.OneToOneField(
        BaseFAQ,
        db_column='faq_faq_node',
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
        db_table = 'faqs_faq'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_faq', 'Can soft delete faq'),
            ('restore_faq', 'Can restore faq'),
        )
        verbose_name = 'Fequently Asked Question'
        verbose_name_plural = 'Frequently Asked Questions'
        default_manager_name = 'objects'

    def __str__(self):
        return self.question

    save = apps.common.functions.faqsave
    delete = apps.common.functions.modeltrash
