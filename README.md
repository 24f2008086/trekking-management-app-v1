# TrekQuest - Trekking Management Application

A role-based Trekking Management System developed using **Flask**, **SQLite**, **Bootstrap**, and **Flask-Login** as part of the IIT Madras BS Degree Modern Application Development-I project.

---

## Project Overview

TrekQuest is a web-based trekking management platform that allows administrators, staff members, and users to efficiently manage trekking events through a centralized system.

The application supports:

- Role-based authentication
- Trek management
- Trek booking
- Staff assignment
- User management
- Booking history
- Profile management
- Search functionality
- Responsive Bootstrap UI

---

## Technology Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login

### Database
- SQLite

### Frontend
- HTML5
- Jinja2
- Bootstrap 5
- Bootstrap Icons

---

## Project Structure

```
TrekkingManagementApp/
│
├── app.py
├── models.py
├── config.py
├── requirements.txt
├── README.md
│
├── instance/
│   └── database.db
│
├── static/
│   └── images/
│
└── templates/
    ├── login.html
    ├── register.html
    ├── admin_dashboard.html
    ├── staff_dashboard.html
    ├── user_dashboard.html
    ├── available_treks.html
    ├── manage_trek.html
    ├── manage_staff.html
    ├── manage_users.html
    └── ...
```

---

# Features

## Admin

- Login
- Dashboard
- Add Trek
- View Treks
- Edit Trek
- Delete Trek
- Assign Staff
- Manage Staff
- Manage Users
- View Bookings
- Search Users
- Search Treks

---

## Staff

- Login
- Dashboard
- View Assigned Treks
- Manage Assigned Trek
- View Registered Participants
- Edit Profile

---

## User

- Register
- Login
- Dashboard
- Browse Available Treks
- Search Treks
- Book Trek
- Duplicate Booking Prevention
- View Booking History
- Edit Profile

---

# Authentication

Implemented using Flask-Login.

Three user roles:

- Admin
- Staff
- User

Role-based dashboards and protected routes are implemented.

---

# Database

SQLite database with SQLAlchemy ORM.

Main Models:

- User
- Trek
- Booking

Relationships are implemented using SQLAlchemy.

---

# Responsive UI

The application uses Bootstrap 5 and is responsive across desktop, tablet and mobile devices.

---

# Validation

Backend validation

- Required fields
- Duplicate booking prevention
- Slot availability checking
- Role authorization

Frontend validation

- HTML5 required fields
- Form validations

---

# Installation

Clone the repository

```
git clone <repository-link>
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application

```
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# Screenshots

- Home Page
- Admin Dashboard
- Staff Dashboard
- User Dashboard
- Available Treks
- Booking Page

(Add screenshots here if required.)

---

# Developed For

Modern Application Development – I

IIT Madras BS Degree Program

---

# License

This project is developed solely for educational purposes.