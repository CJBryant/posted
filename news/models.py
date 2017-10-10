import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    code = models.CharField(max_length=20, primary_key=True)
    image_url = models.CharField(max_length=100)
    article_alt_image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Feed(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, unique=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    last_updated = models.CharField(max_length=100, default='0')
    section = models.CharField(max_length=20)
    followers = models.ManyToManyField(User,through='Following')

    def __str__(self):
        return self.publisher.name + ' - ' + self.name

class Tag(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, unique=True)
    image_url = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    url_rss = models.CharField(max_length=200, unique=True)
    tags = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, through='Added')

    def __str__(self):
        return self.title

    def published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Added(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.article.title

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' : ' + self.feed.publisher.name + ' - ' + self.feed.name
