from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.objects.models import Node, User
from apps.common.functions import nodefindobject
from apps.images.forms import InlineImageForm
from apps.images.models import InlineImage
from django.shortcuts import redirect
from django.contrib import messages
import uuid

def add_inlineimageadd_form(self, context):
    if self.request.POST:
        context['inlineimageaddform'] = InlineImageForm(
            data=self.request.POST,
            files=self.request.FILES,
        )
    else:
        context['inlineimageaddform'] = InlineImageForm()
    return context


class SAMLLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/?next=/'


class BaseURL(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'medialibrary/browser.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['inlineimageaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            copyfiles = context['inlineimageaddform'].files.getlist('image_file')[:]
            count = 0
            for item in copyfiles:
                post = InlineImage.objects.create(
                    image_file=item,
                    pk=uuid.uuid4(),
                    site=self.request.site,
                    create_user=user,
                    update_user=user,
                    parent=context['object'],
                )
                post.save()
                count += 1
        else:
            raise Exception(context['inlineimageaddform'].errors)
        messages.success(
                    request,
                    '{0} Image(s) Added Successfully'.format(count))
        return redirect(self.request.get_full_path())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        errormsg = (
            'Oops, Something went wrong when determining the page the '
            'inline images should belong to. Are you working on an new '
            'page that has not yet been saved? If so populate the required '
            'fields for the page and click "Save and continue editing" then '
            'try again. If you are still have problems contact your '
            'administrator.'
        )
        if self.request.GET.get('pk') == 'false':
            context['showerror'] = errormsg
            return context
        else:
            context['node'] = self.request.GET.get('pk')
        try:
            node = Node.objects.get(pk=context['node'])
        except Node.DoesNotExist:
            node = False
            context['showerror'] = errormsg
            return context
        if node:
            context['object'] = nodefindobject(node)
        context = add_inlineimageadd_form(self, context)
        return context
