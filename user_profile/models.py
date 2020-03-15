# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
# from avatar.utils import get_primary_avatar
from django.utils.html import format_html
from .constants import UserProfileConstant as USER_PROFILE_CONST
from news.models import Category, News
import datetime
from django.conf import settings
from PIL import Image

class Profile(models.Model):
    GENDER_CHOICES = (
          (USER_PROFILE_CONST.GENDER_MALE, _('male')),
          (USER_PROFILE_CONST.GENDER_FEMALE, _('female')),
    )

    ROLE_CHOICES = (
          (USER_PROFILE_CONST.ROLE_VIEWER, _('viewer')),
          (USER_PROFILE_CONST.ROLE_EDITOR, _('editor')),
          (USER_PROFILE_CONST.ROLE_CATEGORIZED_CONTENT_APPROVER, _('categorized content approver')),
          (USER_PROFILE_CONST.ROLE_ADMIN_CONTENT_APPROVER, _('admin content approver')),
          (USER_PROFILE_CONST.ROLE_SYSTEM_ADMIN, _('system admin')),
          (USER_PROFILE_CONST.ROLE_SUPER_ADMIN, _('super adminn')),
    )
    
    name        = models.CharField(_('name'), 
                                   max_length=100,
                                   null=True,
                                   blank=True)
    
    
    gender      = models.CharField(_('gender'),
                                   max_length=10, 
                                   choices=GENDER_CHOICES,
                                   null=True,
                                   blank=True)
    
    phone_number= PhoneNumberField(_('phone number'),
                                   blank=True)
    
    date_of_birth  = models.DateField(_('date of birth'),
                                      blank=True,
                                      null=True,
                                      default = datetime.date.today)
    
    
    about       = models.TextField(_('about'), 
                                   null=True, 
                                   blank=True)

    role        = models.CharField(_('role'),
                                   max_length=50, 
                                   choices=ROLE_CHOICES,
                                   default = USER_PROFILE_CONST.ROLE_VIEWER)
    
    user        = models.OneToOneField(User,
                                       on_delete=models.CASCADE, 
                                       related_name = 'profile',
                                       null=True, 
                                       blank=True )
    
    news_categories = models.ManyToManyField(Category, 
                                            verbose_name='news categories',
                                            related_name = 'user_profile',
                                            blank=True
                                            )
    avatar = models.FileField(upload_to='user_profile/',null=True, blank=True)

    def avatar_tag(self):
        return format_html('<a href="%s"><img style="width:80px;height:80px;border-radius:40px;object-fit: cover;" src="%s"/></a>' % (self.avatar.url, self.avatar.url))

    avatar.allow_tags = True
    avatar_tag.short_description = 'Profile' 
    
@receiver(post_save, sender=User)
def create_profile(sender, instance=None, **kwargs):
    
    if instance is None:
        return
    
    Profile.objects.get_or_create(user=instance)

class SaveNews(models.Model):

    user= models.ForeignKey( User,
                             on_delete = models.CASCADE, 
                             related_name = 'user_news',
                             null=True, 
                             blank=True)

    news = models.ForeignKey( News,
                              on_delete = models.CASCADE,
                              related_name = 'save_news',
                              null=True,
                              blank=True)

    date_created = models.DateTimeField(auto_now_add=True,  null=True)

    date_modified = models.DateTimeField(auto_now=True, null=True)  

