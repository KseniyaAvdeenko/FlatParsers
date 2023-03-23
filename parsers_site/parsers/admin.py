from django.contrib import admin
from .models  import Flats


class FlatsAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'link',
        'city',
        'district',
        'micro_district',
        'street',
        'house_number',
        'rooms_quantity')
    # search_fields = ('city', 'district', 'micro_district', 'rooms_quantity',)
    # list_filter = ('city', 'district', 'micro_district', 'rooms_quantity',)


admin.site.register(Flats, FlatsAdmin)

