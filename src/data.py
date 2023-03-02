class Flat:
    def __init__(self, link, reference=None, price=None, title=None, description=None, date=None, square=None,
                 city=None, street=None, house_number=None, district=None, micro_district=None, house_year=None,
                 rooms_quantity=None, images=[]):
        self.link = link
        self.reference = reference
        self.price = price
        self.title = title
        self.description = description
        self.date = date
        self.square = square
        self.city = city
        self.street = street
        self.house_number = house_number
        self.district = district
        self.micro_district = micro_district
        self.house_year = house_year
        self.rooms_quantity = rooms_quantity
        self.images = images
        # self.seller_phone = seller_phone
