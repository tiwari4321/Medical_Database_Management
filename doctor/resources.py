from import_export import resources
from .models import DiseaseDetails


class diseaseResources(resources.ModelResource):
    class Meta:
        model = DiseaseDetails
        field = '__all__'
        exclude = ['date', 'patient']