from src.utils import WorkToUser


def get_user(player: WorkToUser):
    """Выполняет запрос пользователя"""

    player.choice_site()  # выбор ресурса
    player.get_request()  # запрос
    player.choice_city()  # Выбор региона для поиска вакансий
    player.quantity_vacancies()  # Количество вакансий

    print(f'\n{player}')  # Показывает запрос

    player.work_api()


def main():

    while input('Нажмите Enter, чтобы начать: ') != '':
        continue

    # Очищаем файл
    f = open('vacancies.json', 'w')
    f.close()

    print('\nПриветствую Вас! Подготовим Ваш запрос по поиску вакансий.')

    player = WorkToUser()

    get_user(player)




if __name__ == '__main__':
    main()
