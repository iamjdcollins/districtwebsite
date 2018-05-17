import uuid
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from multisite.models import Alias
from ckeditor.fields import RichTextField
import apps.dashboard.help as apphelp


class PageLayout(models.Model):

    uuid = models.UUIDField(
      primary_key=True,
      unique=True,
      default=uuid.uuid4,
      editable=False,
    )
    title = models.CharField(
        max_length=200,
        help_text=apphelp.PageLayout.title,
        unique=True,
        verbose_name='Page Layouts',
    )
    namespace = models.CharField(
        max_length=200,
        help_text=apphelp.PageLayout.namespace,
        unique=True,
        verbose_name='HTML File Name'
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_pagelayout_create_user',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_pagelayout_update_user',
    )

    class Meta:
        db_table = 'dashboard_pagelayout'
        get_latest_by = 'update_date'
        verbose_name = 'Page Layout'
        verbose_name_plural = 'Page Layouts'

    def __str__(self):
        return self.title


class Template(models.Model):

    uuid = models.UUIDField(
      primary_key=True,
      unique=True,
      default=uuid.uuid4,
      editable=False,
    )
    title = models.CharField(
        max_length=200,
        help_text=apphelp.Templates.title,
        verbose_name='Template Name',
    )
    namespace = models.CharField(
        max_length=200,
        help_text=apphelp.Templates.namespace,
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_template_create_user',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_template_update_user',
    )

    class Meta:
        db_table = 'dashboard_templates'
        get_latest_by = 'update_date'
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return self.title


class GeneralSettings(models.Model):

    uuid = models.UUIDField(
      primary_key=True,
      unique=True,
      default=uuid.uuid4,
      editable=False,
    )
    title = models.CharField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name='Site Title',
        help_text=apphelp.GeneralSettings.title,
    )
    primary_domain = models.CharField(
        max_length=100,
        null=True,
        blank=False,
        help_text=apphelp.GeneralSettings.primary_domain,
    )
    namespace = models.CharField(
        max_length=64,
        null=True,
        blank=False,
        help_text=apphelp.GeneralSettings.namespace,
    )
    gatrackingid = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=apphelp.GeneralSettings.gatrackingid,
        verbose_name='Google Analytics Tracking ID',
    )
    nd_statement = RichTextField(
        null=True,
        blank=False,
        verbose_name='Non-Discrimination Statement',
        help_text=apphelp.GeneralSettings.nd_statement,
    )
    ada_statement = RichTextField(
        null=True,
        blank=False,
        verbose_name='Americans with Disabilities Act (ADA) Statement',
        help_text=apphelp.GeneralSettings.ada_statement,
    )
    template = models.ForeignKey(
        'Template',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        related_name='dashboard_general_template',
        verbose_name='Template',
        help_text=apphelp.GeneralSettings.template,
    )
    site = models.OneToOneField(
        Site,
        null=False,
        blank=False,
        editable=False,
        unique=True,
        on_delete=models.PROTECT,
        related_name='dashboard_general_site',
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_general_create_user',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='dashboard_general_update_user',
    )

    class Meta:
        db_table = 'dashboard_generalsettings'
        get_latest_by = 'update_date'
        verbose_name = 'General Settings'
        verbose_name_plural = 'General Settings'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            self.site
        except ObjectDoesNotExist:
            site, created = Site.objects.get_or_create(
                domain=self.primary_domain,
                defaults={
                    'name': self.title[:50]
                },
            )
            site.save()
            alias, created = Alias.objects.get_or_create(
                domain='{0}-test.{1}'.format(
                    site.domain.split('.')[0],
                    '.'.join(site.domain.split('.')[1:]),
                ),
                is_canonical=None,
                redirect_to_canonical=False,
                site=site,
            )
            alias.save()
            alias, created = Alias.objects.get_or_create(
                domain='{0}-dev.{1}'.format(
                    site.domain.split('.')[0],
                    '.'.join(site.domain.split('.')[1:]),
                ),
                is_canonical=None,
                redirect_to_canonical=False,
                site=site,
            )
            alias.save()
            alias, created = Alias.objects.get_or_create(
                domain='{0}-new.{1}'.format(
                    site.domain.split('.')[0],
                    '.'.join(site.domain.split('.')[1:]),
                ),
                is_canonical=None,
                redirect_to_canonical=False,
                site=site,
            )
            alias.save()
            self.site = site
        # Site name is limited to 50 characters.
        if self.title and self.title[:50] != self.site.name:
            self.site.name = self.title[:50]
            self.site.save()
        if self.primary_domain and self.primary_domain != self.site.domain:
            self.site.domain = self.primary_domain
            self.site.save()
        if self.primary_domain == 'websites.slcschools.org':
            for item in GeneralSettings.objects.exclude(pk=self.pk):
                item.nd_statement = self.nd_statement
                item.ada_statement = self.ada_statement
                item.save()
        else:
            try:
                websites = GeneralSettings.objects.get(primary_domain='websites.slcschools.org')
            except GeneralSettings.DoesNotExist:
                websites = False
            if websites:
                self.nd_statement = websites.nd_statement
                self.ada_statement = websites.ada_statement
        super().save(*args, **kwargs)
