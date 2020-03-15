# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from dtime_news_core.views import BaseAPIView, BaseRetrieveUpdateDestroyAPIView, BaseListCreateAPIView
from .serializers import ( UserProfileSerializer, UserRoleSerializer, UserListSerializer, UserSerializer,
                           ListSaveNewsSerializer,SaveNewSerializer)                         
from .constants import UserProfileConstant as USER_PROFILE_CONST
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser 
from .models import Profile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UserProfileView(BaseAPIView):
    serializer_class = UserProfileSerializer
     
    def get(self, request):
        try:
            self.serializer = self.serializer_class(request.user.profile)
            return self.get_response()
        except Exception as error:
            return self.get_unexpected_error_response()
        
    def put(self, request):

        try:
            self.serializer = self.serializer_class(request.user.profile, data=request.data)
            # print request.data
            if self.serializer.is_valid():
                self.serializer.save()
                # customize data response
                data_response={
                    'id':self.serializer.data['id'],
                    'email':request.data['email'],
                    'name':self.serializer.data['name'],
                    'gender':self.serializer.data['gender'],
                    'phone_number':self.serializer.data['phone_number'],
                    'date_of_birth':self.serializer.data['date_of_birth'],
                    'about':self.serializer.data['about'],
                    'news_categories':self.serializer.data['news_categories'],
                    'avatar':self.serializer.data['avatar']
                }
                return Response(data_response,status=status.HTTP_200_OK)
                # return self.get_response()

            return self.get_error_response()
        except Exception as error:
            return self.get_unexpected_error_response()
          
class UserRoleView(BaseAPIView):
    
    model_class = UserRoleSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = UserRoleSerializer

    def get(self, request, *args, **kwargs):
        # query filter by user id
        queryset = self.queryset.filter(user = request.user.id)
        self.queryset = queryset
        return BaseAPIView.get(self, request, *args, **kwargs)

class UserView(BaseAPIView):
    model_class = UserListSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = UserListSerializer
    filter_fields = ('role','name','user__is_active','news_categories')
    search_fields = ('name',)

    def get(self, request, *args, **kwargs):
        # query filter by user id
        # current user login 
        # user = request.user.id
        queryset = self.queryset.exclude(role = USER_PROFILE_CONST.ROLE_SUPER_ADMIN).exclude(role = USER_PROFILE_CONST.ROLE_SYSTEM_ADMIN).order_by('-id')
        
        self.queryset = queryset
        return BaseAPIView.get(self, request, *args, **kwargs)

class UserManageView(BaseRetrieveUpdateDestroyAPIView):
    model_class = UserSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = UserSerializer

class UserPickCategoriesView(APIView):

    permission_classes = (IsAuthenticated,)

    def patch(self,request,format=None):

        user_profile = Profile.objects.get(user = request.user.id)
        user_profile.news_categories.set(request.data.get('news_categories')) 
        
        try:
            user_profile.save()
            return Response({'status':True ,'message':'Pick Category Success'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':False ,'message':'Pick Category Failed'},status=status.HTTP_501_NOT_IMPLEMENTED)

class SaveNewsView(BaseListCreateAPIView):
    model_class = SaveNewSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = SaveNewSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        request.data.update({'user': request.user.id})
        return BaseListCreateAPIView.post(self, request, *args, **kwargs)

class DetailSaveNewsView(BaseRetrieveUpdateDestroyAPIView):
    model_class = SaveNewSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = SaveNewSerializer

class ListSaveNewsView(BaseAPIView):
    model_class = ListSaveNewsSerializer.Meta.model
    queryset = model_class.objects.all()
    serializer_class = ListSaveNewsSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user = request.user.id).order_by('-id')
        self.queryset = queryset
        return BaseAPIView.get(self, request, *args, **kwargs)

