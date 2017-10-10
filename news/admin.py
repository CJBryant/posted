from django.contrib import admin

# Register your models here.
from .models import Article, Publisher, Feed, Tag, Added, Following

admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Feed)
admin.site.register(Tag)
admin.site.register(Added)
admin.site.register(Following)
