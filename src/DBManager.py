import psycopg2


class DBManager:
    def __init__(self, dbname, params):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список компаний и количество вакансий"""
        query = """
        SELECT company_name, 
        COUNT(*) FROM vacancies
        GROUP BY company_name
        """
        self.cur.execute(query)
        return {row[0]: row[1] for row in self.cur.fetchall()}

    def get_all_vacancies(self):
        """Получает список вакансий с указанием названия компании, вакансии и зарплаты и ссылку"""
        query = """
        SELECT job_title, company_name, salary_from, link_to_vacancy FROM vacancies
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату"""
        query = """
        SELECT AVG(salary_from) FROM vacancies
        """
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий, у которых зарплата выше средней"""
        query = """
        SELECT job_title, salary_from FROM vacancies
        WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий по фильтру"""
        query = """
                        SELECT * FROM vacancies
                        WHERE LOWER(job_title) LIKE %s
                        """
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()