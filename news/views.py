from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import RequestContext
from el_pagination.decorators import page_template
from .models import Article, Publisher, Feed, Tag, Following, Added
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def index_page(request, template = 'news/news_home.html', page_template = 'news/news_article_list.html', extra_context=None):

    current_user = request.user

    # Load articles to page
    article_list = Article.objects.filter(feed__followers=current_user).order_by('-pub_date')
    if len(article_list) == 0:
        return render(request, 'no_articles.html')
    else:
        context = {}
        context['article_list'] = article_list
        context['page_template'] = page_template
        if extra_context is not None:
            context.update(extra_context)
        if request.is_ajax():
            template = page_template

        # Add or remove article from list
        if request.is_ajax() and request.POST:
            article_id = int(request.POST['article'][8:])
            ajax_article = Article.objects.get(id = article_id)
            ajax_action = request.POST['action']
            if ajax_action == 'add':
                try:
                    a = Added.objects.create(user = current_user, article = ajax_article)
                    a.save()
                except:
                    return HttpResponse('Error')
            else:
                try:
                    a = Added.objects.filter(Q(user = current_user), Q(article = ajax_article))
                    a.delete()
                except:
                    return HttpResponse('Error')
        # Render page
        return render(request, template, context)

@login_required
def publishers_page(request, template = 'news/news_publishers.html'):
    context = {}
    if request.is_ajax():
        current_user = request.user
        feed_id = int(request.POST['feed'][5:])
        ajax_feed = Feed.objects.get(id = feed_id)
        ajax_action = request.POST['action']
        if ajax_action == 'follow':
            try:
                f = Following.objects.create(user = current_user, feed = ajax_feed)
                f.save()
            except:
                return HttpResponse('Error')
        else:
            try:
                f = Following.objects.get(Q(user = current_user), Q(feed = ajax_feed))
                f.delete()
            except:
                return HttpResponse('Error')
    else:
        context['publishers_list'] = get_list_or_404(Publisher.objects.all())
        feeds_list = {}
        for pub in context['publishers_list']:
            feeds_list[pub.code] = get_list_or_404(Feed.objects.filter(publisher = pub))
        context['feeds_list'] = feeds_list
    return render(request, template, context)

@login_required
def publisher_page(request, publisher_id, template = 'news/news_publisher.html'):
    publisher = get_object_or_404(Publisher, code=publisher_id)
    context = {}
    context['publisher'] = publisher
    context['publisher_feed_list'] = get_list_or_404(publisher.feed_set)
    return render(request, template, context)

@login_required
def feed_page(request, publisher_id, feed_id,
    template = 'news/news_feed.html', page_template = 'news/news_article_list.html', extra_context=None):

    # Load articles to page
    feed = get_object_or_404(Feed, id=feed_id)
    article_list = get_list_or_404(feed.article_set.all().order_by('-pub_date'))
    if len(article_list) == 0:
        return render(request, 'no_articles.html')
    context = {}
    context['feed'] = feed
    context['publisher'] = feed.publisher
    context['article_list'] = article_list
    context['page_template'] = page_template
    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax():
        template = page_template

    # Add or remove article from list
    current_user = request.user
    if request.is_ajax() and request.POST:
        article_id = int(request.POST['article'][8:])
        ajax_article = Article.objects.get(id = article_id)
        ajax_action = request.POST['action']
        if ajax_action == 'add':
            try:
                a = Added.objects.create(user = current_user, article = ajax_article)
                a.save()
            except:
                return HttpResponse('Error')
        else:
            try:
                a = Added.objects.filter(Q(user = current_user), Q(article = ajax_article))
                a.delete()
            except:
                return HttpResponse('Error')
    # Render page
    return render(request, template, context)

@login_required
def my_articles_page(request, template = 'news/news_my_articles.html', page_template = 'news/news_my_articles_list.html', extra_context=None):

    current_user = request.user

    # Load articles to page
    article_list = current_user.article_set.order_by('-pub_date')
    if len(article_list) == 0:
        return render(request, 'no_articles.html')
    else:
        context = {}
        context['article_list'] = article_list
        context['page_template'] = page_template
        if extra_context is not None:
            context.update(extra_context)
        if request.is_ajax():
            template = page_template

        # Add or remove article from list
        if request.is_ajax() and request.POST:
            article_id = int(request.POST['article'][8:])
            ajax_article = Article.objects.get(id = article_id)
            ajax_action = request.POST['action']
            if ajax_action == 'add':
                try:
                    a = Added.objects.create(user = current_user, article = ajax_article)
                    a.save()
                except:
                    return HttpResponse('Error')
            else:
                try:
                    a = Added.objects.filter(Q(user = current_user), Q(article = ajax_article))
                    a.delete()
                except:
                    return HttpResponse('Error')
        # Render page
        return render(request, template, context)

def my_feeds_page(request, template = 'news_my_feeds.html'):
    current_user = request.user
    context = {}
    if request.is_ajax():
        current_user = request.user
        feed_id = int(request.POST['feed'][5:])
        ajax_feed = Feed.objects.get(id = feed_id)
        ajax_action = request.POST['action']
        if ajax_action == 'follow':
            try:
                f = Following.objects.create(user = current_user, feed = ajax_feed)
                f.save()
            except:
                return HttpResponse('Error')
        else:
            try:
                f = Following.objects.get(Q(user = current_user), Q(feed = ajax_feed))
                f.delete()
            except:
                return HttpResponse('Error')
    else:
        feeds_list = current_user.feed_set.order_by('publisher')
        if len(feeds_list) == 0:
            return render(request, 'no_feeds.html')
        else:
            context['feeds_list'] = feeds_list
    return render(request, template, context)
