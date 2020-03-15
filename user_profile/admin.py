# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Profile, SaveNews
from dtime_news_core.admin import BaseModelAdmin
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('avatar_tag',)
    list_display = ('id','name','gender','phone_number','date_of_birth','about','role','user','avatar_tag',)
    search_fields =('name',)

admin.site.register(Profile, ProfileAdmin) 
admin.site.register(SaveNews, BaseModelAdmin)