# Personal Blog — Django + MongoDB + Docker

A personal publishing platform with registration, login, author dashboard, post CRUD, categories, image uploads, search, and moderated comments.

## Requirements
- Docker Desktop with WSL 2 backend
- Git

## Run locally
1. Copy `.env.example` to `.env`.
2. Change the secret and MongoDB password in `.env`.
3. Build and start:

   ```powershell
   docker compose up --build -d
   ```

4. Apply Django migrations and create an admin:

   ```powershell
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

5. Open http://localhost:8000 and http://localhost:8000/admin/

## Stop
```powershell
docker compose down
```

To also delete the MongoDB data volume (destructive):
```powershell
docker compose down -v
```

## GitHub
Do not commit `.env`. Commit `.env.example` only. Before pushing, ensure `.env` is ignored and contains no real secrets.

## Deployment notes
For production, set `DJANGO_DEBUG=False`, use a strong `DJANGO_SECRET_KEY`, set `DJANGO_ALLOWED_HOSTS` to your domain/IP, change MongoDB credentials, configure HTTPS/reverse proxy, backups, and persistent volumes. Do not expose MongoDB port 27017 publicly.
