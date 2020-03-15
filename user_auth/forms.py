from django import forms
from allauth.account.adapter import get_adapter
# from user_profile.models import Profile

class SignupForm(forms.Form):
    
    name = forms.CharField(max_length=100)
    # gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES,
    #                            required=False)
    
    def signup(self, request, user):
        adapter = get_adapter()
        username = adapter.generate_unique_username([self.cleaned_data['name']])
        user.username = username
        user.save()
        # profile = user.profile
        # profile.name = self.cleaned_data['name']
        # if 'gender' in self.cleaned_data and self.cleaned_data['gender']:
        #     profile.gender = self.cleaned_data['gender']
        # profile.save()
    
