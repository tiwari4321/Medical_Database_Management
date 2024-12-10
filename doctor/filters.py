import django_filters
from django_filters import CharFilter, DateFilter, ChoiceFilter

from .models import *

class DiseaseFilter(django_filters.FilterSet):
    CHOICES = (
        ('ascending','Ascending'),
    ('descending','Descending')
    )
    name = CharFilter(label ='Diesease Name',field_name='name', lookup_expr='icontains')
    organ = CharFilter(label ='Organ',field_name='organ', lookup_expr='icontains')
    # ordering = ChoiceFilter(label='ordering',choices='CHOICES',method='filter_by_order')
    class Meta:
        model = DiseaseDetails
        fields = ['name','modality','diagonised','organ']

    def filter_by_order(self , queryset, name, value):
        expression='date' if value == 'ascending' else '-date'
        return queryset.order_by(expression)

class PatientFilter(django_filters.FilterSet):
    first_name = CharFilter(label ='Name',field_name='first_name', lookup_expr='icontains')
    class Meta:
        model=PatientProfile
        fields = ['first_name']
