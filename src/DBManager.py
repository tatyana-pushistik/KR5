import psycopg2
from src.config_bd_read import config
import os
from config import ROOT_DIR
import json

params_file_name = os.path.join(ROOT_DIR, 'database.ini')

params = config(params_file_name)


class DBManager:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """1 - Список компаний и количество вакансий"""
        query = """
            SELECT employers.company_name, COUNT(vacancies.company_id) AS count
            FROM vacancies
            JOIN employers ON vacancies.company_id = employers.company_id
            GROUP BY employers.company_name 
        """
        self.cur.execute(query)
        return {row[0]: row[1] for row in self.cur.fetchall()}

    def get_all_vacancies(self):
        """2 - Cписок вакансий с указанием названия компании, названия вакансии и зарплаты"""
        query = """
            SELECT employers.company_name, vacancies.job_title, vacancies.salary_from, vacancies.salary_to
            FROM vacancies
            JOIN employers ON vacancies.company_id = employers.company_id;
        """
        self.cur.execute(query)
        return self.cur.fetchall()


    def get_avg_salary(self):
        """3 - Средняя зарплата по вакансиям"""
        query = """
            SELECT AVG(salary_from) FROM vacancies
        """
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """4 - Список вакансий, у которых зарплата выше средней"""
        query = """
            SELECT employers.company_name, vacancies.job_title, vacancies.salary_from, vacancies.salary_to
            FROM vacancies
            JOIN employers ON vacancies.company_id = employers.company_id
            WHERE vacancies.salary_from > (SELECT AVG(salary_from) FROM vacancies);
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """5 - Список вакансий, в названии которых содержатся запрашиваемое слово"""
        query = """
            SELECT employers.company_name, vacancies.job_title, vacancies.salary_from, vacancies.salary_to
            FROM vacancies
            JOIN employers ON vacancies.company_id = employers.company_id
            WHERE vacancies.job_title LIKE %s
        """
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()