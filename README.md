![Workflow badge.](https://github.com/stalinovna/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на различные произведения.

Это совместный проект трёх студентов, который реализован в рамках учебного курса Яндекс.Практикум.

Проект доступен по ссылке: http://stalinovna.hopto.org/admin

## Используемые технологии

- Python 3.9
- Django 3.2
- Django Rest Framework 3.12.4
- Simple JWT

## Описание проекта

API для сервиса YaMDb.

**JWT-токен**: отправить confirmation_code на переданный email, получение JWT-токена в обмен на email и confirmation_code.

**Пользователи**: получить список всех пользователей, создание пользователя, получить пользователя по username, изменить данные пользователя по username, удалить пользователя по username, получить данные своей учетной записи, изменить данные своей учетной записи.

**Категории (типы) произведений**: получить список всех категорий, создать категорию, удалить категорию.

**Категории жанров**: получить список всех жанров, создать жанр, удалить жанр.

**Произведения, к которым пишут отзывы**: получить список всех объектов, создать произведение для отзывов, информация об объекте, обновить информацию об объекте, удалить произведение.

**Отзывы**: получить список всех отзывов, создать новый отзыв, получить отзыв по id, частично обновить отзыв по id, удалить отзыв по id.

**Комментарии к отзывам**: получить список всех комментариев к отзыву по id, создать новый комментарий для отзыва, получить комментарий для отзыва по id, частично обновить комментарий к отзыву по id, удалить комментарий к отзыву по id.

## Как запустить проект

Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Запуск тестов

Из корня проекта:

```
pytest
```

## Примеры некоторых запросов API

#### 1. Регистрация нового пользователя
Получить код подтверждения на переданный email. Права доступа: Доступно без токена. Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

[POST] http://127.0.0.1:8000/api/v1/auth/signup/

#### Sample response STATUS: 200
```
{
  "email": "string",
  "username": "string"
}
```
#### 2. Получение JWT-токена
Получение JWT-токена в обмен на username и confirmation code. Права доступа: Доступно без токена.

[POST] http://127.0.0.1:8000/api/v1/auth/token/

#### Sample response STATUS: 200
```
{
  "token": "string"
}
```
#### 3. Получение списка всех категорий
Получить список всех категорий Права доступа: Доступно без токена.

[GET] http://127.0.0.1:8000/api/v1/categories/

#### Sample response STATUS: 200
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
#### 4. Добавление новой категории
Создать категорию. Права доступа: Администратор. Поле slug каждой категории должно быть уникальным.

[POST]  http://127.0.0.1:8000/api/v1/categories/

#### Sample response STATUS: 201
```
{
  "name": "string",
  "slug": "string"
}
```
#### 5. Удаление категории
Удалить категорию. Права доступа: Администратор.

[DELETE] http://127.0.0.1:8000/api/v1/categories/{slug}/

#### Sample response STATUS: 204
```
```
#### 6. Получение списка всех жанров
Получить список всех жанров. Права доступа: Доступно без токена

[GET] http://127.0.0.1:8000/api/v1/genres/

#### Sample response STATUS: 200
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
#### 7. Добавление жанра
Добавить жанр. Права доступа: Администратор. Поле slug каждого жанра должно быть уникальным.

[POST] http://127.0.0.1:8000/api/v1/genres/

#### Sample response STATUS: 201
```
{
  "name": "string",
  "slug": "string"
}
```
#### 8. Получение списка всех отзывов
Получить список всех отзывов. Права доступа: Доступно без токена.

[GET] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

#### Sample response STATUS: 200
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
#### 9. Добавление нового отзыва
Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: Аутентифицированные пользователи.

[POST] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/

#### Sample response STATUS: 201
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
#### 10. Частичное обновление отзыва по id
Частично обновить отзыв по id. Права доступа: Автор отзыва, модератор или администратор.

[PATCH] http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

#### Sample response STATUS: 200
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
#### Полный список запросов API находятся в документации

по адресу `http://127.0.0.1:8000/redoc/`

## Авторы проекта

[Ковалёв Евгений](https://github.com/eugenekweb) - управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail.

[Купченко Елизавета](https://github.com/stalinovna) - категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них. Реализация импорта данных из csv файлов.

[Хромова Марина](https://github.com/marina-khromova) - отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений.
