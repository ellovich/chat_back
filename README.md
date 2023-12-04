# Backend чата врач-пациент

В работе продемонстрированы умения работать с FastAPI, SQLAlchemy, Celery, Redis, Docker, а также многими другими библиотеками.

Активация окружения:

    .\.venv\Scripts\activate

poetry -> requirements.txt

    poetry export -f requirements.txt --without-hashes > requirements.txt

## alembic

Создание миграции

    alembic revision --autogenerate -m "init"

Обновление структуры БД:

    alembic upgrade head

## Запуск приложения

Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:  

```shell
uvicorn app.main:app --reload
```

Ее необходимо запускать в командной строке, обязательно находясь в корневой директории проекта, используя виртуальное окружение проекта.

### Celery & Flower

Для запуска Celery используется команда  

```shell
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```

`-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.  
Для запуска Flower используется команда  

```shell
celery --app=app.tasks.celery:celery flower
```

### Dockerfile

Для запуска веб-сервера (FastAPI) внутри контейнера необходимо раскомментировать код внутри Dockerfile и иметь уже запущенный экземпляр Docker на компьютере. Команда также запускается из корневой директории, в которой лежит файл Dockerfile.

```shell
docker build .
```

### Docker compose

Для запуска всех сервисов (БД, Redis, веб-сервер (FastAPI), Celery, Flower, Grafana, Prometheus) необходимо использовать файл docker-compose.yml и команды

```shell
docker compose build
docker compose up
```

`build` команду нужно запускать, если произошли изменения внутри Dockerfile, то есть менялась логика составления образа.

## fastapi-users

[fastapi-users](https://fastapi-users.github.io/fastapi-users/12.1)
[fastapi](https://fastapi.tiangolo.com/)
