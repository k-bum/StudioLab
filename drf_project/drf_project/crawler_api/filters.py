import django_filters
from crawler.models import Image

class ImageFilter(django_filters.FilterSet):
    cut = django_filters.CharFilter(lookup_expr='exact')
    part = django_filters.CharFilter(lookup_expr='exact')
    direction = django_filters.CharFilter(lookup_expr='exact')
    pose = django_filters.CharFilter(lookup_expr='exact')
    is_head = django_filters.CharFilter(lookup_expr='exact')
    persom_count = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Image
        fields = ['cut', 'part', 'direction', 'pose', 'is_head', 'person_count']