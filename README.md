# Custom Authentication and Authorization API

Backend-приложение на Django REST Framework с собственной системой аутентификации и авторизации.

Проект реализует:

- регистрацию пользователей;
- вход по email и паролю;
- JWT-аутентификацию;
- logout через деактивацию сессии;
- мягкое удаление аккаунта;
- собственную систему ролей;
- собственную систему правил доступа к ресурсам;
- mock business objects для демонстрации авторизации;
- ошибки `401 Unauthorized` и `403 Forbidden`.

---

## Стек

- Python
- Django
- Django REST Framework
- PostgreSQL
- bcrypt
- PyJWT
- Docker, опционально

---

## Основная идея проекта

Проект разделяет две задачи:

### Аутентификация

Аутентификация отвечает на вопрос:

> Кто этот пользователь?

Пользователь входит в систему по email и паролю. После успешного входа сервер выдает JWT-токен.

Клиент должен передавать токен в заголовке:

```http
Authorization: Bearer <token>
```

При каждом запросе система проверяет:

- наличие токена;
- корректность JWT;
- срок действия токена;
- наличие активного пользователя;
- наличие активной сессии.

Если пользователя определить не удалось, API возвращает:

```http
401 Unauthorized
```

---

### Авторизация

Авторизация отвечает на вопрос:

> Что этому пользователю разрешено делать?

В проекте реализована собственная система ролей и правил доступа.

Пользователь может иметь одну или несколько ролей.

Роль имеет набор правил доступа к ресурсам приложения.

Если пользователь определен, но у него нет прав на действие, API возвращает:

```http
403 Forbidden
```

---

## Структура управления доступом

В проекте используются следующие основные таблицы.

### users

Собственная таблица пользователей.

Основные поля:

```text
id
first_name
last_name
middle_name
email
password_hash
is_active
created_at
updated_at
```

Пароль не хранится в открытом виде.

Перед сохранением пароль хешируется с помощью `bcrypt`.

---

### sessions

Таблица активных пользовательских сессий.

Основные поля:

```text
id
user_id
jti
is_active
created_at
expires_at
```

При login создается JWT-токен и запись в таблице `sessions`.

Поле `jti` связывает JWT-токен с конкретной сессией.

При logout сессия деактивируется:

```text
is_active = False
```

После этого старый JWT-токен больше не может использоваться.

---

### roles

Таблица ролей.

Примеры ролей:

```text
admin
manager
user
```

---

### user_roles

Связь пользователей и ролей.

Один пользователь может иметь одну или несколько ролей.

---

### business_elements

Таблица ресурсов приложения, к которым применяются правила доступа.

Примеры ресурсов:

```text
users
orders
products
access_rules
```

---

### access_role_rules

Главная таблица правил доступа.

Поля:

```text
role_id
element_id
read_permission
read_all_permission
create_permission
update_permission
update_all_permission
delete_permission
delete_all_permission
```

Права с суффиксом `_all_permission` дают доступ ко всем объектам ресурса.

Права без `_all_permission` дают доступ только к своим объектам, где:

```text
object.owner_id == user.id
```

Например:

```text
read_permission=True
read_all_permission=False
```

означает, что пользователь может читать только свои объекты.

А:

```text
read_all_permission=True
```

означает, что пользователь может читать все объекты этого ресурса.

---

## Установка проекта

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd <project-folder>
```

---

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

---

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

Если файла `requirements.txt` еще нет, можно установить зависимости вручную:

```bash
pip install "Django>=5.2,<6.0" djangorestframework psycopg2-binary python-dotenv bcrypt PyJWT
```

После этого можно создать `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## Настройка переменных окружения

В корне проекта создать файл `.env`:

```env
SECRET_KEY=django-secret-key-for-dev
DEBUG=True

DB_NAME=custom_auth_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

JWT_SECRET=jwt-secret-key-for-dev
JWT_EXPIRE_HOURS=24
```

Файл `.env` не должен попадать в Git.

---

## Запуск PostgreSQL через Docker

Если PostgreSQL не установлен локально, можно запустить его через Docker:

```bash
docker run --name custom_auth_postgres \
  -e POSTGRES_DB=custom_auth_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16
```

Проверить, что контейнер работает:

```bash
docker ps
```

Если контейнер уже был создан ранее, запустить его можно так:

```bash
docker start custom_auth_postgres
```

---

## Миграции

Создать и применить миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Заполнение тестовыми данными

Создать роли, ресурсы и правила доступа:

```bash
python manage.py seed_access
```

Создать демонстрационных пользователей:

```bash
python manage.py seed_users
```

После этого будут доступны пользователи:

### Admin

```text
email: admin@example.com
password: admin12345
role: admin
```

### Manager

```text
email: manager@example.com
password: manager12345
role: manager
```

### Regular user

```text
email: user@example.com
password: user12345
role: user
```

---

## Запуск сервера

```bash
python manage.py runserver
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

---

## Основные API endpoint'ы

### Аутентификация

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
```

---

### Профиль пользователя

```http
GET    /api/users/me/
PATCH  /api/users/me/
DELETE /api/users/me/
```

`DELETE /api/users/me/` выполняет мягкое удаление аккаунта:

```text
is_active = False
```

После этого пользователь больше не может войти в систему.

---

### Управление доступами

Эти endpoint'ы доступны пользователю с правами администратора.

