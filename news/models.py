from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from dtime_news_core.constants import CoreConstant as CORE_CONST
from dtime_news_core.permissions import BaseGlobalMixin, BaseObjectMixin
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils import timezone


class Category(models.Model):

    STATUS_CHOICES = (
                      (CORE_CONST.STATUS_ACTIVE, _('Active')),
                      (CORE_CONST.STATUS_INACTIVE, _('Inactive')),
                     )
    name = models.CharField(_('name'), 
                            max_length =100,
                            unique=True)

    status = models.CharField(max_length = 30,
                              choices  = STATUS_CHOICES,
                              default  = CORE_CONST.STATUS_ACTIVE)
    
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Menu(models.Model):

    STATUS_CHOICES = (
                      (CORE_CONST.STATUS_ACTIVE, _('Active')),
                      (CORE_CONST.STATUS_INACTIVE, _('Inactive')),
                     )

    name = models.CharField(_('name'), 
                            max_length =100,
                            unique=True )

    url = models.TextField(_('link url'),
                            blank = True,
                            null  = True 
                            )

    status = models.CharField(max_length = 30,
                              choices  = STATUS_CHOICES,
                              default  = CORE_CONST.STATUS_ACTIVE)
    main_menu = models.ForeignKey('self',
                                  on_delete=models.CASCADE, 
                                  verbose_name = _('main menu'),
                                  related_name= 'sub_menus',
                                  blank=True, 
                                  null=True 
                                )
    order = models.PositiveIntegerField(_('order'), default = 0)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class News(models.Model, BaseGlobalMixin, BaseObjectMixin):
    
    STATUS_CHOICES = (
                      (CORE_CONST.STATUS_PUBLISH, _('Published')),
                      (CORE_CONST.STATUS_UNPUBLISH, _('Un-Publish')),
                      )
                      
    APPROVAL_STATUS_CHOICES = (
                              (CORE_CONST.APPROVAL_STATUS_DRAFTING, _('Drafting')),
                              (CORE_CONST.APPROVAL_STATUS_WAITING, _('Waiting Approval')),
                              (CORE_CONST.APPROVAL_STATUS_APPROVED, _('Approved')),
                              (CORE_CONST.APPROVAL_STATUS_REJECTED, _('Rejected')),
                              )
                              
    title = models.CharField(_('Title'),
                             max_length=500)
    
    content = models.TextField(_('Content'),
                                  blank = True,
                                  null  = True 
                                  )

    
    expert_text = models.TextField(_('Expert Text'),
                                  blank = True,
                                  null  = True 
                                  )

    created = models.DateTimeField(_('created'),
                                   default = timezone.now) 
    
    creator = models.ForeignKey(User,
                                verbose_name = _('creator'),
                                related_name = 'created_news',
                                on_delete = models.CASCADE,
                                blank = True,
                                null  = True)
    
    published = models.DateTimeField(_('published'),
                                   blank = True,
                                   null  = True,
                                   default = timezone.now) 
    tags = TaggableManager()
    
    thumbnail = models.TextField(   blank = True,
                                    null  = True )
    
    categories = models.ManyToManyField(Category, 
                                        verbose_name = _('categories'), 
                                        related_name = 'news')
    
    status = models.CharField(max_length = 30,
                              choices  = STATUS_CHOICES,
                              default  = CORE_CONST.STATUS_UNPUBLISH)
                              
    show_in_slide = models.BooleanField(default=False)
    
    approval_status = models.CharField(max_length = 30,
                              choices  = APPROVAL_STATUS_CHOICES,
                              default  = CORE_CONST.APPROVAL_STATUS_DRAFTING)
                              
    visited_count = models.PositiveIntegerField(_('visited_count'), 
                                        default = 0)
    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return u'%s' % self.title
    
class NewsAction(models.Model):

    ACTION_CHOICES = ((CORE_CONST.ACTION_SUBMIT, _('Submit')),
                      (CORE_CONST.ACTION_APPROVE, _('Approve')),
                      (CORE_CONST.ACTION_REJECT, _('Reject')),
                      )
    
    news = models.ForeignKey(News, 
                             on_delete=models.CASCADE,
                             verbose_name = _('news'),
                             related_name = 'news_actions')
    

    action = models.CharField(max_length = 30,
                              choices  = ACTION_CHOICES,
                              default  = CORE_CONST.ACTION_SUBMIT
                              )

    comments = models.TextField(blank = True, null  = True)
    
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name = _('creator'),
                                related_name = 'news_actions')
    
    date_created = models.DateTimeField(auto_now_add=True,  null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)  

