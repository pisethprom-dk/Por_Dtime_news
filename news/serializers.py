from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from .models import ( Category, News, NewsAction, Menu )
from django.contrib.auth.models import User

# category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# menu serializer
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')

# news serializer -(read)
class NewsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    creator = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = News
        fields ='__all__'

# news serializer -(write)
class AddNewsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    categories = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields ='__all__' 

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        news = serializers.ModelSerializer.update(self, instance, validated_data)
        news.tags.set(*tags)

        return news

    # get detail infor category     
    def get_categories(self,obj):
        serializer = CategorySerializer(obj.categories, many=True)

        return serializer.data    
  
# news action serializer
class NewsActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsAction
        fields = '__all__'
        
    def create(self, validated_data):
        news_id = self.data['news']
        action =  self.data['action']
        News.objects.filter(pk = news_id).update(approval_status= action)

        return NewsAction.objects.create(**validated_data)

# slide news
class SlideNewsSerializer(serializers.ModelSerializer):
    
    tags = TagListSerializerField()
    creator = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = News
        fields ='__all__'