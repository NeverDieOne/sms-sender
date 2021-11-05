import json

import asks
import asyncclick as click
import trio
from environs import Env

env = Env()
env.read_env()


class SmscApiError(Exception):
    pass


async def request_smsc(
    http_method: str,
    api_method: str,
    *,
    login: str,
    password: str,
    payload: dict = {}
) -> dict:
    url = f'https://smsc.ru/sys/{api_method}'
    params = {
        'login': login,
        'psw': password,
        'fmt': 3,
        **payload
    }
    try:
        response = await asks.request(http_method, url, params=params)
        response_data = response.json()
        if 'error' in response_data:
            raise SmscApiError(response_data)
        return response_data
    except json.decoder.JSONDecodeError:
        raise SmscApiError('Non-exists API method')


@click.command()
@click.option('-l', '--login', help='Логин', default=env.str('LOGIN'))
@click.option('-pass', '--password', help='Пароль', default=env.str('PASSWORD'))
@click.option('-m', '--message', help='Текст сообщения', default=env.str('MESSAGE'))
@click.option('-p', '--phone', help='Номер телефона', default=env.str('PHONE'))
async def main(login, password, message, phone):
    message = await request_smsc(
        'POST', 'send', login=login, password=password,
        payload={'valid': 1, 'mes': message, 'phones': phone}
    )

    await trio.sleep(1)

    status = await request_smsc(
        'GET', 'status', login=login, password=password,
        payload={'phone': phone, 'id': message['id']}
    )
    print(status)


if __name__ == '__main__':
    main(_anyio_backend='trio')
