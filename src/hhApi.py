import requests

def get_employers_data():
    employer_data = {
         'Альфа - Банк': 80,
         'Яндекс': 1740,
         'ВТБ': 4181,
         'Tele2': 4219,
         'МТС': 3776,
         'Газпромбанк': 3388,
         'МегаФон': 3127,
         'X5 Group': 4233,
         'Сбербанк': 3529,
         'Аэрофлот': 1373
    }

    data_employers = []

    for company_name, company_id in employer_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, 'company_name': company_name}
        data_employers.append(company_info)
    return data_employers


def get_vacancies(data):
    vacancies = []

    for company_data in data:
        company_id = company_data['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)

        if response.status_code == 200:
            vacancies_data = response.json()['items']

            for item in vacancies_data:
                company_id = item['employer']['id']
                id_vac = item['id']
                company_name = item['employer']['name']
                job_title = item['name']
                link_to_vacancy = item['employer']['alternate_url']
                salary = item['salary']
                city = item['area']['name']
                salary_from = 0
                salary_to = 0

                if salary:
                    salary_from = salary['from'] or 0
                    salary_to = salary['to'] or 0


                description = item['snippet']['responsibility']

                vacancies.append({
                    "company_id": company_id,
                    "id_vac": id_vac,
                    "company_name": company_name,
                    "job_title": job_title,
                    "link_to_vacancy": link_to_vacancy,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "city": city,
                    "description": description

                })
        else:
            print(f"Ошибка запроса API для компании  {company_data['company_name']}: {response.status_code}")

    return vacancies

# data = get_employers_data()
# data2 = get_vacancies(data)
# print(data2)

