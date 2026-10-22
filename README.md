# Team Tasks Manager

A Django web application for managing tasks inside teams. A **team head** creates and maintains the team's tasks; **team members** pick up open tasks, work on them, and mark them as finished. Everyone sees only their own team's board and can filter it by status or by assignee.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

## Features

- **Registration and login** with team selection and session-based sign-in
- **Team-scoped board:** each user sees only the tasks of their own team
- **Team head:** adds, edits, and deletes tasks that nobody has picked up yet
- **Team members:** claim a new task (it becomes theirs and moves to *in process*), then mark it *finished*
- **Filtering** by status (`new` / `in process` / `finish`) and by the employee performing the task
- **Color-coded statuses** and a due date for every task
- **Django admin** for managing teams, users, and tasks

## Task Workflow

```
new ──(member chooses the task)──► in process ──(assignee finishes)──► finish
```

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python, Django 5.1 (views, ModelForms, ORM, migrations, sessions, CSRF protection) |
| **Database** | SQLite (Django's default; no setup needed) |
| **Frontend** | Django templates, HTML, CSS |

## Project Structure

```
FinalPythonProject/          # Django project root (contains manage.py)
├── manage.py
├── FinalPythonProject/      # project configuration
│   ├── settings.py
│   ├── urls.py              # includes the app's URLs and /admin
│   └── wsgi.py / asgi.py
├── tasksSystem/             # the application
│   ├── models.py            # Team, User, Task
│   ├── views.py             # login, register, tasks list, add / edit / delete, change status
│   ├── forms.py             # login, register, and Task forms
│   ├── urls.py
│   ├── admin.py
│   ├── templates/           # login, register, tasks_list, task_form
│   └── migrations/
└── static/css/              # stylesheets per page
```

## Data Model

| Model | Main fields |
|-------|-------------|
| **Team** | `name` |
| **User** | `id` (national ID, primary key), `fullName`, `password`, `phone`, `isAdmin` (team head), `team` → Team |
| **Task** | `name`, `description`, `status`, `finalDate`, `team` → Team, `user` → User (assignee, optional) |

## Routes

| URL | Method | Description | Intended for |
|-----|--------|-------------|--------------|
| `/`, `/login/` | GET, POST | Sign in | Everyone |
| `/register/` | GET, POST | Create an account and choose a team | Everyone |
| `/tasks/tasks_list/` | GET | Team board; filter with `?status=` and `?user_id=` | Signed-in users |
| `/tasks/add_task/` | GET, POST | Add a task | Team head† |
| `/tasks/edit_task/<id>/` | GET, POST | Edit a task | Team head† |
| `/tasks/delete/<id>/` | POST | Delete a task | Team head† |
| `/tasks/change_status/<id>/` | POST | Take a task / mark it as finished | Team members† |
| `/admin/` | | Django admin | Superuser |

† Currently enforced in the interface; server-side permission checks are on the [roadmap](#roadmap).

## Getting Started

### Prerequisites
- Python 3.10 or newer

### 1. Clone and install
```bash
git clone https://github.com/sara-simi-git/tasks_system_python.git
cd tasks_system_python

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create the database
```bash
cd FinalPythonProject
python manage.py migrate
```

### 3. Create teams
Registration requires choosing an existing team, so create at least one first:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin/>, sign in, and add one or more **Teams**.

### 4. Use the application
Open <http://127.0.0.1:8000/> and register.

- **To try the team-head view:** register with a full name that **starts with `teamhead`** (for example `teamhead Dana`) in a team that does not have a head yet.
- Register another user in the same team to see the member view, then add a task as the head and claim it as the member.


## What This Project Demonstrates

- The Django request cycle end to end: URL routing, views, templates, and the ORM
- Relational modeling with foreign keys and iterative schema changes through migrations
- Form handling with `ModelForm`, CSRF protection, and session-based state
- Filtering with query-string parameters and role-dependent rendering in templates
- Atomic database operations with `transaction.atomic`
