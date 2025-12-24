# MyShop (Flask + React + PostgreSQL)

Этот репозиторий обновлён:

- Frontend переведён на **React** (папка `frontend/`) и стилистически повторяет шаблон из `online_shop-main.zip`.
- Backend оставлен на **Flask**, но добавлен **REST API** для React (`/api/*`).
- База данных переключена на **PostgreSQL** (через SQLAlchemy).
- Docker не используется.

---

## 1) Подготовка PostgreSQL

Пример для локальной БД:

1. Создайте БД `myshop`.
2. Установите переменную окружения `DATABASE_URL`.

Пример:

```bash
export DATABASE_URL='postgresql+psycopg2://postgres:postgres@localhost:5432/myshop'
```

---

## 2) Backend (Flask)

### Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Миграции

В проект добавлена начальная миграция `migrations/versions/0001_initial.py`.

```bash
export FLASK_APP=run.py
flask db upgrade
```

### Запуск

```bash
flask run
```

API будет доступен по адресу:

- `GET http://localhost:5000/api/health`
- `GET http://localhost:5000/api/products`

---

## 3) Frontend (React)

### Установка

```bash
cd frontend
npm install
```

### Разработка

```bash
npm start
```

По умолчанию frontend обращается к `http://localhost:5000/api`.
Если нужно изменить адрес, задайте переменную:

```bash
export REACT_APP_API_URL='http://localhost:5000/api'
```

### Production build (опционально)

```bash
cd frontend
npm run build
```

После этого Flask начнёт отдавать React билд на маршрутах `/`, `/products`, `/cart`, ...

---

## 4) Админ

В React есть `/admin` с простым логином.

Backend API:

- `POST /api/admin/login` → JWT токен
- `POST /api/admin/products` → создание товара

Чтобы админ мог войти, в таблице `user` должен существовать пользователь.
Пароль может быть как **plain text** (для совместимости со старой базой), так и **werkzeug hash**.
