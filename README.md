# TRON_FAST
## Описание проекта
Микросервис позволяет добавлять данные о кошельках в БД и отображать их
### Содержанеие

- [Технологии](#tech)
- [Начало работы](#begining)
- [Комнада проекта](#team)

## <a name="tech">Технологии</a>

- [Fast API](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## <a name="begining">Начало работы</a>

### Начало работы

Активируйте вирутальное окржуние:

```
python -m venv venv
```

### Установка зависимостей

Установите зависимости из файла *requirements.txt*:

```
pip install -r requirements.txt
```

Применение миграций и первый запуск:

```
alembic upgrade head
```

### Запуск проекта

Запустите проект:

```
uvicorn app:app --reload
```

### Основные ендпоинты

/redoc
документация

/tron/wallets/
method - Post
Пройдет обращение к Tron и в БД будут добавлены данные о кошельке

/tron/wallets/
method - Get
Отобразит все данные из БД


## <a name="team">Команда проектка</a>

- Паршин Денис - backend developer
