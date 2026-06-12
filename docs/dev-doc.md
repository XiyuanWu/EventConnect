# EventConnect Developer Documentation

## 1. Project Overview

EventConnect is a campus activity platform for UCR students to discover and organize both on-campus and off-campus events.  
While official school club activities are mostly on campus, many student social activities happen outside campus. This platform gives students one place to post and browse activities.

Core idea:
- Support student-created events (restaurants, games, movies, etc.)
- Keep flows simple: post, browse, comment, and manage your own posts
- Provide a lightweight, school-focused community hub (no RSVP / signup tracking)

## 2. Scope

This document reflects the **current Django implementation**, not future plans.

### Implemented now

- Django monolith with server-rendered **Django Templates** (not React)
- **SQLite** as the only database (`db.sqlite3` via Django defaults)
- Account registration and login (**username + password**)
- Optional **Google sign-in** (requires `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` in environment)
- User profile editing: display name, bio, major, interests, email, first/last name
- Event **create**, **list**, **detail**, **edit**, and **delete** (edit/delete limited to the creator)
- Top-level **comments** on events (authenticated users)
- Django **admin** for users, events, and comments
- Shared UI in `static/css/main.css` and `templates/base.html`

### Explicitly out of scope (not built)

- Profile **avatar / image upload**
- RSVP, participant signup, capacity limits, or waitlists
- Comment **reply** form in the UI (the model supports replies; only top-level posting is exposed)
- Email verification or UCR-only email domain checks
- External / hosted database (MongoDB, Postgres, etc.)
- Production deployment hardening

### Deferred / later

- Richer comment threads (reply UI)
- Email verification flow
- Production hosting, secrets management, and a non-SQLite database if scale requires it

## 3. Tech Stack

| Layer | Choice |
|-------|--------|
| Frontend | HTML, CSS (`static/css/main.css`), Django Templates |
| Backend | Django 6 (Python) |
| Auth | Django `contrib.auth` + custom views in `accounts/`; `django-allauth` installed for Google provider wiring |
| Database | **SQLite** (`django.db.backends.sqlite3`, file `db.sqlite3`) |

Dependencies are listed in `requirements.txt`.

## 4. Project Structure

```text
EventConnect/
│
├─ eventconnect/            # Project config (settings, urls, wsgi/asgi)
├─ accounts/                # Registration, login, profile, Google OAuth
├─ events/                  # Events and comments
├─ templates/               # Shared and app templates
├─ static/                  # Global CSS and assets
├─ docs/                    # Installation and developer docs
├─ manage.py
└─ README.md
```

Notes:
- `venv/` is local-only and should not be committed.
- **`db.sqlite3` is committed** for demo use so clones include sample events and a ready-to-use login (`test` / `test789456123`). See [Installation.md](Installation.md#demo-login-shared--public-database).

## 5. Functional Requirements (as implemented)

### 5.1 Authentication and Accounts

- **Register:** username (required), email (optional), password, confirm password
- **Log in:** username and password
- **Log out:** standard session logout
- **Google:** optional; shows on login page when OAuth env vars are configured
- No email verification; any email format may be used; no `@ucr.edu` enforcement in code

### 5.2 User Profile

Each authenticated user has a `Profile` linked to `User` with:

- `display_name`, `bio`, `major`, `interests`
- User fields editable on profile page: `email`, `first_name`, `last_name`

**Not implemented:** profile photo / avatar.

### 5.3 Event Management

- **Create** — title, date/time, location, description (authenticated)
- **Browse** — event list and detail pages (public)
- **Edit / delete** — creator only; delete requires confirmation
- **No** capacity, RSVP, or “join event” flows

### 5.4 Interaction

- Authenticated users can post **top-level comments** on an event detail page
- Existing replies (e.g. from admin) render in a thread; there is no public reply form yet
- Comments support soft-delete via `is_deleted` in the model (admin-facing)

### 5.5 Administrative Controls

- Django admin can manage users, events, and comments
- No in-app moderator role or user ban UI beyond admin

## 6. Data and Database

- **Single database:** SQLite file at project root (`db.sqlite3`)
- **No external database** is configured; MongoDB and other vendors are not in use
- Migrations live under each app’s `migrations/` package

**Demo note:** For coursework and live demos, the database may be kept **shared or publicly reachable** so teammates and reviewers can try the app without extra setup. **In production**, user data would sit in a **private, access-controlled store** with restricted credentials—not exposed for convenience. See also [README.md](../README.md).

## 7. Development Notes

- Use Django Templates for all UI pages; extend `base.html` for consistent layout
- Keep architecture simple; add features incrementally
- After pulling changes, run `python manage.py migrate` if models changed
- Shared demo login: `test` / `test789456123` (included in the committed database)
