# Maksi Salary Bot 1.0.0

---

## Телеграм бот, для расчета заработной платы.

Рассчитывает зп у складских работников работающих на почасовой оплате.
Создан для отслеживания зп.

### Stack
- Docker - Launch
- Aiogram - Telegram bot api
- Sqlalchemy - ORM
- PostgreSQL - DB
- Alembic - migrations
- Apscheduler - schedule

## Запуск

---
1. Создать venv
2. Установить alembic
3. Запустить приложения командой:
```chatinput
docker compose up -d
```
4. Выполнить миграции:
```chatinput
alembic upgrade head
```
5. Бот должен работать
