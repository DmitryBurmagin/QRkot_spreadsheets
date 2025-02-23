# QRKot - Благотворительный проект для сбора средств для котиков

QRKot — это благотворительный проект, цель которого — собрать средства для помощи бездомным котикам. Этот проект позволяет пользователям пожертвовать деньги на различные цели, следить за прогрессом сбора средств и инвестировать в проекты.

## Технологии, использованные в проекте

В проекте используются следующие основные технологии и библиотеки:

- **FastAPI**: современный веб-фреймворк для создания RESTful API с высокой производительностью, который основан на Python.
- **SQLAlchemy**: ORM для работы с базой данных, которая предоставляет удобный способ работы с SQL.
- **Pydantic**: библиотека для валидации данных и сериализации моделей.
- **Alembic**: инструмент для миграции базы данных.
- **Uvicorn**: ASGI сервер, используемый для запуска FastAPI-приложений.
- **JWT (JSON Web Token)**: для аутентификации и авторизации пользователей.
- **pytest**: фреймворк для тестирования, используемый для написания и выполнения тестов.
- **aiogoogle**: библиотека для асинхронного взаимодействия с Google API.

## Как развернуть проект

### Установка зависимостей

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/DmitryBurmagin/cat_charity_fund.git
    cd cat_charity_fund
    ```

2. Установите зависимости с помощью `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Запустите сервер с помощью `Uvicorn`:

    ```bash
    pipenv run uvicorn app.main:app --reload
    ```

4. Для работы с базой данных используйте Alembic для миграций:

    ```bash
    pipenv run alembic upgrade head
    ```

5. Запустите проект в браузере, перейдите по адресу: [`http://127.0.0.1:8000`](URL).

## Описание функционала

Проект позволяет:

- **Создавать благотворительные проекты** и собирать средства для них.
- **Пожертвовать деньги** на проекты.
- **Следить за прогрессом** сбора средств.
- **Аутентификация пользователей** через JWT-токены.
- **Администрирование** для управления проектами и пожертвованиями.

## Основные файлы

- **`app/main.py`** — основной файл для запуска FastAPI приложения.
- **`app/models/`** — модели SQLAlchemy для взаимодействия с базой данных.
- **`app/schemas/`** — схемы Pydantic для валидации данных.
- **`app/api/routers/`** — маршруты API для взаимодействия с внешним миром.
- **`app/services/`** — вспомогательные сервисы, такие как обработка инвестиций.


## Новый функционал, выгрузка в Google Таблицы: 

### CURL Запрос к эндпоинту /google/

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/google/' \
  -H 'accept: application/json' \
  -d ''
  ```
 
 ## Документация API

Перейдите по [ссылке на документацию FastAPI](http://127.0.0.1:8000/docs) для подробного описания всех доступных эндпоинтов и их параметров.


 

## О проекте

Этот проект был создан в рамках учебного задания Яндекс Практикума. Работу над проектом выполнил [Бурмагин Дмитрий](https://github.com/DmitryBurmagin) .


