import psycopg2
from DBManager import DBManager
from src.config_bd_read import config
from utils import create_db, create_tables, insert_data
from hhApi import get_employers_data, get_vacancies

db_name = "kr5vacancies"
create_db(db_name)
create_tables(db_name)

data = get_employers_data()
vacancies = get_vacancies(data)
insert_data(db_name, vacancies, data)


def main():
    db_manager = DBManager(db_name)
    while True:
        print(f'\n Выберите запрос либо введите слово "стоп": \n'
              f'1 - Список компаний и количество вакансий\n'
              f'2 - Cписок вакансий с указанием названия компании, названия вакансии и зарплаты\n'
              f'3 - Средняя зарплата по вакансиям\n'
              f'4 - Список вакансий, у которых зарплата выше средней\n'
              f'5 - Список вакансий, в названии которых содержатся запрашиваемое слово\n')
        user_request = input()

        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список компаний и количество вакансий:")
            for company, vacancies_count in companies_vacancies_count.items():
                print(f"{company} - {vacancies_count}")

        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print("Cписок вакансий с указанием названия компании, вакансии и зарплаты:")
            for vacancy in vacancy_list:
                print(f"{vacancy[0]} - \"{vacancy[1]}\" зп от {vacancy[2]} до {vacancy[3]}")

        elif user_request == '3':
            avg_salary = round(db_manager.get_avg_salary(), 2)
            print(f"Средняя зарплата по вакансиям: {avg_salary}")

        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(f"Список вакансий, у которых зарплата выше средней: ")
            for vacancy in vacancies_with_higher_salary:
                print(f"{vacancy[0]} - \"{vacancy[1]}\" зп от {vacancy[2]} до {vacancy[3]}")

        elif user_request == '5':
            user_input = input(f'Введите слово: ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"список вакансий, в названии которых содержатся слово \"{user_input}\":")
            for vacancy in vacancies_with_keyword:
                print(f"{vacancy[0]} - \"{vacancy[1]}\" зп от {vacancy[2]} до {vacancy[3]}")

        elif user_request == 'стоп':
            break
        else:
            print(f"Введён неверный запрос")


if __name__ == "__main__":
    main()