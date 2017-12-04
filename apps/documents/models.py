from django.db import models
import apps.common.functions
from apps.objects.models import Node, Document as BaseDocument
from apps.taxonomy.models import BoardPolicySection

class Document(BaseDocument):

  PARENT_URL = ''
  URL_PREFIX = '/documents/document/'

  title = models.CharField(max_length=200, help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_document_node', editable=False)

  document_document_node = models.OneToOneField(BaseDocument, db_column='document_document_node', on_delete=models.CASCADE, parent_link=True, editable=False)

  class Meta:
    db_table = 'documents_document'
    get_latest_by = 'update_date'
    permissions = (('trash_document', 'Can soft delete document'),('restore_document', 'Can restore document'))
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'

  def __str__(self):
    return self.title

  save = apps.common.functions.documentsave
  delete = apps.common.functions.modeltrash

class BoardPolicy(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = '/documents/boardpolicy/'

    title = models.CharField(max_length=200, help_text='')
    policy_title = models.CharField(max_length=150, unique=True, help_text='',verbose_name="Policy Title")
    section = models.ForeignKey(BoardPolicySection, on_delete=models.PROTECT, related_name='documents_boardpolicy_section')
    index = models.IntegerField(verbose_name='Policy Section Number')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardpolicy_node', editable=False)

    document_boardpolicy_node = models.OneToOneField(BaseDocument, db_column='document_boardpolicy_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardpolicy'
        get_latest_by = 'update_date'
        permissions = (('trash_boardpolicy', 'Can soft delete board policy'),('restore_boardpolicy', 'Can restore board policy'))
        verbose_name = 'Board Policy'
        verbose_name_plural = 'Board Policies'

    def get_policy_index(self):
        return '{0}-{1}'.format(self.section.section_prefix, self.index)
    get_policy_index.short_description = 'Policy Index'

    def get_section_prefix(self):
        return '{0}'.format(self.section.section_prefix)

    def __str__(self):
        return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash
