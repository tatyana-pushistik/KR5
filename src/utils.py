from src.hhApi import get_employers_data, get_vacancies
from src.config_bd_read import connect
import psycopg2

def create_db(name, params):
    """Создание базы данных и таблиц"""
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'SELECT pg_terminate_backend(pg_stat_activity.pid) '
                    f'FROM pg_stat_activity '
                    f'WHERE pg_stat_activity.datname = \'{name}\' '
                    f'AND pid <> pg_backend_pid();'
                    )
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        conn.close()

        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS employers '
                        f'(company_id int, company_name varchar(100), company_url varchar (100))')
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS vacancies (company_name varchar (100), job_title varchar(100), '
                        f'link_to_vacancy varchar(100), salary_from int, currency varchar(10), '
                        f'description text, requirement text)')
        conn.commit()
        conn.close()

        print("База данных и таблицы успешно созданы.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")




def insert_data(conn, vacancies):
    """Сохранение данных о компаниях и вакансиях"""

    try:
        with conn.cursor() as cur:
            for record in vacancies:
                cur.execute(
                    """
                    INSERT INTO employers (company_id, company_name, company_url) VALUES (%s, %s, %s)
                    """,
                    (record['company_id'], record['company_name'], record['company_url']))

                cur.execute(
                    """
                    INSERT INTO vacancies (company_name, job_title, link_to_vacancy, salary_from, currency, description, requirement)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (record['company_name'], record['job_title'], record['link_to_vacancy'],
                     record['salary_from'], record['currency'], record['description'], record['requirement']))
        conn.commit()
    except Exception as e:
        print(f"Произошла ошибка при вставке данных: {e}")


