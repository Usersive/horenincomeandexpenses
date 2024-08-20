
# accounts/forms.py
from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    profile_image= forms.ImageField(required=False, error_messages={'invalid':("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['name', 'address', 'phone_number', 'gender', 'profile_image', 'profile_details',]
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
        
