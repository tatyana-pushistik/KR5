import psycopg2
from DBManager import DBManager
from src.config_bd_read import connect
from utils import create_db, insert_data
from hhApi import get_employers_data, get_vacancies

params = connect()

data = get_employers_data()
vacancies = get_vacancies(data)

conn = psycopg2.connect(dbname='vacancies', **params)


create_db('vacancies', params)
insert_data(conn, vacancies)


def main():
    db_manager = DBManager("vacancies", connect())
    while True:
        print(f'Выберите запрос либо введите слово "стоп": \n'
              f'1 - Список компаний и количество вакансий\n'
              f'2 - Cписок вакансий с указанием названия компании, названия вакансии и зарплаты\n'
              f'3 - Средняя зарплата по вакансиям\n'
              f'4 - Список вакансий, у которых зарплата выше средней\n'
              f'5 - Список вакансий, в названии которых содержатся запрашиваемое слово\n')
        user_request = input()
        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список компаний и количество вакансий: {companies_vacancies_count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print(f"Cписок вакансий с указанием названия компании, вакансии и зарплаты: "
                  f"{vacancy_list}")
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплату по вакансиям: {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(f"Список вакансий, у которых зарплата выше средней: "
                  f"{vacancies_with_higher_salary}")
        elif user_request == '5':
            user_input = input(f'Введите слово: ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"список вакансий, в названии которых содержатся {user_input}: {vacancies_with_keyword}")
        elif user_request == 'стоп':
            break
        else:
            print(f"Введён неверный запрос")


if __name__ == "__main__":
    main()