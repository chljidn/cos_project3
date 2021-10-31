from common.models import Qa
from django_filters import rest_framework as filters

class QaFilter(filters.FilterSet):
    class Meta:
        model = Qa
        fields = ['id', 'postname', 'content']