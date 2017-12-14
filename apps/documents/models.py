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

  inline_order = models.PositiveIntegerField(default=0,blank=False, null=False,db_index=True)

  class Meta:
    db_table = 'documents_document'
    ordering = ['inline_order',]
    get_latest_by = 'update_date'
    permissions = (('trash_document', 'Can soft delete document'),('restore_document', 'Can restore document'))
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.documentsave
  delete = apps.common.functions.modeltrash

class BoardPolicy(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

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
        default_manager_name = 'objects'

    def get_policy_index(self):
        return '{0}-{1}'.format(self.section.section_prefix, self.index)
    get_policy_index.short_description = 'Policy Index'

    def get_section_prefix(self):
        return '{0}'.format(self.section.section_prefix)

    def __str__(self):
        return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class Policy(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_policy_node', editable=False)

    document_policy_node = models.OneToOneField(BaseDocument, db_column='document_policy_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_policy'
        get_latest_by = 'update_date'
        permissions = (('trash_policy', 'Can soft delete policy'),('restore_policy', 'Can restore policy'))
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class AdministrativeProcedure(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_administrativeprocedure_node', editable=False)

    document_administrativeprocedure_node = models.OneToOneField(BaseDocument, db_column='document_administrativeprocedure_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_administrativeprocedure'
        get_latest_by = 'update_date'
        permissions = (('trash_administrativeprocedure', 'Can soft delete administrative procedure'),('restore_administrativeprocedure', 'Can restore administrative procedure'))
        verbose_name = 'Administrative Procedure'
        verbose_name_plural = 'Administrative Procedures'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class SupportingDocument(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    document_title = models.CharField(max_length=200, help_text='',verbose_name='Title')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_supportingdocument_node', editable=False)

    document_supportingdocument_node = models.OneToOneField(BaseDocument, db_column='document_supportingdocument_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_supportingdocument'
        get_latest_by = 'update_date'
        permissions = (('trash_supportingdocument', 'Can soft delete supporting document'),('restore_supportingdocument', 'Can restore supporting document'))
        verbose_name = 'Supporting Document'
        verbose_name_plural = 'Supporting Documents'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingAgenda(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingagenda_node', editable=False)

    document_boardmeetingagenda_node = models.OneToOneField(BaseDocument, db_column='document_boardmeetingagenda_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingagenda'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingagenda', 'Can soft delete board meeting agenda'),('restore_boardmeetingagenda', 'Can restore board meeting agenda'))
        verbose_name = 'Board Meeting Agenda'
        verbose_name_plural = 'Board Meeting Agendas'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingMinutes(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingminutes_node', editable=False)

    document_boardmeetingminutes_node = models.OneToOneField(BaseDocument, db_column='document_boardmeetingminutes_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingminutes'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingminutes', 'Can soft delete board meeting minutes'),('restore_boardmeetingminutes', 'Can restore board meeting minutes'))
        verbose_name = 'Board Meeting Minutes'
        verbose_name_plural = 'Board Meeting Minutes'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingAudio(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingaudio_node', editable=False)

    boardmeetingaudio_document_node = models.OneToOneField(BaseDocument, db_column='boardmeetingaudio_document_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingaudio'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingaudio', 'Can soft delete board meeting audio'),('restore_boardmeetingaudio', 'Can restore board meeting audio'))
        verbose_name = 'Board Meeting Audio'
        verbose_name_plural = 'Board Meeting Audio'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingVideo(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingvideo_node', editable=False)

    boardmeetingvideo_document_node = models.OneToOneField(BaseDocument, db_column='boardmeetingvideo_document_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingvideo'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingvideo', 'Can soft delete board meeting video'),('restore_boardmeetingvideo', 'Can restore board meeting video'))
        verbose_name = 'Board Meeting Video'
        verbose_name_plural = 'Board Meeting Videos'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingExhibit(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingexhibit_node', editable=False)

    boardmeetingexhibit_document_node = models.OneToOneField(BaseDocument, db_column='boardmeetingexhibit_document_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingexhibit'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingexhibit', 'Can soft delete board meeting exhibit'),('restore_boardmeetingexhibit', 'Can restore board meeting exhibit'))
        verbose_name = 'Board Meeting Exhibit'
        verbose_name_plural = 'Board Meeting Exhibits'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash

class BoardMeetingAgendaItem(BaseDocument):

    PARENT_URL = ''
    URL_PREFIX = ''

    title = models.CharField(max_length=200, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='documents_boardmeetingagendaitem_node', editable=False)

    boardmeetingagendaitem_document_node = models.OneToOneField(BaseDocument, db_column='boardmeetingagendaitem_document_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'documents_boardmeetingagendaitem'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingagendaitem', 'Can soft delete board meeting agenda item'),('restore_boardmeetingagendaitem', 'Can restore board meeting agenda item'))
        verbose_name = 'Board Meeting Agenda Item'
        verbose_name_plural = 'Board Meeting Agenda Items'
        default_manager_name = 'objects'

    def __str__(self):
       return self.title

    save = apps.common.functions.documentsave
    delete = apps.common.functions.modeltrash
