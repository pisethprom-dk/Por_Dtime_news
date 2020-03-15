from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

# from user_profile.models import Profile 

class SignupSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=500)
    # gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES, 
    #                                  required=False)
    def custom_signup(self, request, user):

        adapter = get_adapter()
        username = adapter.generate_unique_username([self.validated_data['name']])
        # user.username = username
        user.username = self.validated_data['name']
        # user.first_name = request.data.get('displayname')
        # user.last_name = request.data.get('displayname')
        user.save()
        # profile = user.profile
        #profile.name = self.validated_data['name']
        # profile.name = request.data.get('displayname')
        # if 'gender' in self.validated_data and self.validated_data['gender']:
        #     profile.gender = self.validated_data['gender']
        # profile.save()

# class ActiveUser(UserDetailsSerializer):
#     def active (self, request):

