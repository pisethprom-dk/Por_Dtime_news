# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from dtime_news_core.views import (BaseAPIView, BaseAPIView_LatestNew,
                                   BaseListCreateAPIView, BaseListTagAPIView,
                                   BaseRetrieveUpdateDestroyAPIView)
from dtime_news_core.constants import CoreConstant as CORE_CONST 
from .serializers import ( CategorySerializer, MenuSerializer, NewsSerializer,
                         NewsActionSerializer, AddNewsSerializer, SlideNewsSerializer )
from .models import (Menu)
from rest_framework.response import Response
from rest_framework import status
# category view
class CategoryView(BaseListCreateAPIView):
    model_class = CategorySerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = CategorySerializer
    filter_fields = ('status',)
    search_fields = ('name',)

# category detail view 
class CategoryDetailView(BaseRetrieveUpdateDestroyAPIView):
    model_class = CategorySerializer.Meta.model
    queryset = model_class.objects.all().order_by('-id')
    serializer_class = CategorySerializer

# menu view
class MenuView(BaseListCreateAPIView):
    model_class = MenuSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = MenuSerializer
    
    def get(self, request, *args, **kwargs):
        menu_list = Menu.objects.filter(main_menu__isnull=True,status=CORE_CONST.STATUS_ACTIVE).order_by('order')
        list_menu = []
        for m in menu_list:
          list_sub_menu =[]
          sub_menu = Menu.objects.filter(main_menu=m.id,status=CORE_CONST.STATUS_ACTIVE).order_by('order')

          if(len(sub_menu)>0):
              for m1 in sub_menu:
                sub_menu_obj = {
                    "id": m1.id,
                    "name": m1.name,
                    "url": m1.url,
                    "status": m1.status,
                    "order": m1.order
                }
                list_sub_menu.append(sub_menu_obj)
            
          menu_obj = {
                "id": m.id,
                "name": m.name,
                "url": m.url,
                "status": m.status,
                "order": m.order,
                "sub_menu": list_sub_menu
          }

          list_menu.append(menu_obj)

        return Response({'menus':list_menu,'count':len(list_menu)}) 

# parent view 
class ParentMenu(BaseListCreateAPIView):
    model_class = MenuSerializer.Meta.model
    queryset = model_class.objects.filter(main_menu__isnull=True).order_by('order')
    serializer_class = MenuSerializer
    filter_fields = ('status',)
    search_fields = ('name',)

# menu detail view
class MenuDetailView(BaseRetrieveUpdateDestroyAPIView):
    model_class = MenuSerializer.Meta.model
    queryset = model_class.objects.all().order_by('-id')
    serializer_class = MenuSerializer

# news view
class NewsView(BaseListCreateAPIView):
    model_class = NewsSerializer.Meta.model
    queryset = model_class.objects.all().order_by('-created')
    serializer_class = NewsSerializer
    filter_fields = ('status','id','categories__id')
    search_fields = ('title',)

# add news view
class AddNewsView(BaseListCreateAPIView):
    model_class = AddNewsSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = AddNewsSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        request.data.update({'creator': request.user.id})
        return BaseListCreateAPIView.post(self, request, *args, **kwargs)

# news detail view
class NewsDetailView(BaseRetrieveUpdateDestroyAPIView):
    model_class = AddNewsSerializer.Meta.model
    queryset = model_class.objects.all().order_by('-id')
    serializer_class = AddNewsSerializer
    
    def get(self, request, *args, **kwargs):
        visited = self.get_object().visited_count + 1
        AddNewsSerializer.Meta.model.objects.filter(
            pk=self.get_object().pk).update(visited_count=visited)
        return BaseRetrieveUpdateDestroyAPIView.get(self, request, *args, **kwargs)

# slide news view 
class SlideNewsView(BaseListCreateAPIView):
    model_class = NewsSerializer.Meta.model
    queryset = model_class.objects.filter(show_in_slide = True,status=CORE_CONST.STATUS_PUBLISH).order_by('-created')[:6]  
    serializer_class = NewsSerializer    

# related news
class RelateNewsView(BaseListCreateAPIView):
    model_class = NewsSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = NewsSerializer 

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset).filter(
                categories=request.GET['category'],status=CORE_CONST.STATUS_PUBLISH).exclude(id=request.GET['id']).order_by('-created')
        self.queryset = queryset
        return BaseListCreateAPIView.get(self, request, *args, **kwargs)

# porular news
class PorpularNewView(BaseListCreateAPIView):
    model_class = NewsSerializer.Meta.model
    queryset = model_class.objects.filter(status=CORE_CONST.STATUS_PUBLISH).order_by('-visited_count')
    serializer_class = NewsSerializer 