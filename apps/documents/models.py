import re
from django.db import models
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Document as BaseDocument
from apps.taxonomy.models import BoardPolicySection
from apps.dashboard.models import PageLayout


class Document(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/documents/'
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(namespace='document.html', defaults={'title': 'Document'})[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_document_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_document_node = models.OneToOneField(
        BaseDocument,
        db_column='document_document_node',
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
        db_table = 'documents_document'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_document', 'Can soft delete document'),
            ('restore_document', 'Can restore document'),
        )
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DisclosureDocument(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/disclosure-document/'
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(namespace='disclosure-document.html',
                                         defaults={'title': 'Disclosure Document'})[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
        verbose_name='Class Name',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_disclosuredocument_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    disclosuredocument_document_node = models.OneToOneField(
        BaseDocument,
        db_column='disclosuredocument_document_node',
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
        db_table = 'documents_disclosuredocument'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_document', 'Can soft delete Disclosure Document'),
            ('restore_document', 'Can restore Disclosure Document'),
        )
        verbose_name = 'Disclosure Document'
        verbose_name_plural = 'Disclosure Documents'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    def has_files(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def modal_ajax(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def target_blank(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return False
        return True

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardPolicy(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    policy_title = models.CharField(
        max_length=150,
        unique=True,
        help_text='',
        verbose_name="Policy Title",
    )
    section = models.ForeignKey(
        BoardPolicySection,
        on_delete=models.PROTECT,
        related_name='documents_boardpolicy_section',
    )
    index = models.IntegerField(
        verbose_name='Policy Section Number',
    )
    subcommittee_review = models.DateField(
        null=True,
        blank=True,
        verbose_name='Subcommitte Meeting Review',
    )
    boardmeeting_review = models.DateField(
        null=True,
        blank=True,
        verbose_name='Anticipated Board Meeting Review',
    )
    last_approved = models.DateField(
        null=True,
        blank=True,
        verbose_name='Last Approved',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardpolicy_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_boardpolicy_node = models.OneToOneField(
        BaseDocument,
        db_column='document_boardpolicy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardpolicy'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardpolicy', 'Can soft delete board policy'),
            ('restore_boardpolicy', 'Can restore board policy'),
        )
        verbose_name = 'Board Policy'
        verbose_name_plural = 'Board Policies'
        default_manager_name = 'base_manager'

    def get_policy_index(self):
        return '{0}-{1}'.format(self.section.section_prefix, self.index)
    get_policy_index.short_description = 'Policy Index'

    def get_section_prefix(self):
        return '{0}'.format(self.section.section_prefix)

    def __str__(self):
        return self.title

    def force_title(self):
        return self.section.section_prefix + '-' + str(self.index)

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Policy(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_policy_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_policy_node = models.OneToOneField(
        BaseDocument,
        db_column='document_policy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_policy'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_policy', 'Can soft delete policy'),
            ('restore_policy', 'Can restore policy'),
        )
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.parent.node_title + ' Policy'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class AdministrativeProcedure(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_administrativeprocedure_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_administrativeprocedure_node = models.OneToOneField(
        BaseDocument,
        db_column='document_administrativeprocedure_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_administrativeprocedure'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_administrativeprocedure',
                'Can soft delete administrative procedure'),
            ('restore_administrativeprocedure',
                'Can restore administrative procedure'),
        )
        verbose_name = 'Administrative Procedure'
        verbose_name_plural = 'Administrative Procedures'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.parent.node_title + ' AP'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SupportingDocument(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    document_title = models.CharField(
        max_length=200,
        help_text='',
        verbose_name='Title',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_supportingdocument_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_supportingdocument_node = models.OneToOneField(
        BaseDocument,
        db_column='document_supportingdocument_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_supportingdocument'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_supportingdocument',
                'Can soft delete supporting document'),
            ('restore_supportingdocument',
                'Can restore supporting document'),
        )
        verbose_name = 'Supporting Document'
        verbose_name_plural = 'Supporting Documents'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        if ((not self.document_title) and self.title) \
                or self.title != self.node_title:
            self.document_title = \
                re.sub(r'^' + re.escape(
                    self.parent.node_title
                ) + '[ ]?', '', self.title).strip()
        return self.parent.node_title + ' ' + self.document_title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingAgenda(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingagenda_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_boardmeetingagenda_node = models.OneToOneField(
        BaseDocument,
        db_column='document_boardmeetingagenda_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingagenda'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingagenda',
                'Can soft delete board meeting agenda'),
            ('restore_boardmeetingagenda',
                'Can restore board meeting agenda'),
        )
        verbose_name = 'Board Meeting Agenda'
        verbose_name_plural = 'Board Meeting Agendas'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Agenda'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingMinutes(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingminutes_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    document_boardmeetingminutes_node = models.OneToOneField(
        BaseDocument,
        db_column='document_boardmeetingminutes_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingminutes'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingminutes',
                'Can soft delete board meeting minutes'),
            ('restore_boardmeetingminutes',
                'Can restore board meeting minutes'),
        )
        verbose_name = 'Board Meeting Minutes'
        verbose_name_plural = 'Board Meeting Minutes'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Minutes'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingAudio(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingaudio_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardmeetingaudio_document_node = models.OneToOneField(
        BaseDocument,
        db_column='boardmeetingaudio_document_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingaudio'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingaudio', 'Can soft delete board meeting audio'),
            ('restore_boardmeetingaudio', 'Can restore board meeting audio'),
        )
        verbose_name = 'Board Meeting Audio'
        verbose_name_plural = 'Board Meeting Audio'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Audio'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingVideo(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingvideo_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardmeetingvideo_document_node = models.OneToOneField(
        BaseDocument,
        db_column='boardmeetingvideo_document_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingvideo'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingvideo', 'Can soft delete board meeting video'),
            ('restore_boardmeetingvideo', 'Can restore board meeting video'),
        )
        verbose_name = 'Board Meeting Video'
        verbose_name_plural = 'Board Meeting Videos'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Video'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingExhibit(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingexhibit_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardmeetingexhibit_document_node = models.OneToOneField(
        BaseDocument,
        db_column='boardmeetingexhibit_document_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingexhibit'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingexhibit',
                'Can soft delete board meeting exhibit'),
            ('restore_boardmeetingexhibit',
                'Can restore board meeting exhibit'),
        )
        verbose_name = 'Board Meeting Exhibit'
        verbose_name_plural = 'Board Meeting Exhibits'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingAgendaItem(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_boardmeetingagendaitem_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardmeetingagendaitem_document_node = models.OneToOneField(
        BaseDocument,
        db_column='boardmeetingagendaitem_document_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'documents_boardmeetingagendaitem'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingagendaitem',
                'Can soft delete board meeting agenda item'),
            ('restore_boardmeetingagendaitem',
                'Can restore board meeting agenda item'),
        )
        verbose_name = 'Board Meeting Agenda Item'
        verbose_name_plural = 'Board Meeting Agenda Items'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolCommunityCouncilMeetingAgenda(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/scc-agenda/'
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(
            namespace='school-community-council-meeting-agenda.html',
            defaults={'title': 'School Community Council Meeting Agenda'},
        )[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
        verbose_name='Title',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_schoolcommunitycouncilmeetingagenda_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schoolcommunitycouncilmeetingagenda_document_node = models.OneToOneField(
        BaseDocument,
        db_column='sccagenda_schoolcommunitycouncilmeetingagenda_node',
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
        db_table = 'documents_schoolcommunitycouncilmeetingagenda'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            (
                'trash_schoolcommunitycouncilmeetingagenda',
                'Can soft delete scc agenda'
            ),
            (
                'restore_schoolcommunitycouncilmeetingagenda',
                'Can restore scc agenda'
            ),
        )
        verbose_name = 'School Community Council Meeting Agenda'
        verbose_name_plural = 'School Community Council Meeting Agendas'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    def has_files(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def modal_ajax(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def target_blank(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return False
        return True

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolCommunityCouncilMeetingMinutes(BaseDocument):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/scc-minutes/'
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(
            namespace='school-community-council-meeting-minutes.html',
            defaults={'title': 'School Community Council Meeting Minutes'},
        )[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
        verbose_name='Title',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='documents_schoolcommunitycouncilmeetingminutes_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schoolcommunitycouncilmeetingminutes_document_node = models.OneToOneField(
        BaseDocument,
        db_column='sccMinutes_schoolcommunitycouncilmeetingminutes_node',
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
        db_table = 'documents_schoolcommunitycouncilmeetingminutes'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            (
                'trash_schoolcommunitycouncilmeetingminutes',
                'Can soft delete scc minutes'
            ),
            (
                'restore_schoolcommunitycouncilmeetingminutes',
                'Can restore scc minutes'
            ),
        )
        verbose_name = 'School Community Council Meeting Minutes'
        verbose_name_plural = 'School Community Council Meeting Minutes'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    def has_files(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def modal_ajax(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return True
        return False

    def target_blank(self):
        doc_len = self.files_file_node.filter(published=1, deleted=0).count()
        if doc_len > 1:
            return False
        return True

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
