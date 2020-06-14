from django import forms
from .models import Upload


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file1','file2']
        labels = {
            'file1': 'First File',
            'file2': 'Second File'
        }