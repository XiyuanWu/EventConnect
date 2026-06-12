# EventConnect Developer Documentation

## 1. Project Overview

EventConnect is a campus activity platform for UCR students to discover and organize both on-campus and off-campus events.  
While official school club activities are mostly on campus, many student social activities happen outside campus. This platform gives students one place to post and browse activities; baseline scope skips formal “join RSVP” mechanics.

Core idea:
- Support student-created events (restaurants, games, movies, etc.)
- Keep flows simple: post and browse events; comments on events (optional depth later)
- Provide a lightweight, school-focused community hub (no RSVP / signup tracking in baseline scope)

## 2. Scope

This document describes the current implementation direction for the Django version of the project.

In scope now:
- Django monolith project structure
- Server-rendered pages using Django Templates (not React)
- Basic account system
- Event posting and browsing (list/detail as implemented)
- Event comments on the public-facing side when built
- Admin moderation basics

Explicitly simplified / deferred:
- Participant signup, RSVP, “join event”, capacity limits, or waitlists

Out of scope for now:
- Email verification flow
- Production deployment details
- Final database vendor decision

## 3. Tech Stack

- Frontend: HTML, CSS, Django Templates
- Backend: Django (Python)
- Authentication: Django authentication system (customized for email-based login/register flow)
- Database (Production): MongoDB
- Database (Local Dev): SQLite (default for local testing only)

## 4. Project Structure

```text
EventConnect/
│
├─ eventconnect/            # Django project config (settings, urls, wsgi/asgi)
│
├─ accounts/                # App: authentication and user profile management
├─ events/                  # App: events (post/list/detail); comments tied to events
│
├─ templates/               # Shared Django templates
├─ static/                  # CSS/JS/images (if used globally)
├─ manage.py                # Django management entrypoint
└─ README.md                # Setup and quick start
```

Notes:
- `venv/` is local-only and should not be committed.
- Local `db.sqlite3` is for development convenience only.

## 5. Functional Requirements

### 5.1 Authentication and Accounts

Current decision:
- Any email can register in this phase (no verification code flow).
- Frontend may use regex for basic email format validation.
- No strict domain validation or inbox verification for now.

Account flows:
- Sign up inputs: `email`, `password`, `confirm password`
- Log in inputs: `email`, `password`
- Log out: authenticated users can log out normally

### 5.2 User Profile

- Each user can create/edit a profile.
- Profile can include basic personal information and profile image (to be finalized in model fields section later).

### 5.3 Event Management

- Users can create events.
- Event requires key fields such as title, time, location, and description.
- Users can browse and view event details.
- Capacity / join limits are out of baseline scope unless reintroduced deliberately later.

### 5.4 Interaction

- Users can comment on events (planned in current feature set).

### 5.5 Administrative Controls

- Admin can manage users and event posts.
- Admin can remove inappropriate content and suspend/ban users if needed.

## 6. Data and Database Plan

Production database target:
- MongoDB

Pending decisions:
- Database engine/vendor
- Hosted environment and credentials strategy
- Migration strategy from local SQLite to production database

## 7. Development Notes

- Use Django Templates for all initial UI pages.
- Keep architecture simple first, then extend features incrementally.
- This document is a living spec and will be updated as requirements evolve.
- On a fresh clone, run migrations and `createsuperuser` to set up local admin access. See [Installation.md](Installation.md#5-database-setup-local-development).