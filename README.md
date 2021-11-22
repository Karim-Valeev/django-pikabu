# Приложение с системой древовидных комментариев (как на pikabu.ru).

### Link to the [site](https://django-pikabu.herokuapp.com/)

### Функциональность:
- регистрация и авторизация пользователей
- CRUD постов
- CRUD комментариев (комментарии привязываются либо к посту, либо к другому комментарию)
- REST API

### Условия:
- исходники на GitHub
- фреймворк — Django либо FastAPI

### ERD:

- user:
  - id | PK
  - username
  - email
  - password

- post:
  - id | PK
  - author | FK
  - title
  - body
  - created_at (auto)
  - comments 
  - categories | M2M

- comment:
  - id | PK
  - author | FK
  - text
  - created_at
  - post | FK
  - in_reply_to | FK


### Запуск

- `python3 -m venv venv` - создать виртуальное окружение
- `source venv/bin/activate` - войти в виртуальное окружение 
- `pip install -r requirements.txt` - установка зависимостей
- `docker-compose up -d` - запуск базы данных PostgreSQL (вместо выполнения этой команды можно поднять базу данных другим
способом)
- `python src/manage.py migrate` - применить миграции
- `python src/manage.py collectstatic` - собрать всю статику в одну папку
- `cd src/main/static && npm install` - поставить все пакеты, необходимые для верстки через пакетный менеджер npm
- `pip3 install pre-commit && pre-commit install` - включение pre-commit hook для автоматического запуска линтера
- `python src/manage.py runserver` - запуск сервера для разработки

### Загрузка данных

- `python src/manage.py loaddata src/main/fixtures/*.json` - загрузка начальных данных
