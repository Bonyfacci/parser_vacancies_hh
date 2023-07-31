from typing import Any

import psycopg2

from src.config import config


class DBManager:

    @staticmethod
    def create_db(database_name: str, params=config()):
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f'DROP DATABASE {database_name}')
        except Exception:
            pass

        try:
            cur.execute(f'CREATE DATABASE {database_name}')
        except Exception:
            pass

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

    @staticmethod
    def save_data_to_database(data: list[dict[str, Any]], database_name: str, table_name: str, params=config()) -> None:
        """Сохранение данных о вакансиях в базу данных"""

        conn = psycopg2.connect(dbname=database_name, **params)

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
    def get_all_vacancies(database_name: str, table_name, params=config()):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where company='МФТИ' "

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
    def get_avg_salary(database_name: str, table_name, params=config()):
        """
        Получает среднюю зарплату по вакансиям
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select round(avg(salary)) from {table_name} "

            cursor.execute(postgresql_select_query)
            total_vacancies = cursor.fetchall()

            for row in total_vacancies:
                print(f'\nСредняя зарплата по вакансиям - {row[0]}')

            cursor.close()
            connection.close()
        except Exception as error:
            print('Ошибка при работе PostgreSQL', error)

    @staticmethod
    def get_vacancies_with_higher_salary(database_name: str, table_name, params=config()):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where salary > (select avg(salary) from vacancies) "

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
    def get_vacancies_with_keyword(database_name: str, table_name, params=config()):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например 'python'
        """
        try:
            connection = psycopg2.connect(dbname=database_name, **params)
            cursor = connection.cursor()
            postgresql_select_query = f" select * from {table_name} where title_vacancies LIKE '%Junior%' "

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
