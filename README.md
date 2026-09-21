# AuthApp

Небольшое приложение авторизации на FastAPI с PostgreSQL, подтверждением email и простым frontend без сборщика.

## Запуск

1. Создайте локальный файл настроек:

   ```bash
   cp .env.example .env
   ```

2. Заполните `.env`. Для Gmail используйте пароль приложения, а не обычный пароль.

3. Запустите PostgreSQL:

   ```bash
   docker compose up -d postgres
   ```

4. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

5. Примените миграции:

   ```bash
   alembic upgrade head
   ```

6. Запустите API:

   ```bash
   uvicorn app.main:app --reload
   ```

   API будет доступен по адресу `http://127.0.0.1:8000`, документация — по адресу `http://127.0.0.1:8000/docs`.

7. Запустите frontend отдельным локальным сервером в другом терминале:

   ```bash
   python3 -m http.server 5500 --directory frontend
   ```

   Откройте `http://127.0.0.1:5500`.

## Остановка

Остановить PostgreSQL можно командой:

```bash
docker compose down
```