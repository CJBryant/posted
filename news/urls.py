from django.conf.urls import url

from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.index_page, name='index'),
    url(r'^myarticles/$', views.my_articles_page, name='myarticles'),
    url(r'^myfeeds/$', views.my_feeds_page, name='myfeeds'),
    url(r'^providers/$', views.publishers_page, name ='publishers'),
    url(r'^providers/(?P<publisher_id>\w+)/$', views.publisher_page, name='publisher'),
    url(r'^providers/(?P<publisher_id>\w+)/(?P<feed_id>\w+)/$', views.feed_page, name='feed'),
]
