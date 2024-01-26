# Домашнее задание №4 

В этом репозитории представлен сайт-анкета с опросом на знание диалектизмов.

## Как запустить сайт с анкетой:

1. Склонировать репозиторий и перейти в папку flask_poll:

```bash
$ git clone git@github.com:afkhabirzyanova/flask_poll.git
$ cd flask_poll
```

2. Создать новое виртуальное окружение (приведен пример для miniconda) и уставновить все необходимые зависимости из requirements.txt:
```bash
$ conda create --name [new_env] python=3.11
$ conda activate [new_env]
(new_env)$ pip install -r requirements.txt
```

3. Для запуска сайта выполнить команду:
```bash
(new_env)$ python app.py
```

4. Перейти на страницу  http://127.0.0.1:5000.

