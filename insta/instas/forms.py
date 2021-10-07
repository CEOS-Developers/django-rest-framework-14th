from django import forms
from .models import Photos, Videos

class UploadPhoto(forms.ModelForm):
    class Meta:
        model = Photos
        fileds = ('photo_id', 'photo_url')

    def __init__(self,*args,**kwargs):
        super(PostForm, self).__init__(*args,**kwargs)
        self.fields['photo_url'].required = False
