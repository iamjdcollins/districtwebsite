import json
from django.contrib import admin
from haystack.utils.highlighting import Highlighter
from haystack.forms import SearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from haystack.query import SQ
from haystack.inputs import AutoQuery
from ajax_select.lookup_channel import LookupChannel
import uuid
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateResponseMixin
from django import forms
#Delete View
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import get_deleted_objects, unquote
from django.db import models, router, transaction
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import (
    override as translation_override, string_concat, ugettext as _, ungettext,
)
from django.contrib.auth import get_permission_codename
TO_FIELD_VAR = '_to_field'
IS_POPUP_VAR = '_popup'
from guardian.shortcuts import get_perms
from imagekit.cachefiles.backends import CachedFileBackend
import apps.common.functions as commonfunctions
from mptt.admin import DraggableMPTTAdmin, JS
from django.core.serializers.json import DjangoJSONEncoder


class DeletedListFilter(admin.SimpleListFilter):
    title = 'deleted'
    parameter_name = 'deleted'


    def lookups(self, request, model_admin):
        return (('1','Yes'),('0','No'))

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(deleted=1)
        elif self.value() == '0':
            return queryset.filter(deleted=0)
        elif self.value() == None:
            return queryset.filter(deleted=0)

class UUIDLookupChannel(LookupChannel):
  def get_objects(self, ids):
        """
        This is used to retrieve the currently selected objects for either ManyToMany or ForeignKey.

        Args:
            ids (list): list of primary keys
        Returns:
            list: list of Model objects
        """
        if self.model._meta.pk.rel is not None:
            # Use the type of the field being referenced
            pk_type = self.model._meta.pk.target_field.to_python
        else:
            pk_type = self.model._meta.pk.to_python

        # Return objects in the same order as passed in here
        ids = [pk_type(pk) for pk in ids]
        # uuid_to_id = []
        # for id in ids:
        #   if int(id).bit_length() > 63:
        #     user = self.model.objects.get(uuid=uuid.UUID(id))
        #     uuid_to_id.append(str(user.uuid))
        #   else:
        #     uuid_to_id.append(id)
        # ids = uuid_to_id
        idcount = 0
        for id in ids:
            ids[idcount] = str(id)
            idcount += 1
        things = self.model.objects.in_bulk(ids)
        for thing in things:
          things[str(thing)] = things.pop(thing)
        return [things[aid] for aid in ids if aid in things]

class ModelAdminOverwrite():
  def delete_view(self, request, object_id, extra_context=None):
    "The 'delete' admin view for this model."
    opts = self.model._meta
    app_label = opts.app_label

    to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
    if to_field and not self.to_field_allowed(request, to_field):
      raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)
    obj = self.get_object(request, unquote(object_id), to_field)

    if not self.has_delete_permission(request, obj):
      raise PermissionDenied

    if obj is None:
      raise Http404(
      _('%(name)s object with primary key %(key)r does not exist.') %
      {'name': force_text(opts.verbose_name), 'key': escape(object_id)}
    )

    using = router.db_for_write(self.model)

    # Populate deleted_objects, a data structure of all related objects that
    # will also be deleted.
    (deleted_objects, model_count, perms_needed, protected) = get_deleted_objects(
        [obj], opts, request.user, self.admin_site, using)

    #Redo Perms Needed
    if obj.deleted == False:
      perms_needed = set()

      for obj in [obj]:
        add = True
        opts = obj._meta
        p = '%s.%s' % (opts.app_label,
                       get_permission_codename('trash', opts))
        p_short = '%s' % (get_permission_codename('trash', opts))
        if request.user.has_perm(p):
          add = False
        if p_short in get_perms(request.user,obj):
          add = False
        if add == True:
          perms_needed.add(opts.verbose_name)

    if request.POST and not protected:  # The user has confirmed the deletion.
      if perms_needed:
        raise PermissionDenied
      obj_display = force_text(obj)
      attr = str(to_field) if to_field else opts.pk.attname
      obj_id = obj.serializable_value(attr)
      self.log_deletion(request, obj, obj_display)
      self.delete_model(request, obj)
      return self.response_delete(request, obj_display, obj_id)

    object_name = force_text(opts.verbose_name)

    if perms_needed or protected:
      title = _("Cannot delete %(name)s") % {"name": object_name}
    else:
      title = _("Are you sure?")

    context = dict(
      self.admin_site.each_context(request),
      title=title,
      object_name=object_name,
      object=obj,
      deleted_objects=deleted_objects,
      model_count=dict(model_count).items(),
      perms_lacking=perms_needed,
      protected=protected,
      opts=opts,
      app_label=app_label,
      preserved_filters=self.get_preserved_filters(request),
      is_popup=(IS_POPUP_VAR in request.POST or
                IS_POPUP_VAR in request.GET),
      to_field=to_field,
    )
    context.update(extra_context or {})

    return self.render_delete_form(request, context)


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a class="editlink" href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class LinkToInlineObject(object):

    def copy_link(self, instance):
        if instance.pk:
            return mark_safe(u'<span class="linkto md-linkvariant" data-clipboard-text="https://{s}{u}" data-href="{u}"></span>'.format(s=instance.site.domain, u=instance.url))
        else:
            return ''


class CustomSearchForm(SearchForm):

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        q = self.cleaned_data['q']
        sqs = SearchQuerySet().filter(SQ(content=AutoQuery(q)) | SQ(url=AutoQuery(q)) | SQ(node_type=AutoQuery(q)) | SQ(content_type=AutoQuery(q)))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class CustomSearchView(SearchView, TemplateResponseMixin):

    form_class=CustomSearchForm

    def get_template_names(self):
        template_name='cmstemplates/{0}/pagelayouts/search-results.html'.format(
            self.request.site.dashboard_general_site.template.namespace
        )
        return [template_name]


class Simple(CachedFileBackend):
    """
    The most basic file backend. The storage is consulted to see if the file
    exists. Files are generated synchronously.

    """

    def generate(self, file, force=False):
        exists = self.exists(file)
        sourceexists = file.generator.source.storage.exists(
            file.generator.source.name
        )
        if not sourceexists:
            return
        if not exists:
            self.generate_now(file, force=True)
        else:
            self.generate_now(file, force=force)

    def _exists(self, file):
        return bool(file.storage.exists(file.name))

    exists = _exists


class JustInTime(object):
    """
    A strategy that ensures the file exists right before it's needed.

    """

    def on_existence_required(self, file):
        file.generate()

    def on_content_required(self, file):
        file.generate()

    def on_source_saved(self, file):
        commonfunctions.silentdelete_media(file.path)
        file.generate(force=True)


class MyDraggableMPTTAdmin(DraggableMPTTAdmin):

    def changelist_view(self, request, *args, **kwargs):
        if request.is_ajax() and request.POST.get('cmd') == 'move_node':
            return self._move_node(request)

        response = super(DraggableMPTTAdmin, self).changelist_view(
            request, *args, **kwargs)

        try:
            response.context_data['media'].add_css({'all': (
                'mptt/draggable-admin.css',
            )})
            response.context_data['media'].add_js((
                JS('mptt/draggable-admin.js', {
                    'id': 'draggable-admin-context',
                    'data-context': json.dumps(
                        self._tree_context(request), cls=DjangoJSONEncoder
                    ),

                }),
            ),)
        except (AttributeError, KeyError):
            # Not meant for us if there is no context_data attribute (no
            # TemplateResponse) or no media in the context.
            pass

        return response

