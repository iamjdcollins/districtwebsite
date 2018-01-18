from haystack import indexes
from .models import Page, School, Department, SubPage, Board, BoardSubPage

class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class SchoolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return School

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class DepartmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return Department

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class SubPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return SubPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class BoardIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return Board

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class BoardSubPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    render_top = indexes.CharField(use_template=True)
    render_bottom = indexes.CharField(use_template=True)

    def get_model(self):
        return BoardSubPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)
