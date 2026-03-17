# OA System — Project Startup Guide

## Project Overview

A full-stack enterprise OA (Office Automation) system with separated frontend and backend:

| Layer | Tech Stack | Directory |
|-------|-----------|-----------|
| Frontend | Vue 3 + Vite + Element Plus + Pinia | `src/` |
| Backend | Django 6 + Django REST Framework + JWT | `oaback/` |
| Database | SQLite3 (development) | `oaback/db.sqlite3` |

---

## Requirements

| Tool | Recommended Version |
|------|-------------------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |

---

## 1. Backend Setup

### 1. Create and activate virtual environment

```bash
# From the project root directory
python -m venv venv

# Windows
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r oaback/requirements.txt
```

Key dependencies:

```
Django==6.0.3
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
django-cors-headers==4.9.0
pillow==12.1.1
```

### 3. Run database migrations

```bash
cd oaback
python manage.py migrate
```

### 4. Create a superuser (first-time setup)

```bash
cd oaback
python manage.py createsuperuser
```

> The superuser account is the **administrator** of the system. See the Permission System section below for full details.

### 5. Start the backend development server

```bash
cd oaback
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

Admin panel: `http://127.0.0.1:8000/admin`

---

## 2. Frontend Setup

### 1. Install dependencies

```bash
# From the project root directory (where src/ is located)
npm install
```

### 2. Environment variable configuration

Development config file: `.env.development`

```env
VITE_BASE_URL=http://127.0.0.1:8000
VITE_APP_TITLE="OA System"
```

> If the backend port changes, update `VITE_BASE_URL` accordingly.

### 3. Start the frontend development server

```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 3. Initial Data Setup (First-time Use)

Go to Django Admin at `http://127.0.0.1:8000/admin` and follow these steps:

1. **Create departments**: STAFF → Department → Add
   - Example: `Tech`, `Marketing`, `Board of Directors`

2. **Add employees**: Log in to the frontend as a superuser and go to Employee Management → Add Employee, or create them manually via STAFF → Staff in the admin panel

3. **Assign departments**: STAFF → Staff → edit the employee and set their department

---

## 4. Permission System

The system has two permission levels:

### Superuser (Administrator)
Created via `python manage.py createsuperuser` or by checking **Superuser status** in Django Admin.

| Feature | Superuser |
|---------|-----------|
| Add Employee | ✅ |
| Delete Employee | ✅ |
| Update Employee Status | ✅ |
| View all Leave Requests (Team Attendance) | ✅ |
| Approve / Reject any Leave Request | ✅ |
| Delete any Notification | ✅ |
| Publish Notification to any department | ✅ |
| View all Notifications | ✅ |

### Regular Employee
Standard accounts created through Add Employee.

| Feature | Regular Employee |
|---------|----------------|
| View own Leave Requests | ✅ |
| Submit Leave Request | ✅ |
| Delete own Notifications | ✅ |
| Publish Notification to own department or All | ✅ |
| View Notifications (own dept + public only) | ✅ |
| Team Attendance / Add Employee / Delete Employee | ❌ |

> **Note:** After a superuser logs in, they must **log out and log back in** if their `is_superuser` flag was changed, since the frontend caches user info in `localStorage`.

---

## 5. API Routes

| Module | Prefix | Description |
|--------|--------|-------------|
| Auth | `/auth/` | Login, change password |
| Staff | `/staff/` | Department management, employee CRUD |
| Notification | `/inform/` | Publish, list, detail, read records, file/image upload |
| Leave | `/absent/` | Leave application and approval |
| Home | `/home/` | Dashboard statistics |
| Media files | `/media/` | Uploaded images and attachments |

---

## 6. Notification File Uploads

The rich-text editor in **Publish Notification** supports:
- **Images**: drag & drop or toolbar button, up to **25 MB**
- **Other files** (PDF, Word, etc.): toolbar button or drag & drop, up to **25 MB**

Uploaded files are stored under `oaback/media/`:
- Images → `oaback/media/images/`
- Other files → `oaback/media/attachments/`

---

## 7. Employee Status

| Value | Meaning | Frontend Display |
|-------|---------|-----------------|
| `1` | Active | Green |
| `0` | Inactive | Yellow |
| `3` | Locked | Red |

Only superusers can update employee status. Status can also be changed via Django Admin.

---

## 8. JWT Authentication

- Request header format: `Authorization: JWT <token>`
- Access Token lifetime: **1 day**
- Refresh Token lifetime: **7 days**
- Tokens are stored in the browser's `localStorage`

---

## 9. Frequently Asked Questions

**Q: Frontend requests return CORS errors?**
Make sure the backend is running at `http://127.0.0.1:8000` and `VITE_BASE_URL` in `.env.development` matches.

**Q: Page is blank or Employee List shows no data after login?**
Check that the logged-in user has a Staff record in Django Admin with a department assigned.

**Q: Notification List is empty after publishing?**
Make sure all migrations have been applied (`python manage.py migrate`). The `inform_inform_departments` join table must exist.

**Q: Department dropdown is empty?**
Add at least one department in Django Admin under STAFF → Department.

**Q: Superuser cannot see Team Attendance / Add Employee after login?**
Log out and log back in so the frontend reloads the updated user info (including `is_superuser`) from the backend.

**Q: File upload in Notification editor does nothing?**
Ensure the backend server is running. Uploaded files are served from `/media/` — confirm `MEDIA_ROOT` is writable.
