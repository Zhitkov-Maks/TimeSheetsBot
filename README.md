# Maksi Salary Bot 2.0.1

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

Для работы приложения у вас должен быть установлен докер.

### Запустить приложение командой

```commandline
docker compose up -d
```

Автоматически должны выполниться миграции и запуститься бот.