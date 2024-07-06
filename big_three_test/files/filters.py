from django_filters import rest_framework as filters

from files.models import File


class FileFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(
        field_name='created', lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created', lookup_expr='lte'
    )

    class Meta:
        model = File
        fields = ['created_after', 'created_before']
