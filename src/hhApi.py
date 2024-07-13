import requests

def get_employers_data():
    employer_data = {
        'Альфа - Банк': 80,
        # 'Яндекс': 1740,
        # 'ВТБ': 4181,
        # 'Tele2': 4219,
        # 'МТС': 3776,
        # 'Газпромбанк': 3388,
        # 'МегаФон': 3127,
        # 'X5 Group': 4233,
        # 'Сбербанк': 3529,
         'Аэрофлот': 1373
    }

    data_employers = []

    for company_name, company_id in employer_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
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
                company = item['employer']['name']
                company_url = item['employer']['url']
                job_title = item['name']
                link_to_vacancy = item['employer']['alternate_url']
                salary = item['salary']
                currency = ''
                salary_from = 0

                if salary:
                    salary_from = salary['from'] or 0
                    currency = salary['currency'] or ''

                description = item['snippet']['responsibility']
                requirement = item['snippet']['requirement']

                vacancies.append({
                    "company_id": company_id,
                    "company_name": company,
                    "company_url": company_url,
                    "job_title": job_title,
                    "link_to_vacancy": link_to_vacancy,
                    "salary_from": salary_from,
                    "currency": currency,
                    "description": description,
                    "requirement": requirement
                })
        else:
            print(f"Ошибка запроса API для компании  {company_data['company_name']}: {response.status_code}")

    return vacancies