```http
GET    /api/access/roles/
POST   /api/access/roles/
GET    /api/access/roles/<id>/
PATCH  /api/access/roles/<id>/
DELETE /api/access/roles/<id>/

GET    /api/access/elements/
POST   /api/access/elements/
GET    /api/access/elements/<id>/
PATCH  /api/access/elements/<id>/
DELETE /api/access/elements/<id>/

GET    /api/access/rules/
POST   /api/access/rules/
GET    /api/access/rules/<id>/
PATCH  /api/access/rules/<id>/
DELETE /api/access/rules/<id>/

GET    /api/access/user-roles/
POST   /api/access/user-roles/
GET    /api/access/user-roles/<id>/
PATCH  /api/access/user-roles/<id>/
DELETE /api/access/user-roles/<id>/
```

---

### Mock business endpoint'ы

Для демонстрации авторизации реализованы mock endpoint'ы заказов.

```http
GET    /api/orders/
POST   /api/orders/
GET    /api/orders/<id>/
PATCH  /api/orders/<id>/
DELETE /api/orders/<id>/
```

Таблица заказов в базе данных не создается.

Заказы хранятся в коде как список словарей.

Пример объекта:

```json
{
  "id": 1,
  "title": "Order 1",
  "description": "First mock order",
  "owner_id": 2
}
```

---

## Примеры запросов

### Регистрация

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "middle_name": "Ivanovich",
    "email": "ivan@example.com",
    "password": "12345678",
    "password_repeat": "12345678"
  }'
```

---

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "user12345"
  }'
```

Пример ответа:

```json
{
  "token": "<jwt-token>",
  "user": {
    "id": 1,
    "first_name": "Regular",
    "last_name": "User",
    "middle_name": "",
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2026-06-17T18:53:24.487020Z",
    "updated_at": "2026-06-17T18:53:24.487024Z"
  }
}
```

---

### Получить текущего пользователя

```bash
curl http://127.0.0.1:8000/api/users/me/ \
  -H "Authorization: Bearer <jwt-token>"
```

---

### Обновить профиль

```bash
curl -X PATCH http://127.0.0.1:8000/api/users/me/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "first_name": "Petr",
    "last_name": "Petrov"
  }'
```

---

### Logout

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Bearer <jwt-token>"
```

После logout этот же токен больше не работает.

---

### Мягкое удаление аккаунта

```bash
curl -X DELETE http://127.0.0.1:8000/api/users/me/ \
  -H "Authorization: Bearer <jwt-token>"
```

После удаления аккаунта пользователь больше не может войти в систему, но запись остается в базе данных со статусом:

```text
is_active = False
```

---

## Проверка авторизации

### Login admin

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin12345"
  }'
```

---

### Admin может получить список правил доступа

```bash
curl http://127.0.0.1:8000/api/access/rules/ \
  -H "Authorization: Bearer <admin-token>"
```

---

### Regular user не может получить список правил доступа

```bash
curl http://127.0.0.1:8000/api/access/rules/ \
  -H "Authorization: Bearer <user-token>"
```

Ожидаемый результат:

```http
403 Forbidden
```

---

### Получить список доступных заказов

```bash
curl http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer <user-token>"
```

Обычный пользователь увидит только те заказы, где:

```text
owner_id == user.id
```

Manager может видеть все заказы, если для роли `manager` установлено:

```text
read_all_permission=True
```

---

### Проверка 403 на чужом объекте

```bash
curl -i http://127.0.0.1:8000/api/orders/1/ \
  -H "Authorization: Bearer <user-token>"
```

Если заказ принадлежит другому пользователю, API вернет:

```http
403 Forbidden
```

---

### Проверка 401 без токена

```bash
curl -i http://127.0.0.1:8000/api/users/me/
```

Ожидаемый результат:

```http
401 Unauthorized
```

---

## Принцип проверки прав

Проверка прав выполняется функцией:

```python
has_access(user, element_code, action, owner_id=None)
```

Примеры:

```python
has_access(user, "orders", "read", owner_id=2)
has_access(user, "orders", "create")
has_access(user, "orders", "update", owner_id=2)
has_access(user, "orders", "delete", owner_id=2)
```

Логика:

```text
read:
  read_all_permission=True -> можно читать все объекты
  read_permission=True + owner_id == user.id -> можно читать свой объект

create:
  create_permission=True -> можно создать объект

update:
  update_all_permission=True -> можно изменять все объекты
  update_permission=True + owner_id == user.id -> можно изменять свой объект

delete:
  delete_all_permission=True -> можно удалять все объекты
  delete_permission=True + owner_id == user.id -> можно удалять свой объект
```

---

## Коды ошибок

### 401 Unauthorized

Возвращается, если:

```text
- отсутствует Authorization header;
- токен некорректный;
- токен истек;
- пользователь не найден;
- пользователь неактивен;
- сессия не найдена;
- сессия деактивирована.
```

---

### 403 Forbidden

Возвращается, если:

```text
- пользователь успешно аутентифицирован;
- но у пользователя нет прав на запрашиваемое действие.
```

---

## Особенности реализации

Проект не использует стандартную Django auth-систему как основную систему пользователей и прав.

Django и DRF используются как backend/API framework, но:

- таблица пользователей реализована самостоятельно;
- хранение паролей реализовано через bcrypt;
- JWT создается вручную через PyJWT;
- сессии хранятся в собственной таблице;
- роли и правила доступа реализованы в собственных таблицах;
- проверка доступа выполняется собственной функцией `has_access`.

---
