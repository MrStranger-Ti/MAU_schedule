# MAU Schedule

<img alt="Static Badge" src="https://img.shields.io/badge/status-testing-blue" height="26">

--------------------


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54&link=https://www.djangoproject.com/)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

--------------------

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
- [Команда и Обязанности](#команда-и-обязанности)

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
- [Bootstrap](https://getbootstrap.com/)
- [SunEditor](https://github.com/JiHong88/suneditor)

## Запуск

--------------------

- Установите [Python 3.12](https://www.python.org/downloads/)
- Создайте файл ```.env``` и укажите настройки, используя [шаблон](.env.template) и [описание настроек](#env-файл).
- Откройте командную строку и перейдите в корень проекта:
  ```
  cd <путь до проекта>
  ```

### Настройка и запуск вручную

--------------------

#### Настройка виртуального окружения

- Создайте виртуальное окружение:
  ```
  python -m venv venv
  ```
- Активируйте виртуальное окружение:
    - Linux/MacOS:
      ```
      source venv/bin/activate
      ```
    - Windows
      ```
      venv/Scripts/activate
      ```

#### Установка и настройка PostgreSQL

- Установите [PostgreSQL](https://www.postgresql.org/download/)
- Войдите в оболочку PostgreSQL:
    - Linux/MacOS:
      ```
      sudo -U postgres psql
      ```
    - Windows:
      ```
      cd "C:\Program Files\PostgreSQL\<версия>\bin"
      
      psql -U postgres
      ```
- Создайте нового пользователя:
  ```
  CREATE USER <имя> WITH PASSWORD '<пароль>';
  ```
- Создайте новую базу данных:
  ```
  CREATE DATABASE <имя>;
  ```
- Дайте права только что созданному пользователю:
  ```
  GRANT ALL PRIVILEGES ON DATABASE <имя базы данных> TO <имя пользователя>;
  ```
- Укажите в ```.env``` все переменные, связанные с PostgreSQL.

#### Установка Redis

Redis не поддерживается на Windows, поэтому можно воспользоваться Docker образом [redis](https://hub.docker.com/_/redis) или установить подсистему Ubuntu на Windows с помощью [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/install).

- Установка Redis:
  ```
  sudo apt install redis-server
  ```
- Запуск сервера Redis:
  ```
  sudo service redis-server start
  ```

- Укажите в ```.env``` все переменные, связанных с Redis (если вы не меняли конфигурацию Redis, то можете оставить значения переменных по умолчанию).


- Остановить Redis можно следующей командой:
  ```
  sudo service redis-server stop
  ```

#### Запуск Celery

- Запустите worker:
  ```
  celery -A app worker -l info
  ```
- Запустите планировщик задач:
  ```
  celery -A app beat -l info
  ```

#### Запуск приложения

- Установите миграции:
  ```
  python manage.py migrate
  ```

- Создайте суперпользователя (для входа в админ. панель):
  ```
  python manage.py createsuperuser
  ```

- Запуск приложения:
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

### Использование

Если запустили приложение локально, то можно перейти по следующему адресу в браузере:

http://127.0.0.1:8000

Войти в админ. панель можно по следующему адресу:

http://127.0.0.1:8000/admin


## Env файл

--------------------

В этом разделе описаны подробности о переменных окружения проекта.

### Django

- <span style="color: pink;">DEBUG</span> - если 1, то запустить приложение в debug режиме, если 0, то запустить в производственном режиме

  **По умолчанию:** 0


- <span style="color: pink;">SECRET_KEY</span> - секретный ключ, который используется для криптографической подписи. Должен быть установлен на уникальное и непредсказуемое значение

  **По умолчанию:** случайно сгенерированный ключ Django


- <span style="color: pink;">ALLOWED_HOSTS</span> - список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django.

  **Пример**: _127.0.0.1,example.com_

  **По умолчанию:** пустой список


- <span style="color: pink;">TIME_ZONE</span> - часовой пояс

  **По умолчанию:** UTC

### PostgreSQL

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

### Redis

- <span style="color: pink;">REDIS_HOST</span> - хост для Redis, где хранится кэш

  **По умолчанию:** localhost


- <span style="color: pink;">REDIS_PORT</span> - порт для Redis

  **По умолчанию:** 6379

### MAU Schedule

- <span style="color: pink;">REQUESTS_TIMEOUT</span> - время ожидания ответа от сайта университета в секундах

  **По умолчанию:** 5

## Функционал

--------------------

### Идентификация / Аутентификация

--------------------

#### Главная

Зарегистрироваться в системе может человек с почтой, у которой домен МАУ (...@masu.edu.ru, ...@mstu.edu.ru, ...@mauniver.ru):

<img width="800px" src="readme_images/images/mau_domain_required.png" alt="Главная">

#### Регистрация

Для регистрации нужно указать несколько данных:

<img src="readme_images/gifs/sign-up.gif" alt="Регистрация">

В письме можно перейти по ссылке, чтобы подтвердить почту:

<img width="800px" src="readme_images/images/email_confirmed.png" alt="Отправлена ссылка для подтверждения почты">

#### Сброс пароля

Для сброса пароля нужно указать почту:

<img src="readme_images/gifs/password-reset-email-form.gif" alt="Отправка письма для сброса пароля">

В письме можно перейти по ссылке, чтобы сбросить пароль:

<img src="readme_images/gifs/password-reset-new.gif" alt="Установка нового пароля">

#### Вход

Для входа достаточно указать email и пароль:

<img src="readme_images/gifs/sign-in.gif" alt="Вход">

### Профиль

В профиле находится вся необходимая информация для отображения расписания:

<img src="readme_images/gifs/profile.gif" alt="Профиль">

### Расписание

#### Расписание группы

В расписании можно удобно выбирать неделю, по умолчанию будет выставлена текущая неделя:

<img src="readme_images/gifs/group-schedule.gif" alt="Расписание группы">

#### Расписание преподавателя

Для просмотра по расписания преподавателя необходимо его найти:

<img src="readme_images/gifs/teacher-schedule.gif" alt="Работа с профилем">


### Заметки

Можно добавлять заметки и редактировать их для каждой пары прямо в расписании:

<img src="readme_images/gifs/notes.gif" alt="Работа с профилем">

### Адаптивность

Приложением **MAU Schedule** можно пользоваться на разных устройствах с удобством:

<img src="readme_images/gifs/adaptability.gif" alt="Работа с профилем">


## Команда и обязанности

- Сорокожердьев Андрей - Fullstack-разработчик
  
  - [Telegram](https://t.me/MrStrangerTi)
  - asorokozherdyev@gmail.com


- Егорова Софья - Веб-дизайнер
  
  - [Telegram](https://t.me/alrdseled)
  - [Vk](https://vk.com/alrdseled)
