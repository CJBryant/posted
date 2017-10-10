from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()

@register.filter
def keyvalue(dict, key):
    return dict[key]

@register.filter(needs_autoescape=True)
def follow(feed, user, autoescape=True):
    if feed in user.feed_set.all():
        css_class = ' unfollow-btn'
        btn_text = 'Following'
    else:
        css_class = ''
        btn_text = 'Follow'
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<button type="button" id="feed-%s" class="btn follow-btn%s">%s</button>' % (esc(feed.id), esc(css_class), esc(btn_text))
    return mark_safe(result)

@register.filter(needs_autoescape=True)
def add_article(article, user, autoescape=True):
    if article in user.article_set.all():
        css_class = ' remove-btn'
        btn_glyph = 'glyphicon-minus'
    else:
        css_class = ''
        btn_glyph = 'glyphicon-plus'
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<button type="button" id="article-%s" class="btn add-btn%s"><span class="glyphicon %s" aria-hidden="true"></span></button>' % (esc(article.id), esc(css_class), esc(btn_glyph))
    return mark_safe(result)
