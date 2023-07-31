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
    DBManager.get_companies_and_vacancies_count('hh_vacancies', 'vacancies')
    DBManager.get_all_vacancies('hh_vacancies', 'vacancies')
    DBManager.get_avg_salary('hh_vacancies', 'vacancies')
    DBManager.get_vacancies_with_higher_salary('hh_vacancies', 'vacancies')
    DBManager.get_vacancies_with_keyword('hh_vacancies', 'vacancies')


def main():

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
