from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import login_required

from config import Config

from models import db, User, Trek

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user


app = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

app.config.from_object(Config)


db.init_app(app)
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )

with app.app_context():

    db.create_all()

    admin = User.query.filter_by(
        email="admin@trek.com"
    ).first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            role="admin",
            status="active"
        )

        db.session.add(admin)

        db.session.commit()

        print("Admin Created Successfully")

@app.route("/")
def home():

    return "Trekking App Running Successfully"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        hashed_password = generate_password_hash(password)

        status = "active"

        if role == "staff":
            status = "pending"

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            status=status
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            print("ROLE =", user.role)
            print("STATUS =", user.status)
            login_user(user)

            if user.role == "admin":
                return redirect("/admin-dashboard")

            elif user.role == "staff":
                return redirect("/staff-dashboard")

            else:
                return redirect("/user-dashboard")

        flash("Invalid Login")

    return render_template("login.html")
@app.route("/admin-dashboard")
@login_required
def admin_dashboard():

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_treks = Trek.query.count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks
    )

@app.route("/add-trek", methods=["GET", "POST"])
@login_required
def add_trek():

    if request.method == "POST":

        name = request.form["name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration = request.form["duration"]
        available_slots = request.form["slots"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek Added Successfully")

        return redirect(url_for("admin_dashboard"))

    return render_template("add_trek.html")
    


@app.route("/staff-dashboard")
def staff_dashboard():
    return "Staff Dashboard"


@app.route("/user-dashboard")
def user_dashboard():
    return "User Dashboard"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/view-treks")
@login_required
def view_treks():

    treks = Trek.query.all()

    return render_template(
        "view_treks.html",
        treks=treks
    )

if __name__ == "__main__":
    app.run(debug=True)
