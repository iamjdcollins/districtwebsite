from django.core.management.base import BaseCommand
import urllib.request
import json
from django.utils import timezone
import html
import uuid
from django.contrib.sites.models import Site
from time import sleep
from apps.pages.models import News
from apps.images.models import NewsThumbnail, ContentBanner, \
    PhotoGallery, PhotoGalleryImage
from apps.objects.models import User
import apps.common.functions


class Command(BaseCommand):
    site = Site.objects.get(domain='www.slcschools.org')
    host = 'https://www1.slcschools.org'
    req = urllib.request.Request(host + '/rest/districtnewsall')
    resp = urllib.request.urlopen(req, timeout=1200)
    districtnewsjson = resp.read().decode('utf8')
    districtnews = json.loads(districtnewsjson)
    webmaster = User.objects.get(username='webmaster@slcschools.org')
    for article in districtnews:
        sleep(2)
        article_id = article['nid']
        article_uuid = uuid.UUID(article['uuid'])
        title = html.unescape(article['title'])
        body = article['body']
        summary = article['body_1']
        pinned = int(article['field_pin_to_home_page'])
        author_date = timezone.datetime(
            int(article['created_1']),
            int(article['created_2']),
            int(article['created_3']),
            hour=int(article['created_4']),
            minute=int(article['created_5']),
            tzinfo=timezone.utc
        )
        news, created = News.objects.get_or_create(
            uuid=article_uuid,
            defaults={
                'title': title,
                'author_date': author_date,
                'deleted': 0,
                'create_user': webmaster,
                'update_user': webmaster,
                'published': 1,
                'url': '/tempnewsurl',
                'site': site
            }
        )
        news.title = title
        news.body = body
        news.summary = summary
        news.pinned = pinned
        news.author_date = author_date
        news.deleted = False
        news.create_user = webmaster
        news.update_user = webmaster
        news.published = True
        news.save()
        print(news)
        if article['field_article_image'] != '':
            newsthumbimage, created = NewsThumbnail.objects.get_or_create(
                uuid=uuid.uuid5(news.uuid, article['field_article_image']),
                defaults={
                    'related_node': news.page_node,
                    'title': news.title + ' Thumbnail',
                    'deleted': 0,
                    'create_user': webmaster,
                    'update_user': webmaster,
                    'published': 1,
                    'url': '/tempnewsthumburl',
                    'parent': news.page_node,
                    'site': site
                }
            )
            newsthumbimage.related_node = news.page_node
            newsthumbimage.title = news.title + ' Thumbnail'
            newsthumbimage.deleted = 0
            newsthumbimage.create_user = webmaster
            newsthumbimage.update_user = webmaster
            newsthumbimage.published = 1
            newsthumbimage.parent = news.page_node
            newsthumbimage.alttext = article['field_article_image_2']
            thumbreq = urllib.request.Request(article['field_article_image_1'])
            thumbresp = urllib.request.urlopen(thumbreq, timeout=1200)
            imagedata = thumbresp
            original_file, original_extension = \
                apps.common.functions.findfileext_media(
                    article['field_article_image_1'])
            newsthumbimage.image_file.save(
                    original_file + original_extension, imagedata)
            newsthumbimage.save()
        bannerids = article['field_district_news_banner'].split(
            '***ITEM_SEPARATOR***')
        bannerurls = article['field_district_news_banner_1'].split(
            '***ITEM_SEPARATOR***')
        banneralts = article['field_district_news_banner_2'].split(
            '***ITEM_SEPARATOR***')
        bannercount = 0
        for banner in bannerids:
            if bannerids[bannercount]:
                newsbannerimage, created = ContentBanner.objects.get_or_create(
                    uuid=uuid.uuid5(news.uuid, bannerids[bannercount]),
                    defaults={
                        'related_node': news.page_node,
                        'title': news.title + ' Banner ' + str(bannercount),
                        'deleted': 0,
                        'create_user': webmaster,
                        'update_user': webmaster,
                        'published': 1,
                        'url': '/tempnewsbannerurl',
                        'parent': news.page_node,
                        'site': site
                    }
                )
                newsbannerimage.related_node = news.page_node
                newsbannerimage.title = '{0} Banner {1}'.format(
                    news.title,
                    str(bannercount)
                )
                newsbannerimage.deleted = 0
                newsbannerimage.create_user = webmaster
                newsbannerimage.update_user = webmaster
                newsbannerimage.published = 1
                newsbannerimage.parent = news.page_node
                newsbannerimage.alttext = banneralts[bannercount]
                bannerreq = urllib.request.Request(bannerurls[bannercount])
                bannerresp = urllib.request.urlopen(bannerreq, timeout=1200)
                imagedata = bannerresp
                original_file, original_extension = \
                    apps.common.functions.findfileext_media(
                            bannerurls[bannercount])
                newsbannerimage.image_file.save(
                        original_file + original_extension, imagedata)
                newsbannerimage.save()
                bannercount += 1
        photogalreq = urllib.request.Request(
                host + '/rest/districtnews/photo-galleries-1/' + article_id)
        photogalresp = urllib.request.urlopen(photogalreq, timeout=1200)
        photogaljson = photogalresp.read().decode('utf8')
        photogal = json.loads(photogaljson)
        for gallery in photogal:
            gallery_uuid = uuid.UUID(gallery['uuid'])
            gallery_title = html.unescape(gallery['title'])
            photogallery, created = PhotoGallery.objects.get_or_create(
                uuid=gallery_uuid,
                defaults={
                    'related_node': news.page_node,
                    'title': gallery_title,
                    'deleted': 0,
                    'create_user': webmaster,
                    'update_user': webmaster,
                    'published': 1,
                    'url': '/tempgalleryurl',
                    'parent': news.page_node,
                    'site': site
                }
            )
            photogallery.title = gallery_title
            photogallery.save()
            galleryphotos = gallery['field_gallery_photo'].split(
                '***ITEM_SEPARATOR***')
            photocount = 0
            for photo in galleryphotos:
                photolist = photo.split('***ATTR_SEPARATOR***')
                photogalleryimage_uuid = uuid.uuid5(
                    photogallery.uuid, photolist[2])
                photogalleryimage_title = '{0} Image {1}'.format(
                    photogallery.title,
                    photocount,
                )
                photogalleryimage_alt = html.unescape(photolist[1])
                galimage, created = PhotoGalleryImage.objects.get_or_create(
                    uuid=photogalleryimage_uuid,
                    defaults={
                        'related_node': photogallery.image_node,
                        'title': photogalleryimage_title,
                        'alttext': photogalleryimage_alt,
                        'deleted': 0,
                        'create_user': webmaster,
                        'update_user': webmaster,
                        'published': 1,
                        'url': '/tempphotogalleryimageurl',
                        'parent': photogallery.image_node,
                        'site': site
                    }
                )
                galimage.alttext = photogalleryimage_alt
                galimagereq = urllib.request.Request(photolist[0])
                galimageresp = urllib.request.urlopen(
                    galimagereq, timeout=1200)
                imagedata = galimageresp
                original_file, original_extension = \
                    apps.common.functions.findfileext_media(
                            photolist[0])
                galimage.image_file.save(
                        original_file + original_extension, imagedata)
                galimage.save()
                photocount += 1
