# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from dtime_news_core.admin import BaseModelAdmin
from .models import ( News, NewsAction, Category, Menu)
# Register your models here.
admin.site.register(Category, BaseModelAdmin) 
admin.site.register(Menu, BaseModelAdmin)
admin.site.register(News, BaseModelAdmin) 
admin.site.register(NewsAction, BaseModelAdmin)
