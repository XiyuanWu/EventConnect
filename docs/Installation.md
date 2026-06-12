# Installation / Usage

Set up and run the EventConnect project locally.

## 1. Prerequisites

Install these first:
- Python 3.12+ (recommended)
- Git

## 2. Clone the Repository

```bash
git clone <your-repo-url>
cd final-project-campus_event_platform
```

## 3. Create and Activate Virtual Environment

Choose commands for your OS.

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS / Linux (bash or zsh)

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Upgrade pip and Install Dependencies

```bash
python -m pip install --upgrade pip
```

Current required package:

```bash
pip install django
```

If a `requirements.txt` file exists, install all dependencies with:

```bash
pip install -r requirements.txt
```

## 5. Database Setup (Local Development)

Run migrations:

```bash
python manage.py migrate
```

Create your own admin account (optional):

```bash
python manage.py createsuperuser
```

### Default admin account (local / demo only)

A default superuser may already exist for local testing and demos:

| Field | Value |
|-------|-------|
| Username | `admin` |
| Email | `admin@admin.com` |
| Password | `123` |

Use this only on your own machine or in a demo environment. **Change or remove this account** before sharing, deploying, or using a shared database.

## 6. Run the Development Server

```bash
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/


## 7. Common Development Commands

Create a new app:

```bash
python manage.py startapp <app_name>
```

Collect static files (if needed later):

```bash
python manage.py collectstatic
```

Run Django checks:

```bash
python manage.py check
```

## 8. Deactivate Environment

When finished:

```bash
deactivate
```

## 9. Troubleshooting

### `django-admin` or `python manage.py` command not found

- Make sure virtual environment is activated.
- Use `python -m django --version` to verify Django is installed in the active environment.
- On Windows, you can run commands explicitly with:

```powershell
.\venv\Scripts\python manage.py runserver
```

### Migration issues

- Ensure you are in the project root (same folder as `manage.py`).
- Run:

```bash
python manage.py makemigrations
python manage.py migrate
```