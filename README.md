# Веб-сервис для управления движением денежных средств (ДДС)

Веб-приложение на Django для учёта, управления и анализа поступлений и списаний денежных средств.

## Стек технологий

- **Backend:** Python 3.12, Django 6, Django REST Framework
- **БД:** SQLite
- **Frontend:** Bootstrap 5, JavaScript (Fetch API)
- **Админ-панель:** django-jazzmin

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/levanchik3010-jpg/testovoe_zadanie_PervayaITCompaniya.git
cd testovoe_zadanie_PervayaITCompaniya
```

### 2. Установить зависимости

```bash
uv sync
```

### 3. Применить миграции

```bash
uv run manage.py migrate
```

### 4. Создать суперпользователя

```bash
uv run manage.py createsuperuser
```

### 5. Запустить сервер

```bash
uv run manage.py runserver
```

Приложение: **http://127.0.0.1:8000/**  
Админ-панель: **http://127.0.0.1:8000/admin/**

## Первоначальная настройка справочников

После запуска войдите в админ-панель и добавьте начальные данные:

- **Статусы:** Бизнес, Личное, Налог
- **Типы:** Пополнение, Списание
- **Категории** (с привязкой к типу): например, «Маркетинг» → «Списание»
- **Подкатегории** (с привязкой к категории): например, «Avito», «Farpost» → «Маркетинг»

## API

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/categories/?type_id=<id>` | Категории по типу |
| GET | `/api/subcategories/?category_id=<id>` | Подкатегории по категории |