from typing import DefaultDict
import asks
import asyncclick as click
from environs import Env


env = Env()
env.read_env()


@click.command()
@click.option('-l', '--login', help='Логин', default=env.str('LOGIN'))
@click.option('-pass', '--password', help='Пароль', default=env.str('PASSWORD'))
@click.option('-m', '--message', help='Текст сообщения', default=env.str('MESSAGE'))
@click.option('-p', '--phone', help='Номер телефона', default=env.str('PHONE'))
async def main(login, password, message, phone):
    url = 'https://smsc.ru/sys/send.php'
    params = {
        'login': login,
        'psw': password,
        'phones': phone,
        'mes': message,
        'valid': 1
    }
    response = await asks.post(url, params=params)
    print(response)


if __name__ == '__main__':
    main(_anyio_backend='trio')
