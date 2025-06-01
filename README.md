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
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

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
- [React](https://react.dev/)
- [SunEditor](https://github.com/JiHong88/suneditor)

## Запуск

--------------------

- Создайте файл ```.env``` в корне проекта и укажите настройки, используя [шаблон](.env.template) и [описание настроек](#env-файл).
- Создайте самоподписанный SSL сертификат для использования https. Поместите файлы `localhost.crt` и `localhost.key` в папку **secrets**.
- Установите [Docker](https://www.docker.com/).
- Сборка и запуск приложения:

  ```shell
  docker compose up --build -d
  ```
- Остановка приложения:

  ```shell
  docker compose down
  ```

## Env файл

--------------------

В этом разделе описаны подробности о переменных окружения проекта.

### Backend

#### Django

- <span style="color: pink;">DEBUG</span> - если 1, то запустить приложение в debug режиме, если 0, то запустить в производственном режиме

  **По умолчанию:** 0


- <span style="color: pink;">SECRET_KEY</span> - секретный ключ, который используется для криптографической подписи. Должен быть установлен на уникальное и непредсказуемое значение

  **По умолчанию:** случайно сгенерированный ключ Django


- <span style="color: pink;">ALLOWED_HOSTS</span> - список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django.

  **Пример**: _127.0.0.1,example.com_

  **По умолчанию:** пустой список


- <span style="color: pink;">TIME_ZONE</span> - часовой пояс

  **По умолчанию:** UTC

#### PostgreSQL

- <span style="color: pink;">POSTGRES_DB</span> - название базы данных

- <span style="color: pink;">POSTGRES_USER</span> - имя пользователя для бызы данных

- <span style="color: pink;">POSTGRES_PASSWORD</span> - пароль от базы данных

- <span style="color: pink;">POSTGRES_HOST</span> - хост базы данных

- <span style="color: pink;">POSTGRES_PORT</span> - порт для базы данных

#### Redis

- <span style="color: pink;">REDIS_HOST</span> - хост для Redis, где хранится кэш

- <span style="color: pink;">REDIS_PORT</span> - порт для Redis

#### MAU Schedule

- <span style="color: pink;">REQUESTS_TIMEOUT</span> - время ожидания ответа от сайта университета в секундах

  **По умолчанию:** 5

### Frontend

- <span style="color: pink;">HTTPS</span> - использовать ли https

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
