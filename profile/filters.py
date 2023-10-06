import django_filters
from django import forms

from board.models import Response, Category


class ResponseFilter(django_filters.FilterSet):
    acceptResponse = django_filters.BooleanFilter(
        field_name='acceptResponse',
        label='Принятые / не принятые',
    )
    timeResponse = django_filters.DateFilter(
        field_name='timeResponse',
        label='Создан позже чем',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY', 'class': "col form-control border-right"
                   }),
        input_formats=['%d-%m-%Y', '%d-%m', '%m', '%d', '%m-%Y', '%Y-%m-%d', '%Y-%m', '%m-%d', '%d.%m.%Y']
    )
    responsePost__title = django_filters.CharFilter(
        field_name='responsePost__title',
        label='Заголовок новости',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': "col form-control border-right",
        }),
    )
    responsePost__text = django_filters.CharFilter(
        field_name='responsePost__textPost',
        label='Текст новости',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'class': "col form-control border-right",
        }),
    )
    responsePost__postCategory = django_filters.ModelChoiceFilter(
        field_name='responsePost__category',
        label='Категория',
        lookup_expr='exact',
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': "col form-control border-right selectpicker",
        }),
    )

    class Meta:
        model = Response
        fields = ['timeResponse', 'responsePost__title', 'responsePost__text', 'responsePost__postCategory']