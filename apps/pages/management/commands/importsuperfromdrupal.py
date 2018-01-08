from django.core.management.base import BaseCommand, CommandError
import urllib.request
import json
import pytz
import datetime
from django.utils import timezone
import html
import uuid
from time import sleep
from apps.pages.models import SuperintendentMessage
from apps.images.models import NewsThumbnail, ContentBanner
from apps.objects.models import User
import apps.common.functions

class Command(BaseCommand):
  host = 'https://www1.slcschools.org'
  req = urllib.request.Request(host + '/rest/supermessages')
  resp = urllib.request.urlopen(req,timeout=600)
  supermessagejson = resp.read().decode('utf8')
  supermessage = json.loads(supermessagejson)
  webmaster = User.objects.get(username='webmaster@slcschools.org')
  for article in supermessage:
    sleep(2)
    article_uuid = uuid.UUID(article['uuid'])
    body = article['body']
    summary = article['body_1']
    author_date = timezone.datetime(int(article['created_1']),int(article['created_2']), int(article['created_3']), hour=int(article['created_4']), minute=int(article['created_5']), tzinfo=timezone.utc)
    message, created = SuperintendentMessage.objects.get_or_create(uuid=article_uuid, defaults={'author_date':author_date,'deleted':0,'create_user':webmaster,'update_user':webmaster,'published':1,'url':'/tempnewsurl'})
    message.body=body
    message.summary=summary
    message.author_date=author_date
    message.deleted=False
    message.create_user=webmaster
    message.update_user=webmaster
    message.published=True
    message.save()
    print(message)
    if article['field_article_image'] != '':
      newsthumbimage, created = NewsThumbnail.objects.get_or_create(uuid=uuid.uuid5(message.uuid, article['field_article_image']), defaults={'related_node':message.page_node,'title':message.title + ' Thumbnail','deleted':0,'create_user':webmaster,'update_user':webmaster, 'published':1,'url':'/tempnewsthumburl','parent':message.page_node})
      newsthumbimage.related_node = message.page_node
      newsthumbimage.title = message.title + ' Thumbnail'
      newsthumbimage.deleted = 0
      newsthumbimage.create_user = webmaster
      newsthumbimage.update_user = webmaster
      newsthumbimage.published = 1
      newsthumbimage.parent = message.page_node
      newsthumbimage.alttext=article['field_article_image_2']
      thumbreq = urllib.request.Request(article['field_article_image_1'])
      thumbresp = urllib.request.urlopen(thumbreq,timeout=600)
      imagedata = thumbresp
      original_file, original_extension = apps.common.functions.findfileext_media(article['field_article_image_1'])
      newsthumbimage.image_file.save(original_file + original_extension, imagedata)
      newsthumbimage.save()
