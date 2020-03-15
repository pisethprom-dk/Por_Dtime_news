# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from datetime import timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from filer.models import Folder, Image
from dtime_news_core.views import BaseAPIView, BaseListCreateAPIView, BaseRetrieveUpdateDestroyAPIView
from .serializers import FolderSerializer, ImageSerializer, VideoSerializer
from .models import Video
from rest_framework.views import APIView
from io import BytesIO
import traceback

# Folder View
class FolderView(BaseListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_fields = ('name', 'level')

# Folder Detail View
class FolderDetailView(BaseRetrieveUpdateDestroyAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

# Sub Folder Detail View
class SubFolderView(FolderView):

    def get(self, request,  *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.queryset)
            paginated_queryset = self.paginate_queryset(queryset)
            self.serializer = self.get_serializer(
                paginated_queryset, many=True)

            return self.get_paginated_response(self.serializer.data)
        except Exception as err:
            return self.get_unexpected_error_response()

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data.update({'parent': kwargs['pk']})
            self.serializer = self.get_serializer(data=data)
            if self.serializer.is_valid():
                return self.get_creation_response()
            return self.get_error_response()

        except Exception as err:
            return self.get_unexpected_error_response()

    def filter_queryset(self, queryset):

        folder_name = self.kwargs.get('pk', None)
        folderobj = Folder.objects.get(name=folder_name)
        pk = folderobj.id

        queryset = FolderView.filter_queryset(self, queryset)
        queryset = queryset.filter(parent=pk)
        return queryset

# Image View
class ImageView(BaseListCreateAPIView):
    queryset = Image.objects.order_by('-id')
    serializer_class = ImageSerializer
    filter_fields = ('name', 'folder')

    def get(self, request,  *args, **kwargs):

        # option star_date and end_date
        star_date = request.GET.get('date_from', False)
        end_date = request.GET.get('date_to', False)

        if star_date and end_date:
            star_date = datetime.datetime.strptime(star_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            queryset = self.queryset.filter(uploaded_at__range=[star_date, end_date])
            self.queryset = queryset
        return BaseAPIView.get(self, request, *args, **kwargs)

# Image By Folder 
class ImageByFolderView(ImageView):

    def get(self, request,  *args, **kwargs):
        # option star_date and end_date if have date_from and date_to
        star_date = request.GET.get('date_from', False)
        end_date = request.GET.get('date_to', False)

        if star_date and end_date:
            star_date = datetime.datetime.strptime(star_date, "%Y-%m-%d").date()
            # increase one more day for filte [start_date, end_date]
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
            queryset = self.queryset.filter(uploaded_at__range=[star_date, end_date])
            self.queryset = queryset

        try:
            queryset = self.filter_queryset(self.queryset, request.user.id)
            paginated_queryset = self.paginate_queryset(queryset)
            self.serializer = self.get_serializer(
                paginated_queryset, many=True)

            return self.get_paginated_response(self.serializer.data)
        except Exception as err:
            self.message = traceback.format_exc()
            return self.get_unexpected_error_response()

    def post(self, request, *args, **kwargs):
        try:
            folder_id = kwargs['pk']
            try:
                data = request.data
                data.update({'folder': folder_id, 'owner':request.user.id})
                self.serializer = self.get_serializer(data=data)
                if self.serializer.is_valid():
                    self.serializer.save()
                    return self.get_creation_response()
                self.message = traceback.format_exc()
                return self.get_error_response()

            except Exception as err:
                self.message = traceback.format_exc()
                return self.get_unexpected_error_response()

        except Folder.DoesNotExist:
            self.message = traceback.format_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def filter_queryset(self, queryset, user_id):

        # find parent forlder ID
        folder_name = self.kwargs.get('pk', None)
        folderobj = Folder.objects.get(name=folder_name)
        pk = folderobj.id

        # check sub folder and get ID to filter
        if (folderobj.level == 0):
            subfolderobj = Folder.objects.get(parent=pk, name='images')
            pk = subfolderobj.id

        queryset = ImageView.filter_queryset(self, queryset)
        
        # filter file by user permission for role editor
        try:
            queryset = queryset.filter(folder=pk)
        except Folder.DoesNotExist:
            queryset = queryset.filter(folder=pk)
        
        # final query set 
        return queryset

# Image Detail View
class ImageDetailView(BaseRetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

# Video View
class VideoView(BaseListCreateAPIView):
    queryset = Video.objects.all().order_by('-id')
    serializer_class = VideoSerializer
    filter_fields = ('name', 'folder')

    def get(self, request,  *args, **kwargs):

        # option star_date and end_date
        star_date = request.GET.get('date_from', False)
        end_date = request.GET.get('date_to', False)

        if star_date and end_date:
            star_date = datetime.datetime.strptime(star_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            queryset = self.queryset.filter(
                uploaded_at__range=[star_date, end_date])
            self.queryset = queryset

        return BaseAPIView.get(self, request, *args, **kwargs)

# Video By Folder View
class VideoByFolderView(VideoView):

    def get(self, request,  *args, **kwargs):
        # option star_date and end_date if have date_from and date_to
        star_date = request.GET.get('date_from', False)
        end_date = request.GET.get('date_to', False)

        if star_date and end_date:
            star_date = datetime.datetime.strptime(star_date, "%Y-%m-%d").date()
            # increase one more day for filte [start_date, end_date]
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)
            queryset = self.queryset.filter(uploaded_at__range=[star_date, end_date])
            self.queryset = queryset
            
        try:
            queryset = self.filter_queryset(self.queryset, request.user.id)
            paginated_queryset = self.paginate_queryset(queryset)
            self.serializer = self.get_serializer(paginated_queryset, many=True)

            return self.get_paginated_response(self.serializer.data)
        except Exception as err:
            self.message = traceback.format_exc()
            return self.get_unexpected_error_response()

    def post(self, request, *args, **kwargs):
        try:
            # find parent folder ID
            folder_id = kwargs['pk']
            # add folder_id and file permission to filer file model
            try:
                data = request.data
                data.update({'folder': folder_id,'owner':request.user.id})
                self.serializer = self.get_serializer(data=data)
                if self.serializer.is_valid():
                    self.serializer.save()
                    return self.get_creation_response()
                return self.get_error_response()

            except Exception as err:
                return self.get_unexpected_error_response()

        except Folder.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def filter_queryset(self, queryset, user_id):
    
        folder_name = self.kwargs.get('pk', None)
        folderobj = Folder.objects.get(name=folder_name)
        pk = folderobj.id

        queryset = VideoView.filter_queryset(self, queryset)

        try:
            
                queryset = queryset.filter(folder=pk)

        except Folder.DoesNotExist:
            queryset = queryset.filter(folder=pk)

        return queryset

# Video Detail View
class VideoDetailView(BaseRetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
