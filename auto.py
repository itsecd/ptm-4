import os
import time
from typing import NoReturn

from rich import print
from rich.console import Console


console = Console()


def auto() -> NoReturn:
    """
    Проводит первоначальную настройку бота, включая создание директории и запись токена.
    Если директория уже существует или токен уже записан, пропускает соответствующие шаги.
    """
    print('Made by rus152')
    print('Файл токена не найден. Начинается первоначальная настройка')

    turnoff_path = os.path.join(os.getenv('APPDATA'), 'TurnOffBot')
    try:
        os.mkdir(turnoff_path)
    except (IOError, Exception):
        print()

    token_count: int = 0
    entered_token = ''
    while token_count < 3:
        print('Введете свой токен. (Взять токен для своего бота можно у официального бота BotFather)')
        entered_token: str = input()
        print('')
        print(
            f'Ваш токен: {entered_token}? Это верно? (Для избежания дальнейших проблем с запуском, удостоверьтесь, '
            f'что токен введён правильно) \n [Да/Нет]')

        confirmation_count: int = 0
        while confirmation_count < 2:
            user_confirmation: str = input()
            if user_confirmation.lower() in ['да', 'нет']:
                if user_confirmation.lower() == 'да':
                    token_count += 3
                    break
                else:
                    print('')
                    break
            else:
                print('Введите (Да) или (Нет)')

    with open(os.path.join(turnoff_path, 'token'), 'w') as f:
        f.write(entered_token)

    print('Первоначальная настройка завершена.')
    time.sleep(5)
    console.clear()
