import asks
import asyncclick as click
from environs import Env
import trio


env = Env()
env.read_env()


async def send_message(login, password, phone, message):
    url = 'https://smsc.ru/sys/send.php'
    params = {
        'login': login,
        'psw': password,
        'phones': phone,
        'mes': message,
        'valid': 1,
        'fmt': 3,
    }
    response = await asks.post(url, params=params)
    return response.json()


async def get_status(login, password, phone, message_id):
    url = 'https://smsc.ru/sys/status.php'
    params = {
        'login': login,
        'psw': password,
        'phone': phone,
        'id': message_id,
        'fmt': 3
    }
    response = await asks.get(url, params=params)
    return response.json()


@click.command()
@click.option('-l', '--login', help='Логин', default=env.str('LOGIN'))
@click.option('-pass', '--password', help='Пароль', default=env.str('PASSWORD'))
@click.option('-m', '--message', help='Текст сообщения', default=env.str('MESSAGE'))
@click.option('-p', '--phone', help='Номер телефона', default=env.str('PHONE'))
async def main(login, password, message, phone):
    message = await send_message(login, password, phone, message)
    await trio.sleep(1)
    status = await get_status(login, password, phone, message['id'])
    print(status)


if __name__ == '__main__':
    main(_anyio_backend='trio')
