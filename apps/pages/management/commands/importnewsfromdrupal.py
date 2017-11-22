from django.core.management.base import BaseCommand, CommandError
import urllib.request
import json
import pytz
import datetime
from django.utils import timezone
import html
import uuid
from time import sleep
from apps.pages.models import News
from apps.images.models import NewsThumbnail, ContentBanner
from apps.objects.models import User
import apps.common.functions

class Command(BaseCommand):
  host = 'https://www1.slcschools.org'
  req = urllib.request.Request(host + '/rest/districtnewsall')
  resp = urllib.request.urlopen(req,timeout=600)
  districtnewsjson = resp.read().decode('utf8')
  districtnews = json.loads(districtnewsjson)
  webmaster = User.objects.get(username='webmaster@slcschools.org')
  for article in districtnews:
    sleep(2)
    article_uuid = uuid.UUID(article['uuid'])
    title = html.unescape(article['title'])
    body = article['body']
    summary = article['body_1']
    pinned = int(article['field_pin_to_home_page'])
    author_date = timezone.datetime(int(article['created_1']),int(article['created_2']), int(article['created_3']), hour=int(article['created_4']), minute=int(article['created_5']), tzinfo=timezone.utc)
    #try:
    #  news = News.objects.get(uuid=article_uuid)
    #except News.DoesNotExist:
    #  news = News.objects.create(uuid=article_uuid,title=title,body=body,author_date=author_date,deleted=0,create_user=webmaster,update_user=webmaster,published=True)
    news, created = News.objects.get_or_create(uuid=article_uuid, defaults={'title':title,'author_date':author_date,'deleted':0,'create_user':webmaster,'update_user':webmaster,'published':1,'url':'/tempnewsurl'})
    news.title=title
    news.body=body
    news.summary=summary
    news.pinned=pinned
    news.author_date=author_date
    news.deleted=False
    news.create_user=webmaster
    news.update_user=webmaster
    news.published=True
    news.save()
    print(news)
    if article['field_article_image'] != '':
      #try:
      #  newsthumbimage = NewsThumbImage.objects.get(news=news)
      #except NewsThumbImage.DoesNotExist:
      #  newsthumbimage = NewsThumbImage.objects.create(uuid=uuid.uuid5(news.uuid, article['field_article_image']), news=news, deleted=0,create_user=webmaster,update_user=webmaster, published=1)
      newsthumbimage, created = NewsThumbnail.objects.get_or_create(uuid=uuid.uuid5(news.uuid, article['field_article_image']), defaults={'related_node':news.page_node,'title':news.title + ' Thumbnail','deleted':0,'create_user':webmaster,'update_user':webmaster, 'published':1,'url':'/tempnewsthumburl','parent':news.page_node})
      newsthumbimage.related_node = news.page_node
      newsthumbimage.title = news.title + ' Thumbnail'
      newsthumbimage.deleted = 0
      newsthumbimage.create_user = webmaster
      newsthumbimage.update_user = webmaster
      newsthumbimage.published = 1
      newsthumbimage.parent = news.page_node
      newsthumbimage.alttext=article['field_article_image_2']
      thumbreq = urllib.request.Request(article['field_article_image_1'])
      thumbresp = urllib.request.urlopen(thumbreq,timeout=600)
      imagedata = thumbresp
      original_file, original_extension = apps.common.functions.findfileext_media(article['field_article_image_1'])
      newsthumbimage.image_file.save(original_file + original_extension, imagedata)
      newsthumbimage.save()
    bannerids = article['field_district_news_banner'].split('***ITEM_SEPARATOR***')
    bannerurls = article['field_district_news_banner_1'].split('***ITEM_SEPARATOR***')
    banneralts = article['field_district_news_banner_2'].split('***ITEM_SEPARATOR***')
    bannercount = 0
    for banner in bannerids:
      if bannerids[bannercount]:
        #try:
        #  newsbannerimage = NewsBannerImage.objects.get(uuid=uuid.uuid5(news.uuid, bannerids[bannercount]))
        #except NewsBannerImage.DoesNotExist:
        #  newsbannerimage = NewsBannerImage.objects.create(uuid=uuid.uuid5(news.uuid, bannerids[bannercount]), news=news, deleted=0,create_user=webmaster,update_user=webmaster, published=1)
        newsbannerimage, created = ContentBanner.objects.get_or_create(uuid=uuid.uuid5(news.uuid, bannerids[bannercount]), defaults={'related_node':news.page_node,'title':news.title + ' Banner ' + str(bannercount),'deleted':0,'create_user':webmaster,'update_user':webmaster, 'published':1,'url':'/tempnewsbannerurl','parent':news.page_node})
        newsbannerimage.related_node = news.page_node
        newsbannerimage.title = news.title + ' Banner ' + str(bannercount)
        newsbannerimage.deleted = 0
        newsbannerimage.create_user = webmaster
        newsbannerimage.update_user = webmaster
        newsbannerimage.published = 1
        newsbannerimage.parent = news.page_node
        newsbannerimage.alttext=banneralts[bannercount]
        bannerreq = urllib.request.Request(bannerurls[bannercount])
        bannerresp = urllib.request.urlopen(bannerreq,timeout=600)
        imagedata = bannerresp
        original_file, original_extension = apps.common.functions.findfileext_media(bannerurls[bannercount])
        newsbannerimage.image_file.save(original_file + original_extension, imagedata)
        newsbannerimage.save()
        bannercount += 1
