import psycopg2
from src.creds import USER, PASSWORD, HOST, DATABASE

FLATS_TABLE = 'flats'


def create_flats_table():
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS flats
                (id SERIAL NOT NULL PRIMARY KEY,
                reference VARCHAR(30),
                link CHARACTER VARYING(300) UNIQUE,
                title CHARACTER VARYING(1000),
                price INTEGER,
                update_date TIMESTAMP WITH TIME ZONE,
                description CHARACTER VARYING(10000), 
                square REAL, 
                city CHARACTER VARYING(50),
                street CHARACTER VARYING(50),
                house_number CHARACTER VARYING(50),
                district CHARACTER VARYING(50),
                micro_district CHARACTER VARYING(70),
                house_year INTEGER,
                rooms_quantity INTEGER)
                ''')


def insert_flat(flat):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO flats (reference, link, title, price, update_date, description, square, city,
             street, house_number, district, micro_district, house_year, rooms_quantity, seller_phone, photo_links)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON CONFLICT (link) DO UPDATE
              SET
              link = EXCLUDED.link,
              price = EXCLUDED.price,
              title = EXCLUDED.title,
              description = EXCLUDED.description,
              update_date = EXCLUDED.update_date,
              square = EXCLUDED.square,
              city = EXCLUDED.city,
              street = EXCLUDED.street,
              house_number = EXCLUDED.house_number,
              district = EXCLUDED.district,
              micro_district = EXCLUDED.micro_district,
              house_year = EXCLUDED.house_year,
              rooms_quantity = EXCLUDED.rooms_quantity,
              seller_phone = EXCLUDED.seller_phone,
              photo_links = EXCLUDED.photo_links
            ''', (flat.reference, flat.link, flat.title, flat.price, flat.date, flat.description,
                  flat.square, flat.city, flat.street, flat.house_number, flat.district,
                  flat.micro_district, flat.house_year, flat.rooms_quantity, flat.seller_phone, flat.images)
                           )


# create_flats_table()