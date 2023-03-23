from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
























# # from django_filters import rest_framework as filters
# from .models import Flats
# #
# # # CITIES = (
# # #     (0, 'г.Минск'),
# # #     (1, 'г.Витебск'),
# # #     (2, 'г.Гомель'),
# # #     (3, 'г.Могилев'),
# # #     (4, 'г.Брест'),
# # #     (4, 'г.Гродно'),
# # # )
# #
# #
# # class FlatsFilter(filters.FilterSet):
# #     # city = filters.CharFilter(field_name='city')
# #     # district = filters.CharFilter(field_name='district')
# #     # micro_district = filters.CharFilter(field_name='micro_district')
# #     rooms_quantity = filters.NumberFilter()
# #     # price = filters.NumberFilter()
# #
# #     class Meta:
# #         model = Flats
# #         fields = (
# #             # 'city',
# #             # 'district',
# #             # 'micro_district',
# #             'rooms_quantity',
# #             # 'price'
# #         )
#
#
# from django.http import QueryDict
# from url_filter.filtersets import ModelFilterSet
#
#
# class FlatFilterSet(ModelFilterSet):
#     class Meta(object):
#         model = Flats
#
# query = QueryDict('city=г.Минск&')
# fs = FlatFilterSet(data=query, queryset=Flats.objects.all())
# filtered_flats = fs.filter()