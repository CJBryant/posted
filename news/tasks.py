import re
from time import time, sleep
from datetime import datetime
from celery import shared_task
import feedparser as fp
import ssl
# from lxml import html, cssselect
import requests
from bs4 import BeautifulSoup
from .models import Article, Feed
from django.utils import timezone
from django.db.utils import IntegrityError
import pytz
UTC = pytz.UTC

@shared_task
def article_maintenance():
    try:
        start = time()
        print('Updating articles...')
        update_articles()
        print('Fetching new articles...')
        get_new_articles()
        end = time()
        print('Article maintenance took', str(int(end - start)), 'seconds.')
    except (KeyboardInterrupt, SystemExit):
        pass

@shared_task
def update_articles():
    date_from = timezone.now() - timezone.timedelta(hours=8)
    recent_articles = Article.objects.filter(pub_date__gte=date_from)
    for article in recent_articles:
        print('Updating... ' + article.title)
        r = requests.get(article.url_rss, headers={'User-agent':'Mozilla/5.0'})
        page = BeautifulSoup(r.content, 'html.parser')
        try:
            article_title = page.find(property='og:title').get('content')
            article.title = article_title
        except:
            print(article.title + ' has no og:title.')
        try:
            article_description = page.find(property='og:description').get('content')
            article.description = article_description
        except:
            print(article.title + ' has no og:description.')
        try:
            article_url = page.find(property='og:url').get('content')
            article.url = article_url
        except:
            print(article.title + ' has no og:url.')
        try:
            article_image_url = page.find(property='og:image').get('content')
            article.image_url = article_image_url
        except:
            print(article.title + ' has no og:image.')
        try:
            article.save()
        except IntegrityError:
            print(article.title + ' is a duplicate.')
            article.delete()

@shared_task
def get_new_articles():
    feeds = Feed.objects.all()
    for feed in feeds:
        print('Processing... ' + feed.publisher.name + ' - ' + feed.name)
        parse_feed(feed)

@shared_task
def parse_feed(feed):
    loaded_articles_url_rss = {article.url_rss for article in feed.publisher.article_set.all()}
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    channel = fp.parse(feed.url)
    for item in channel['entries']:
        if not_already_seen(item, loaded_articles_url_rss):
            article_info = get_article(feed, item)
            article = Article(**article_info)
            try:
                article.save()
                print('Saving...', article.title)
            except IntegrityError:
                print(article.title + ' already exists.')
        sleep(0.1)

@shared_task
def not_already_seen(item, loaded_articles):
    url_rss = re.search(r'[^\?]+', item['link']).group()
    return url_rss not in loaded_articles

@shared_task
def get_article(feed, item):
    article_url_rss = re.search(r'[^\?]+', item['link']).group()
    r = requests.get(article_url_rss, headers={'User-agent':'Mozilla/5.0'})
    page = BeautifulSoup(r.content, 'html.parser')
    # page = html.fromstring(requests.get(article_url_rss, headers={'User-agent':'Mozilla/5.0'}).content)
    try:
        article_title = page.find(property='og:title').get('content')
    except AttributeError:
        article_title = item['title']
    try:
        article_url = page.find(property='og:url').get('content')
    except AttributeError:
        article_url = '#'
    try:
        article_description = page.find(property='og:description').get('content')
    except:
        article_description = ''
    try:
        article_image_url = page.find(property='og:image').get('content')
    except AttributeError:
        article_image_url = ''
    try:
        article_pub_date = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        article_pub_date = UTC.localize(datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %Z'))
    return {'title': article_title,
            'description': article_description,
            'publisher': feed.publisher,
            'feed': feed,
            'url': article_url,
            'image_url': article_image_url,
            'pub_date': article_pub_date,
            'url_rss': article_url_rss,
            }
