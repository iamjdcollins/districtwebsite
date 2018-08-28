from django.template import loader
from haystack import indexes
import textract
from ast import literal_eval
from .models import Policy, AdministrativeProcedure, SupportingDocument, BoardMeetingMinutes, BoardMeetingAgenda

class PolicyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    site = indexes.CharField(model_attr='site__domain')
    url = indexes.CharField(model_attr='url',boost=1.125)
    node_type = indexes.CharField(model_attr='node_type',boost=1.125)
    content_type = indexes.CharField(model_attr='content_type',boost=1.125)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return Policy

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

    def prepare(self, obj):
        data = super(PolicyIndex, self).prepare(obj)
        extracted = ''
        for file in obj.files_file_node.filter(deleted=0).filter(published=1):
            try:
                extracted += textract.process(file.file_file.path).decode('utf-8')
            except:
                pass
        t = loader.select_template(('search/indexes/documents/policy_text.txt',))
        data['text'] = t.render({'object': obj, 'extracted': extracted})
        return data

class AdministrativeProcedureIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    site = indexes.CharField(model_attr='site__domain')
    url = indexes.CharField(model_attr='url',boost=1.125)
    node_type = indexes.CharField(model_attr='node_type',boost=1.125)
    content_type = indexes.CharField(model_attr='content_type',boost=1.125)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return AdministrativeProcedure

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

    def prepare(self, obj):
        data = super(AdministrativeProcedureIndex, self).prepare(obj)
        extracted = ''
        for file in obj.files_file_node.filter(deleted=0).filter(published=1):
            try:
                extracted += textract.process(file.file_file.path).decode('utf-8')
            except:
                pass
        t = loader.select_template(('search/indexes/documents/administrativeprocedure_text.txt',))
        data['text'] = t.render({'object': obj, 'extracted': extracted})
        return data

class SupportingDocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    site = indexes.CharField(model_attr='site__domain')
    url = indexes.CharField(model_attr='url',boost=1.125)
    node_type = indexes.CharField(model_attr='node_type',boost=1.125)
    content_type = indexes.CharField(model_attr='content_type',boost=1.125)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return SupportingDocument

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

    def prepare(self, obj):
        data = super(SupportingDocumentIndex, self).prepare(obj)
        extracted = ''
        for file in obj.files_file_node.filter(deleted=0).filter(published=1):
            try:
                extracted += textract.process(file.file_file.path).decode('utf-8')
            except:
                pass
        t = loader.select_template(('search/indexes/documents/supportingdocument_text.txt',))
        data['text'] = t.render({'object': obj, 'extracted': extracted})
        return data

class BoardMeetingMinutesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    site = indexes.CharField(model_attr='site__domain')
    url = indexes.CharField(model_attr='url',boost=1.125)
    node_type = indexes.CharField(model_attr='node_type',boost=1.125)
    content_type = indexes.CharField(model_attr='content_type',boost=1.125)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return BoardMeetingMinutes

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

    def prepare(self, obj):
        data = super(BoardMeetingMinutesIndex, self).prepare(obj)
        extracted = ''
        for file in obj.files_file_node.filter(deleted=0).filter(published=1):
            try:
                extracted += textract.process(file.file_file.path).decode('utf-8')
            except:
                pass
        t = loader.select_template(('search/indexes/documents/boardmeetingminutes_text.txt',))
        data['text'] = t.render({'object': obj, 'extracted': extracted})
        return data

class BoardMeetingAgendaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    site = indexes.CharField(model_attr='site__domain')
    url = indexes.CharField(model_attr='url',boost=1.125)
    node_type = indexes.CharField(model_attr='node_type',boost=1.125)
    content_type = indexes.CharField(model_attr='content_type',boost=1.125)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return BoardMeetingAgenda

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

    def prepare(self, obj):
        data = super(BoardMeetingAgendaIndex, self).prepare(obj)
        extracted = ''
        for file in obj.files_file_node.filter(deleted=0).filter(published=1):
            try:
                extracted += textract.process(file.file_file.path).decode('utf-8')
            except:
                pass
        t = loader.select_template(('search/indexes/documents/boardmeetingagenda_text.txt',))
        data['text'] = t.render({'object': obj, 'extracted': extracted})
        return data
