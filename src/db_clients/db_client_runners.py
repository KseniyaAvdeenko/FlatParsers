import psycopg2
from src.creds import USER, PASSWORD, HOST, DATABASE

'''for is_posted_status'''


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


'''for is_archived_status'''


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
