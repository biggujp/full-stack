# BaanSaiJai

Pixel Night / Retro Game themed Django project — A simple incident/product/member app.

---

## Quick Start (Windows)

1. Clone the repo

```bash
git clone <repo-url> full-stack
cd full-stack
```

2. Create virtual environment and activate

```powershell
python -m venv venv
# PowerShell
venv\Scripts\Activate.ps1
# or cmd
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations and create superuser

```bash
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py createsuperuser
```

5. Run development server

```bash
venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

---

## Media files (avatars, uploads)

- During development Django serves media when `MEDIA_URL` and `MEDIA_ROOT` are set.
- Uploaded avatars are saved under `media/avatars/`.

If you run with `runserver` the `urls.py` already includes static serving for `MEDIA_URL`.

---

## Useful Commands

- Run tests (if present):

```bash
venv\Scripts\python.exe manage.py test
```

- Open Django shell

```bash
venv\Scripts\python.exe manage.py shell
```

- Collect static files (for production):

```bash
venv\Scripts\python.exe manage.py collectstatic
```

---

## Deployment Notes

- Configure a production-ready webserver (Gunicorn / Daphne) and static/media serving (NGINX).
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
- Use environment variables or a secrets manager for sensitive settings.

---

## Troubleshooting

- "Couldn't import Django" — activate the virtualenv or install dependencies.
- URL reverse errors (e.g. `{% url 'about' %}`) — ensure `name=` is set in `myapp/urls.py`.
- Uploaded files not appearing — check `MEDIA_ROOT` and that the process has write permission.

---

If you want, I can also:

- Add a `requirements.txt` generated from the current venv.
- Add a short `docker-compose` for local dev.

