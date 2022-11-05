from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['files'] = forms.FileField(required = False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean(self):
        files = self.files.getlist('files')
        for f in files:
            if f.name.split('.')[1] not in ['gif', 'jpeg', 'png', 'jpg', 'svg', 'mp4']:
                raise ValidationError(f'Формат {f.name.split(".")[1]} не поддерживается сервисом. Поддерживаемые разрешения: gif, jpeg, png, jpg, svg, mp4')
        return self.cleaned_data

    class Meta:
        model = Post
        fields = ['text', 'title',  'category']
        widgets = {'author': forms.HiddenInput()}
