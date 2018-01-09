from django.db import models
import apps.common.functions
from apps.objects.models import Node, ContactMessage as BaseContactMessage

class ContactMessage(BaseContactMessage):

    PARENT_URL = ''
    URL_PREFIX = '/contact-message/'

    title = models.CharField(max_length=200, help_text='')
    your_name = models.CharField(max_length=200, help_text='')
    your_email = models.EmailField(max_length=254, help_text='')
    message_subject = models.CharField(max_length=400, help_text='')
    your_message = models.TextField(max_length=2000, help_text='')
    message_sent = models.BooleanField(default=False,db_index=True)
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='contactmessages_contactmessage_node', editable=False)

    contactmessage_contactmessage_node = models.OneToOneField(BaseContactMessage, db_column='contactmessage_contactmessage_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    inline_order = models.PositiveIntegerField(default=0,blank=False, null=False,db_index=True)

    class Meta:
        db_table = 'contactmessages_contactmessage'
        ordering = ['inline_order',]
        get_latest_by = 'update_date'
        permissions = (('trash_contactmessage', 'Can soft delete contact message'),('restore_contactmessage', 'Can restore contact message'))
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Message'
        default_manager_name = 'objects'

    def __str__(self):
       return self.message_subject

    save = apps.common.functions.contactmessagesave
    delete = apps.common.functions.modeltrash
