# Israel Classifieds Telegram Bot (aiogram 3)

Готовый к запуску бот объявлений для жителей Израиля: работа, аренда, авто, мероприятия и **Даром**.

## Локально (Docker)
1) Скопируй `.env.example` в `.env` и проверь `BOT_TOKEN`.
2) `docker compose up --build`
3) Открой бот в Telegram и отправь `/start`.

## Railway (быстро)
1) Запушь папку в GitHub.
2) В Railway: New Project → Deploy from GitHub.
3) В Variables добавь из `.env`: `BOT_TOKEN`, `ADMIN_IDS`, `POSTGRES_*`, `REDIS_*`.
4) Добавь два Plugins: PostgreSQL и Redis. Пропиши их хост/порт в переменные.
5) Deploy.

> В демо-режиме таблицы создаются автоматически при старте. Для продакшна стоит добавить Alembic-миграции.
