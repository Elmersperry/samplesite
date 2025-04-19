from django import forms
from django.contrib.auth.models import User
from .models import Bb

class BbForm(forms.Form):
    title = forms.CharField(max_length=200, label="Заголовок")
    content = forms.CharField(widget=forms.Textarea, label="Содержание обьявления ")
    price = forms.FloatField(label="Цена")
    image = forms.ImageField(required=False, label="Изображение")

# class NewBbForm(forms.ModelForm):
#     class Meta:
#         model = Bb
#         fields = '__all__'
#         fields = ('title', 'content')
#         exclude = ('price', 'published')
#
#         labels = {
#             'title': 'Заголовок',
#             'content': 'Содержание'
#         }