# Realtime Chat
Данный проект - Fullstack приложение на Python FastAPI и React, выполненное как тестовое задание на стажировку Greenatom.

## Инструкция по запуску (деплою)
Все необходимые образы для работы приложения представлены в docker-compose в директорр /app. В /app/backend и /app/frontend представлены Dockerfile для backend и frontend соотвественно. \
Запуск приложения осуществляется через скрипт /app/scripts/start.sh (запуск docker-compose, upgrade alembic до последней ревизии, инициализация базовыми данными приложения). \
Запуск имеющихся **тестов** происходит через скрипт /app/scripts/test.sh
