import psycopg2
from src.creds import USER, PASSWORD, HOST, DATABASE

'''for tg_bot'''


class UserQuery:
    def create_user_query_table(self):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_query
                    (id SERIAL NOT NULL PRIMARY KEY,
                    user_id CHARACTER VARYING(50) UNIQUE,
                    username CHARACTER VARYING(50),
                    selected_city CHARACTER VARYING(50),
                    selected_district CHARACTER VARYING(50),
                    selected_rooms INTEGER,
                    selected_query CHARACTER VARYING(200)
                    )
                    ''')

    def insert_userid_username(self, user_query):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO user_query (user_id, username) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE 
                SET username = EXCLUDED.username;'''
                data = (user_query['user_id'], user_query['username'])
                cursor.execute(sql, data)

    def insert_selected_city(self, user_query):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO user_query (user_id, username, selected_city) VALUES (%s, %s, %s) 
                ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username, selected_city = EXCLUDED.selected_city'''
                data = (user_query['user_id'], user_query['username'], user_query['selected_city'])
                cursor.execute(sql, data)

    def insert_selected_district(self, user_query):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO user_query (user_id, username, selected_city, selected_district) 
                VALUES (%s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET username = EXCLUDED.username, 
                selected_city = EXCLUDED.selected_city, selected_district = EXCLUDED.selected_district'''
                data = (user_query['user_id'], user_query['username'], user_query['selected_city'],
                        user_query['selected_district'])
                cursor.execute(sql, data)

    def insert_selected_rooms(self, user_query):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO user_query (user_id,  username, selected_city, selected_district, 
                selected_rooms) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id)
                 DO UPDATE SET username = EXCLUDED.username, selected_city = EXCLUDED.selected_city,
                  selected_district = EXCLUDED.selected_district, selected_rooms = EXCLUDED.selected_rooms'''
                data = (user_query['user_id'], user_query['username'], user_query['selected_city'],
                        user_query['selected_district'], user_query['selected_rooms'])
                cursor.execute(sql, data)

    def insert_selected_query(self, user_query):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO user_query (user_id,  username, selected_city, selected_district, selected_rooms,
                 selected_query) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (user_id) 
                 DO UPDATE SET username = EXCLUDED.username, selected_city = EXCLUDED.selected_city, 
                 selected_district = EXCLUDED.selected_district, selected_rooms = EXCLUDED.selected_rooms, 
                 selected_query = EXCLUDED.selected_query'''
                data = (user_query['user_id'], user_query['username'], user_query['selected_city'],
                        user_query['selected_district'], user_query['selected_rooms'], user_query['selected_query'])
                cursor.execute(sql, data)

    def show_user_query(self, user_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT * FROM user_query WHERE user_id = %s''', (user_id,))
                return cursor.fetchall()


def show_flats_criteria(query, data):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, data)
            return cursor.fetchall()


def get_cities():
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT city FROM flats GROUP BY city
            ''')
            return cursor.fetchall()


def get_districts():
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT district FROM flats WHERE (city = 'г.Минск' OR city = 'Минск') GROUP BY district''')
            return cursor.fetchall()


def get_rooms_by_district(district):
    with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT rooms_quantity FROM flats WHERE (city = 'г.Минск' OR city = 'Минск')
             and district = %s GROUP BY rooms_quantity ''', (district,))
            return cursor.fetchall()
