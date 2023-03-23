from django.forms import ModelForm, TextInput, NumberInput
from . models import Flats


class FlatForm(ModelForm):
    class Meta:
        model = Flats
        fields = ["city", "district", "rooms_quantity"]
        widgets = {
            "city": TextInput(attrs={
                'class': 'input__item',
                'placeholder': 'Введите город: например - г.Минск'
            }),
            "district": TextInput(attrs={
                'class': 'input__item',
                'placeholder': 'Введите район: например - Октябрьский район'
            }),
            "rooms_quantity": NumberInput(attrs={
                'class': 'input__select',
                'placeholder': 'Кол-во комнат'
            }),
        }