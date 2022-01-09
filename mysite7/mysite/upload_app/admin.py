from django.contrib import admin

# Register your models here.
from .models import Content


class ContentManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'picture']
    list_display_links = ['title']






admin.site.register(Content, ContentManager)
