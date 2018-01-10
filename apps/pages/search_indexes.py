from haystack import indexes
from .models import Page, School, Department, SubPage

class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class SchoolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return School

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class DepartmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Department

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)

class SubPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SubPage

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=0).filter(published=1).filter(searchable=1)
