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
                price_for_meter INTEGER,
                seller_phone CHARACTER VARYING(50),
                update_date TIMESTAMP WITH TIME ZONE,
                description CHARACTER VARYING(10000), 
                square REAL, 
                city CHARACTER VARYING(50),
                street CHARACTER VARYING(50),
                house_number CHARACTER VARYING(50),
                district CHARACTER VARYING(50),
                micro_district CHARACTER VARYING(70),
                house_year INTEGER,
                rooms_quantity INTEGER,
                photo_links TEXT,
                is_tg_posted BOOLEAN DEFAULT false,
                is_archived BOOLEAN DEFAULT false
                )
                ''')


# create_flats_table()

def create_flats_test_table():
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS flats_test
                (id SERIAL NOT NULL PRIMARY KEY,
                reference VARCHAR(30),
                link CHARACTER VARYING(300) UNIQUE,
                title CHARACTER VARYING(1000),
                price INTEGER,
                price_for_meter INTEGER,
                seller_phone CHARACTER VARYING(100),
                update_date TIMESTAMP WITH TIME ZONE,
                description CHARACTER VARYING(10000), 
                square REAL, 
                city CHARACTER VARYING(100),
                street CHARACTER VARYING(100),
                house_number CHARACTER VARYING(100),
                district CHARACTER VARYING(100),
                micro_district CHARACTER VARYING(70),
                house_year INTEGER,
                rooms_quantity INTEGER,
                photo_links TEXT,
                is_tg_posted BOOLEAN DEFAULT false,
                is_archived BOOLEAN DEFAULT false
                )
                ''')


# create_flats_test_table()


def insert_many(ready_flats):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            query = "INSERT INTO flats (reference, link, title, price, price_for_meter, update_date, description, " \
                    "square, city, street, house_number, district, micro_district, house_year, rooms_quantity, " \
                    "seller_phone, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
                    "ON CONFLICT (link) DO UPDATE SET link = EXCLUDED.link, price = EXCLUDED.price," \
                    " title = EXCLUDED.title, description = EXCLUDED.description, update_date = EXCLUDED.update_date, " \
                    "square = EXCLUDED.square, city = EXCLUDED.city, street = EXCLUDED.street, " \
                    "house_number = EXCLUDED.house_number, district = EXCLUDED.district, " \
                    "micro_district = EXCLUDED.micro_district, house_year = EXCLUDED.house_year, " \
                    "rooms_quantity = EXCLUDED.rooms_quantity, seller_phone = EXCLUDED.seller_phone, " \
                    "photo_links = EXCLUDED.photo_links, price_for_meter = EXCLUDED.price_for_meter "
            cursor.executemany(query, ready_flats)


def insert_flat(flat):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO flats_test (reference, link, title, price, update_date, 
            description, square, city, street, house_number, district, micro_district, house_year, rooms_quantity,
             seller_phone, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                  flat.micro_district, flat.house_year, flat.rooms_quantity, flat.seller_phone, ','.join(flat.images))
                           )


def get_all_not_posted_flats(parser_types):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    SELECT link, reference, price, title, description, update_date, photo_links, id FROM flats
                    WHERE (is_tg_posted = false) AND reference IN %(parser_types)s ORDER BY update_date DESC;
                ''', {'parser_types': tuple(parser_types)}
                           )
            return cursor.fetchall()


def update_is_posted_state(ids):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE flats SET is_tg_posted = true
                WHERE id = ANY(%s);
            ''', [ids, ]
                           )


def get_all_not_archived_flats():
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                    SELECT link, title, id FROM flats 
                    WHERE (is_archived = false);''', )

            return cursor.fetchall()


def update_is_archived_state(ids):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE flats SET is_archived = true
                WHERE id = ANY(%s);
            ''', [ids, ])
