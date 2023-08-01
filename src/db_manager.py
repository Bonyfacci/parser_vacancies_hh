from typing import Any

import psycopg2

from src.config import config
from src.work_file import ReadWriteToSQL


class DBManager:

    @staticmethod
    def create_db(database_name: str, params=config()) -> None:
        """
        Создаёт базу данных и таблицы
        :param database_name: str
        :param params: dict
        :return: None
        """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f'DROP DATABASE {database_name}')
            ReadWriteToSQL.add_info(f'\nDROP DATABASE {database_name};\n')
        except Exception:
            pass

        try:
            cur.execute(f'CREATE DATABASE {database_name}')
            ReadWriteToSQL.add_info(f'\nCREATE DATABASE {database_name};\n')
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)
        cur.close()
        conn.close()

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        company VARCHAR(255) NOT NULL,
                        title_vacancies VARCHAR(255) NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        salary INTEGER,
                        url TEXT
                    )
                    """
                )

            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE top_vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        company VARCHAR(255) NOT NULL,
                        title_vacancies VARCHAR(255) NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        salary INTEGER,
                        url TEXT
                    )
                    """
                )

        conn.close()
        ReadWriteToSQL.add_info(f'\nCREATE TABLE vacancies ('
                                f'\n    vacancy_id SERIAL PRIMARY KEY,'
                                f'\n    company VARCHAR(255) NOT NULL,'
                                f'\n    title_vacancies VARCHAR(255) NOT NULL,'
                                f'\n    city VARCHAR(255) NOT NULL,'
                                f'\n    salary INTEGER,'
                                f'\n    url TEXT'
                                f'\n);\n'
                                f'\nCREATE TABLE top_vacancies ('
                                f'\n    vacancy_id SERIAL PRIMARY KEY,'
                                f'\n    company VARCHAR(255) NOT NULL,'
                                f'\n    title_vacancies VARCHAR(255) NOT NULL,'
                                f'\n    city VARCHAR(255) NOT NULL,'
                                f'\n    salary INTEGER,'
                                f'\n    url TEXT'
                                f'\n);\n')

    @staticmethod
    def save_data_to_database(data: list[dict[str, Any]], database_name: str, table_name: str, params=config()) -> None:
        """Сохранение данных о вакансиях в базу данных"""

        conn = psycopg2.connect(dbname=database_name, **params)

        info_vacancies = ''

        with conn.cursor() as cur:
            for vacancy in data:
                cur.execute(
                    f"""
                    INSERT INTO {table_name} (company, title_vacancies, city, salary, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy['company'], vacancy['title'], vacancy['city'],
                     vacancy['salary_int'], vacancy['url'])
                )
                if len(info_vacancies) < 1:
                    info_vacancies += f"{vacancy['company']}, {vacancy['title']}, {vacancy['city']}, " \
                                      f"{vacancy['salary_int']}, {vacancy['url']}\n"
                else:
                    info_vacancies += f"        {vacancy['company']}, {vacancy['title']}, {vacancy['city']}, " \
                                      f"{vacancy['salary_int']}, {vacancy['url']}\n"

        ReadWriteToSQL.add_info(f"\nINSERT INTO {table_name} (company, title_vacancies, city, salary, url)"
                                f"\nVALUES ({info_vacancies});\n")
        conn.commit()
        conn.close()

    @staticmethod
    def get_companies_and_vacancies_count(database_name: str, table_name, params=config()):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f'select company, count(*) from {table_name} group by company'
            ReadWriteToSQL.add_info(f'\nSELECT company, count(*)'
                                    f'\nFROM {table_name}'
                                    f'\nGROUP BY company;\n')

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            print(f'Компания - количество вакансий')
            for row in total_vacancies:
                print(f'{row[0]} - {row[1]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_all_vacancies(database_name: str, table_name: str, user_query: str, params=config()):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where company='{user_query}' "
            ReadWriteToSQL.add_info(f"\nSELECT *"
                                    f"\nFROM {table_name}"
                                    f"\nWHERE company='{user_query}';\n")

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nКомпания - {row[1]},'
                      f'\nВакансия - {row[2]},'
                      f'\nЗарплата - {row[4]},'
                      f'\nСсылка на вакансию - {row[5]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_avg_salary(database_name: str, table_name: str, params=config()):
        """
        Получает среднюю зарплату по вакансиям
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select round(avg(salary)) from {table_name} "
            ReadWriteToSQL.add_info(f"\nSELECT round(AVG(salary))"
                                    f"\nfrom {table_name};\n")

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nСредняя зарплата по вакансиям - {row[0]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_vacancies_with_higher_salary(database_name: str, table_name: str, params=config()):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where salary > (select avg(salary) from vacancies) "
            ReadWriteToSQL.add_info(f"\nSELECT *"
                                    f"\nFROM {table_name}"
                                    f"\nWHERE salary > (SELECT AVG(salary)"
                                    f"\n                    FROM vacancies);\n")

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nКомпания - {row[1]},'
                      f'\nВакансия - {row[2]},'
                      f'\nЗарплата - {row[4]},'
                      f'\nСсылка на вакансию - {row[5]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_vacancies_with_keyword(database_name: str, table_name: str, user_query: str, params=config()):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where title_vacancies LIKE '%{user_query}%' "
            ReadWriteToSQL.add_info(f"\nSELECT *"
                                    f"\nFROM {table_name}"
                                    f"\nWHERE title_vacancies LIKE '%{user_query}%';\n")

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nКомпания - {row[1]},'
                      f'\nВакансия - {row[2]},'
                      f'\nЗарплата - {row[4]},'
                      f'\nСсылка на вакансию - {row[5]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_top10_vacancies(database_name: str, table_name: str, params=config()):
        """
        Получает список всех вакансий, которые понравились пользователю
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} "
            ReadWriteToSQL.add_info(f"\nSELECT *"
                                    f"\nFROM {table_name};\n")

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nКомпания - {row[1]},'
                      f'\nВакансия - {row[2]},'
                      f'\nЗарплата - {row[4]},'
                      f'\nСсылка на вакансию - {row[5]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)
