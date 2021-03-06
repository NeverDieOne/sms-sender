# Программа для рассылки SMS-оповещений

Сервис для рассылки SMS-оповещений через API SMSC.

## Как установить

1. Создать новое виртуальное окружение

```console
python -m venv venv
```

2. Активировать виртуальное окружение

Если у вас MacOS/Linux
```console
. ./venv/bin/acitvate
```

Если у вас Windows
```console
venv/Scripts/acitvate
```

3. Установи зависимости

```console
python -r requirements.txt
```

4. Запустить программу

```console
python main.py
```

5. Перейти [на сайт](http://127.0.0.1:5000)

## Настройки окружения

```
LOGIN - логин от сервиса smsc
PASSWORD - пароль от сервиса smsc
MESSAGE - сообщение для отпавки [опционально]
PHONE - телефон для отправки/список телефонов через запятую
REDIS_URL - строка подключения к Redis
```

## Отправка сообщения из скрипта

Можно воспользоваться отдельным скриптом для отправки сообщения.

Сообщение и номер телефона будут взяты из переменных окружения или их можно задать через аргументы командной строки.

```console
python smsc_api.py
```

```console
python smsc_api.py -m "Привет" -p "89123456789"
```

Для вызова справки:
```console
python smsc_api.py -h
```

