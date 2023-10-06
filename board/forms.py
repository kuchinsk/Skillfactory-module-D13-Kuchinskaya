from urllib import request

from django.forms import ModelForm
from .models import Post, Response
from django import forms


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'textPost', 'img', 'video', 'file', 'category']
        labels = {
            'title': 'Заголовок',
            'textPost': 'Текст объявления',
            'img': 'Изображение',
            'video': 'Видео',
            'file': 'Файл',
            'category': 'Категория'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок'
            }),
            'textPost': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст вашего объявления'
            }),
            # 'img': forms.ImageField(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Прикрепите изображения'
            # }),
            # 'video': forms.FileInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Прикрепите видео'
            # }),
            # 'file': forms.FileInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Прикрепите файлы'
            # }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['textResponse']
        widgets = {
            'textResponse': forms.Textarea(attrs={'class': 'form-control'}),
        }