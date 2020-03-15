from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, SaveNews
from news.serializers import NewsSerializer


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude= ('password','user_permissions','groups')

class UserProfileSerializer(serializers.ModelSerializer):

    # first_name = serializers.CharField(max_length=100, 
    #                                    source='user.first_name', 
    #                                    required=False)
    # last_name = serializers.CharField(max_length=100, 
    #                                   source='user.last_name', 
    #                                   required=False)

    email = serializers.CharField(max_length=100, 
                                  source='user.email', 
                                  required=False)
    user = UserAuthSerializer()
    class Meta: 
        model = Profile
        exclude= ('role',)
        depth = 1
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data:
            User.objects.filter(id=instance.user.id).update(**user_data)
        return serializers.ModelSerializer.update(self, instance, validated_data)
    
class UserRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
          model = Profile
          fields = ('role',)

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Profile
        fields = '__all__'

class SaveNewSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SaveNews
        fields = '__all__'

class ListSaveNewsSerializer(serializers.ModelSerializer):
    news = NewsSerializer()
    class Meta:
        model =  SaveNews
        fields = '__all__'