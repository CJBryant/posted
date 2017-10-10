import csv
from news.models import Publisher, Feed

def load_data():
    fields = ['name', 'url', 'code', 'image_url', 'article_alt_image_url']
    for row in csv.reader(open('publishers.csv')):
        Publisher.objects.create(**dict(zip(fields, row)))

    fields = ['name', 'url', 'publisher', 'last_updated', 'section']
    for row in csv.reader(open('feeds.csv')):
        feed_data = dict(zip(fields, row))
        feed_data['publisher'] = Publisher.objects.get(code=feed_data['publisher'])
        Feed.objects.create(**feed_data)

load_data()
