from django_filters import rest_framework as filters
from .models import News


class NewsFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug',)
    heading = filters.CharFilter(field_name='heading',
                                 lookup_expr='contains',)
    date = filters.DateFilter(field_name='pub_date__date',
                              lookup_expr='contains',)

    class Meta:
        model = News
        fields = ['date', 'category', 'heading']
