# MAU Schedule

<img alt="Static Badge" src="https://img.shields.io/badge/status-testing-blue" height="26">

--------------------


<a href="https://www.python.org/" style="text-decoration: none">
  <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&link=https://www.djangoproject.com/">
</a>
<a href="https://www.djangoproject.com/" style="text-decoration: none">
  <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
</a>
<a href="https://www.djangoproject.com/" style="text-decoration: none">
  <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</a>
<a href="https://www.djangoproject.com/" style="text-decoration: none">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
</a>
<a href="https://www.djangoproject.com/" style="text-decoration: none">
  <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
</a>
<a href="https://www.djangoproject.com/" style="text-decoration: none">
  <img alt="Celery" src="https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4">
</a>
<a href="https://developer.mozilla.org/en-US/docs/Web/HTML" style="text-decoration: none">
  <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white">
</a>
<a href="https://developer.mozilla.org/en-US/docs/Web/CSS" style="text-decoration: none">
  <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white">
</a>
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" style="text-decoration: none">
  <img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E">
</a>

Приложение представляет собой сайт-расписание для студентов Мурманского Арктического Университета (МАУ).

На [официальном сайте](https://www.mauniver.ru/student/timetable/new/) неудобно смотреть расписание, т. к. приходится совершать много действий для его просмотра, а именно зайти на страницу поиска, выбрать неделю, курс и институт, в предложенном списке выбрать свою группу.
Если нужно будет посмотреть другую неделю, то придется повторять все действия.

С помощью приложения **MAU Schedule** достаточно указать все данные при регистрации, после чего зайти на страницу расписания и по умолчанию будет отображаться текущая неделя.

## Содержание

--------------------

- [Технологии](#технологии)
- [Запуск](#запуск)
- [Env файл](#env-файл)
- [Функционал](#функционал)
- [Контакты](#контакты)

## Технологии

--------------------

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [SunEditor](https://github.com/JiHong88/suneditor)

## Запуск

--------------------

- Установите [Python 3.12](https://www.python.org/downloads/)
- Создайте файл ```.env``` и укажите настройки, используя [шаблон](.env.template) и [описание настроек](#env-файл).

### Настройка и запуск вручную

--------------------

#### Настройка виртуального окружения

#### Установка PostgreSQL

#### Установка Redis

#### Запуск Celery

#### Запуск приложения

```
python manage.py runserver
```

### Запуск с помощью Docker

- Установите [Docker](https://www.docker.com/)

- Сборка и запуск приложения:

  ```
  docker compose up --build -d
  ```
- Остановка приложения

  ```
  docker compose down
  ```

## Env файл

--------------------

В этом разделе описаны подробности о переменных окружения проекта.

- <span style="color: pink;">DEBUG</span> - если 1, то запустить приложение в debug режиме, если 0, то запустить в производственном режиме

  **По умолчанию:** 0


- <span style="color: pink;">SECRET_KEY</span> - секретный ключ, который используется для криптографической подписи. Должен быть установлен на уникальное и непредсказуемое значение

  **По умолчанию:** случайно сгенерированный ключ Django


- <span style="color: pink;">ALLOWED_HOSTS</span> - список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django.

  **Пример**: _127.0.0.1,example.com_

  **По умолчанию:** пустой список


- <span style="color: pink;">TIME_ZONE</span> - часовой пояс

  **По умолчанию:** UTC


- <span style="color: pink;">POSTGRES_DB</span> - название базы данных

  **По умолчанию:** MauSchedule


- <span style="color: pink;">POSTGRES_USER</span> - имя пользователя для бызы данных

  **По умолчанию:** MauUser


- <span style="color: pink;">POSTGRES_PASSWORD</span> - пароль от базы данных

  **По умолчанию:** 12345


- <span style="color: pink;">POSTGRES_HOST</span> - хост базы данных

  **По умолчанию:** localhost


- <span style="color: pink;">POSTGRES_PORT</span> - порт для базы данных

  **По умолчанию:** 5432


- <span style="color: pink;">REQUESTS_TIMEOUT</span> - время ожидания ответа от сайта университета в секундах

  **По умолчанию:** 5


- <span style="color: pink;">REDIS_HOST</span> - хост для Redis, где хранится кэш

  **По умолчанию:** localhost


- <span style="color: pink;">REDIS_PORT</span> - порт для Redis

  **По умолчанию:** 6379

## Функционал

--------------------

## Контакты

--------------------
