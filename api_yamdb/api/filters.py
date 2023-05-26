import django_filters as filters
from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """
    Add filters to Titles url query params for:
    category, genre, name, year.
    """
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    year = filters.NumberFilter(field_name='year', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = '__all__'
