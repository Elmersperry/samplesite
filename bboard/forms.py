from django import forms
from django.contrib.auth.models import User
from .models import Bb

# class BbForm(forms.Form):
#     # author = forms.ModelChoiceField(queryset=User.objects.all(), label="Автор"),
#     title = forms.CharField(max_length=200, label="Заголовок")
#     content = forms.CharField(widget=forms.Textarea, label="Содержание обьявления ")
#     price = forms.FloatField(label="Цена")
#     image = forms.ImageField(required=False, label="Изображение")

class BbForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        author = kwargs.pop('author')
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = author
        self.fields['author'].disabled = True
        self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Bb
        fields = ('title', 'author', 'content', 'price', 'image')
        # fields = '__all__'
        # fields = ('title', 'content')
        # exclude = ('price', 'published')
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'price': 'Цена',
            'image': 'Изображение',
        }

class FilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all(), label="Автор", required=False)
    created_at = forms.DateField(label="Дата публикации",
                                 widget=forms.DateInput(attrs={'type': 'date'}),
                                 input_formats=['%Y-%m-%d'], required=False)