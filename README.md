# Документация по развертыванию сервиса

## Установка
 - Клонируйте репозиторий: `git clone https://github.com/nanoCATR/fastapi_ya_audio.git`
 - Настройте API_URL и HTTPS в конфиге: scr/core/config (по необходимости)
 - Создайте приложение по ссылке: [https://oauth.yandex.ru/](URL)
 - Создайте файл .env и введите туда `YANDEX_CLIENT_ID`, `YANDEX_CLIENT_SECRET`, `YANDEX_REDIRECT_URI`, `SECRET_KEY` (для jwt токенов)

## Запуск докер контейнера
Зайдите в папку проекта и запустите следующую команду
```
docker-compose up -d --build


