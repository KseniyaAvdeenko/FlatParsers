from django.shortcuts import render
from django.db.models import OuterRef, Subquery

import datetime

from .models import Flats
from . forms import FlatForm


def flats_search(request):
    error = ''
    if request.method == 'POST':
        form = FlatForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['city']:
                city = form.cleaned_data['city'].title()
            else:
                city = ''
            if form.cleaned_data['district']:
                district = form.cleaned_data['district'].title()
            else:
                district = ''
            if form.cleaned_data['rooms_quantity']:
                rooms_quantity = [form.cleaned_data['rooms_quantity']]
            else:
                rooms_quantity = [1, 2, 3, 4, 5]

            flats = Flats.objects.filter(update_date__gte=datetime.datetime.today() - datetime.timedelta(days=3), is_archived=False,
                                         city__contains=city, district__contains=district, rooms_quantity__in=rooms_quantity).order_by('-date')

            return render(request, 'parsersapp/flats_list.html', {'flats': flats})
        else:
            error = 'Форма заполнена неверно'

    form = FlatForm()
    return render(request, 'parsersapp/searching.html', {'form': form}, {'error': error})
