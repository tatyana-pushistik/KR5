from src.hhApi import get_employers_data, get_vacancies
from src.config_bd_read import config
import os
from config import ROOT_DIR
import psycopg2

params_file_name = os.path.join(ROOT_DIR, 'database.ini')

params = config(params_file_name)

def create_db(name):
    """Создание базы данных и таблиц"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {name}")
    cur.execute(f"CREATE DATABASE {name}")

    cur.close()
    conn.close()


def create_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **params)

    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE employers (
        company_id INTEGER PRIMARY KEY,
        company_name VARCHAR(100) UNIQUE NOT NULL
        )
        """)

        cur.execute("""CREATE TABLE vacancies (
        id_vac INTEGER PRIMARY KEY,
        job_title VARCHAR(100) NOT NULL,
        link_to_vacancy VARCHAR(100),
        salary_from INTEGER,
        salary_to INTEGER,
        company_id INTEGER REFERENCES employers (company_id),
        city VARCHAR(100),
        description VARCHAR(255)
        )
        """)

    conn.close()


def insert_data(db_name, vacancies, data):
    """Сохранение данных о компаниях и вакансиях"""
    conn = psycopg2.connect(dbname=db_name, **params)

    try:

        with conn.cursor() as cur:
            conn.autocommit = True
            for record in data:
                cur.execute("INSERT INTO employers VALUES (%s, %s)",
                            (record["company_id"], record["company_name"]))

            for record in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies ( id_vac, job_title, link_to_vacancy, salary_from, salary_to, company_id, city, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s )
                    """,
                    ( record['id_vac'], record['job_title'], record['link_to_vacancy'],
                     record['salary_from'], record['salary_to'], record['company_id'], record['city'], record['description']))


    except Exception as e:
        print(f"Произошла ошибка при вставке данных: {e}")
