from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="active"
    )

    def __repr__(self):
        return self.name

class Trek(db.Model):

    __tablename__ = "treks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100)
    )

    difficulty = db.Column(
        db.String(50)
    )

    duration = db.Column(
        db.Integer
    )

    available_slots = db.Column(
        db.Integer
    )

    start_date = db.Column(
        db.String(50)
    )

    end_date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50),
        default="Open"
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id")
    )

    booking_date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(50),
        default="Booked"
    )

