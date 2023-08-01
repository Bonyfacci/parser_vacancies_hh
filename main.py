import textwrap
from random import shuffle

from src.db_manager import DBManager
from src.utils import WorkToUser
from src.work_file import ReadWriteToJSON


def get_user(player: WorkToUser):
    """
    Выполняет запрос пользователя
    """
    player.choice_site()  # выбор ресурса
    player.get_request()  # запрос
    player.choice_city()  # Выбор региона для поиска вакансий
    player.quantity_vacancies()  # Количество вакансий

    print(f'\n{player}')  # Показывает запрос

    player.work_api()


def top_10_vacancies():
    """
    Выбирает десять вакансий, которые понравились пользователю
    """
    total_vacancies = ReadWriteToJSON.read_json()
    shuffle(total_vacancies)
    top_vacancies = []
    for vacancy in total_vacancies:
        print(f"\nНазвание компании - {vacancy['company']}"
              f"\nНазвание вакансии - {vacancy['title']}"
              f"\nГород - {vacancy['city']}"
              f"\n{vacancy['salary']}"
              f"\nТребования: {textwrap.fill(vacancy['requirements'], 75)}")
        while True:
            try:
                choice_user = int(input('\n1 - Да'
                                        '\n2 - Нет'
                                        '\nНравится текущая вакансия? '))
                if choice_user == 1:
                    top_vacancies.append(vacancy)
                    break
                elif choice_user == 2:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Некорректный ввод")
        if len(top_vacancies) <= 10:
            continue
        else:
            break
    ReadWriteToJSON.write_json(top_vacancies, file_name='top_vacancies.json',)


def work_db():
    """
    Выполняет работу с базой данных с помощью класса DBManager
    """
    work_list = ['Получить список всех компаний и количество вакансий у каждой компании',
                 'Получить список всех вакансий с указанием названия компании,'
                 '\nназвания вакансии и зарплаты и ссылки на вакансию',
                 'Получить среднюю зарплату по вакансиям',
                 'Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям',
                 'Получает список всех вакансий, в названии которых содержатся переданные в метод слова,'
                 '\nнапример "python"',
                 'Вывести понравившиеся вакансии']
    while True:
        try:
            choice_user = int(input(
                    f'\n1 - {work_list[0]}'
                    f'\n2 - {work_list[1]}'
                    f'\n3 - {work_list[2]}'
                    f'\n4 - {work_list[3]}'
                    f'\n5 - {work_list[4]}'
                    f'\n6 - {work_list[5]}'
                    f'\n0 - Завершить работу программы'
                    f'\nВыбирите, что Вы хотите вывести на экран: '))
            if choice_user in [1, 2, 3, 4, 5, 6]:
                if choice_user == 1:
                    DBManager.get_companies_and_vacancies_count('hh_vacancies', 'vacancies')
                elif choice_user == 2:
                    user_query = input('Введите название компании: ')
                    DBManager.get_all_vacancies('hh_vacancies', 'vacancies', user_query)
                elif choice_user == 3:
                    DBManager.get_avg_salary('hh_vacancies', 'vacancies')
                elif choice_user == 4:
                    DBManager.get_vacancies_with_higher_salary('hh_vacancies', 'vacancies')
                elif choice_user == 5:
                    user_query = input('Введите ключевое слово для запроса: ')
                    DBManager.get_vacancies_with_keyword('hh_vacancies', 'vacancies', user_query)
                elif choice_user == 6:
                    DBManager.get_top10_vacancies('hh_vacancies', 'top_vacancies')
            elif choice_user == 0:
                break
            else:
                raise ValueError
        except ValueError:
            print("\nНекорректный ввод")


def main():
    """
    Выполняет работу программы
    """

    while input('Нажмите Enter, чтобы начать: ') != '':
        continue

    # Очищаем файлы
    f = open('vacancies.json', 'w')
    f.close()
    f = open('top_vacancies.json', 'w')
    f.close()

    # Создаем базу данных
    DBManager.create_db('hh_vacancies')

    print('\nПриветствую Вас! Подготовим Ваш запрос по поиску вакансий.')

    player = WorkToUser()

    get_user(player)

    print('\nТеперь выбирем топ 10 вакансий, которые Вам нравятся.')
    top_10_vacancies()

    # Сохраняем вакансии в базе данных
    DBManager.save_data_to_database(ReadWriteToJSON.read_json('vacancies.json'), 'hh_vacancies', 'vacancies')
    DBManager.save_data_to_database(ReadWriteToJSON.read_json('top_vacancies.json'), 'hh_vacancies', 'top_vacancies')

    # Работа с классом DBManager
    work_db()


if __name__ == '__main__':
    main()
