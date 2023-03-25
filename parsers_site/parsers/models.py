from django.db import models


# Create your models here.
class Flats(models.Model):
    reference = models.CharField('Ресурс', max_length=30)
    link = models.CharField('Ссылка', unique=True, max_length=300)
    title = models.CharField('Название', max_length=1000, blank=True, null=True)
    price = models.IntegerField('Цена', blank=True, null=True)
    price_for_meter = models.IntegerField('Цена за кв.м.', blank=True, null=True)
    seller_phone = models.CharField('Номер продавца', max_length=30, blank=True, null=True)
    update_date = models.DateTimeField('Дата объявления', blank=True, null=True)
    description = models.CharField('Описание', max_length=10000, blank=True, null=True)
    square = models.FloatField('Площадь', blank=True, null=True)
    city = models.CharField('Населенный пункт', max_length=30, blank=True, null=True)
    street = models.CharField('Улица', max_length=500, blank=True, null=True)
    house_number = models.CharField('Номер дома', max_length=500, blank=True, null=True)
    district = models.CharField('Район', max_length=100, blank=True, null=True)
    micro_district = models.CharField('Микрорайон', max_length=500, blank=True, null=True)
    house_year = models.IntegerField('Год постройки', blank=True, null=True)
    rooms_quantity = models.IntegerField('Количество комнат', blank=True, null=True)
    photo_links = models.TextField('Фото')
    is_tg_posted = models.BooleanField('Размещено в ТГ', default=False)
    is_archived = models.BooleanField('Архивное', default=False)

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        ordering = ('id',)
        db_table = 'flats'
