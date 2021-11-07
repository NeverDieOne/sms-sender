from unittest.mock import patch

from pydantic import BaseModel, ValidationError, constr
from quart import render_template, request, websocket
from quart_trio import QuartTrio

import smsc_api
from settings import settings

app = QuartTrio(__name__)


class Message(BaseModel):
    text: constr(min_length=1)


@app.route('/')
async def index():
    return await render_template('index.html')


@app.route('/send/', methods=['POST'])
async def send_message():
    try:
        form = await request.form
        message = Message(text=form['text'])

        with patch('smsc_api.request_smsc') as mock:
            mock.return_value = {
                'id': 244,
                'cnt': 1
            }
            response = await smsc_api.request_smsc(
                'POST', 'send', login=settings.login, password=settings.password,
                payload={'valid': 1, 'mes': message.text, 'phones': settings.phone}
            )
            print(response)

        return {'message': response}
    except ValidationError as error:
        errors = [e['msg'] for e in error.errors()]
        return {'errorMessage': errors}, 400
    except smsc_api.SmscApiError as e:
        return {'errorMessage': e.args}, 400


@app.websocket('/ws')
async def ws():
    while True:
        data = await websocket.receive()
        await websocket.send(f"echo {data}")


if __name__ == '__main__':
    app.run(port=5000)
