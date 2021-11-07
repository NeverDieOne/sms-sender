import json
from unittest.mock import patch

import asks
import asyncclick as click

from settings import settings


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
@click.option('-l', '--login', help='Логин', default=settings.login)
@click.option('-pass', '--password', help='Пароль', default=settings.password)
@click.option('-m', '--message', help='Текст сообщения', default=settings.message)
@click.option('-p', '--phone', help='Номер телефона', default=settings.phone)
async def main(login, password, message, phone):
    with patch('__main__.request_smsc') as mock:
        mock.return_value = {
            'id': 244,
            'cnt': 1
        }
        message = await request_smsc(
            'POST', 'send', login=login, password=password,
            payload={'valid': 1, 'mes': message, 'phones': phone}
        )

        mock.return_value = {
            'status': 1,
            'last_date': '05.11.2021 15:08:20',
            'last_timestamp': 1636114100
        }
        status = await request_smsc(
            'GET', 'status', login=login, password=password,
            payload={'phone': phone, 'id': message['id']}
        )
        print(status)


if __name__ == '__main__':
    main(_anyio_backend='trio')
