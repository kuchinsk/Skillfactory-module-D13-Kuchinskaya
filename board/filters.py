import django_filters
from django import forms

from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        label='Заголовок',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': "col form-control border-right",
            'placeholder': "Введите заголовок"}),
    )
    author = django_filters.CharFilter(
        field_name='author__authorUser__username',
        label='Автор',
        lookup_expr='iregex',
        widget=forms.TextInput(attrs={
            'class': "col form-control border-right",
            'placeholder': "Имя автора"}),
    )
    category = django_filters.ModelChoiceFilter(
        field_name='category__name',
        # choices='TYPE_CHOICES',
        label='Категория',
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': "col form-control border-right selectpicker",
            'placeholder': "Выберете категорию"}),
    )


    class Meta:
        model = Post
        fields = ['title', 'author', 'category']


