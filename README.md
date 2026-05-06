# Team Task Manager

A web app where teams can manage projects, assign tasks, and track progress — built with role-based access control.

Made as a final-year B.Tech CSE project.

---

## Features

**Admin Role**
- Create, edit, delete projects
- Add/remove team members from projects
- Assign tasks to members with due dates
- View all tasks across projects
- See overdue task alerts

**Member Role**
- View projects they've been added to
- View tasks assigned to them
- Update task status: Pending → In Progress → Completed
- Cannot create projects or assign tasks

**REST API**
- Full CRUD APIs for projects and tasks
- Role-based permissions enforced on every endpoint
- Session-based auth

---

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: SQLite
- **Frontend**: Django Templates, HTML, CSS, vanilla JS
- **Auth**: Django's built-in auth system

---

## Project Structure

```
team_task_manager/
├── core/               # Django project settings & URLs
├── users/              # Auth, UserProfile model, dashboards
├── projects/           # Project model, views, REST API
├── tasks/              # Task model, views, REST API
├── templates/          # HTML templates
│   ├── shared/         # Base layout
│   ├── users/          # Login, signup, dashboards
│   ├── projects/       # Project pages
│   └── tasks/          # Task pages
├── static/
│   ├── css/style.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Clone / extract the project

```bash
cd team_task_manager
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for Django admin panel)

```bash
python manage.py createsuperuser
```

Or run the setup script which does both:

```bash
python setup.py
```

### 6. Start the server

```bash
python manage.py runserver
```

### 7. Open in browser

```
http://127.0.0.1:8000/
```

You'll be redirected to the login page. Sign up to create an account.

---

## How to Use

1. **Sign up** as Admin (to manage projects) or Member (to work on tasks)
2. **Admins**: Create a project → Add members → Create tasks and assign them
3. **Members**: Log in and see your assigned tasks → Update status as you work
4. **Admins**: Track all tasks from the dashboard, check overdue tasks in the nav

### REST API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/signup/` | Register new user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| GET  | `/api/auth/me/` | Current user info |
| GET/POST | `/api/projects/` | List / create projects |
| GET/PUT/DELETE | `/api/projects/<id>/` | Project detail |
| GET/POST | `/api/tasks/` | List / create tasks |
| GET/PATCH/DELETE | `/api/tasks/<id>/` | Task detail |
| GET  | `/api/users/` | List users (admin only) |

All API endpoints require session authentication (login first via `/api/auth/login/`).

---

## Notes

- The `UserProfile` model extends Django's User with a role field (admin/member)
- Role checks are done in views and API views — both template and API layers are protected
- Members can only update the `status` field of their tasks via the API (validated in serializer)
- SQLite is used for simplicity — can be swapped to PostgreSQL by changing `DATABASES` in `settings.py`

---

