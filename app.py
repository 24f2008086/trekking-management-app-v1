from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from datetime import datetime
from config import Config
from models import db, User, Trek, Booking

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


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
        # print("Admin Created Successfully")


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

@app.route("/")
def home():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))

        elif current_user.role == "staff":
            return redirect(url_for("staff_dashboard"))

        else:
            return redirect(url_for("user_dashboard"))
    return render_template("index.html")


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

                if user.status != "active":
                    flash("Your account is waiting for admin approval.", "warning")
                    return redirect(url_for("login"))

                return redirect("/staff-dashboard")

            else:

                if user.status == "blacklisted":
                    flash("Your account has been blacklisted.", "danger")
                    return redirect(url_for("login"))

                return redirect("/user-dashboard")

        flash("Invalid Email or Password!", "danger")

    return render_template("login.html")
@app.route("/admin-dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))

    total_users = User.query.filter_by(role="user").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return render_template(
    "admin_dashboard.html",
    total_users=total_users,
    total_staff=total_staff,
    total_treks=total_treks,
    total_bookings=total_bookings
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

        flash("Trek Added Successfully", "success")

        return redirect(url_for("admin_dashboard"))

    return render_template("add_trek.html")
    


@app.route("/staff-dashboard")
@login_required
def staff_dashboard():
    if current_user.role != "staff":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))

    treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff_dashboard.html",
        treks=treks
    )

@app.route("/manage-trek/<int:trek_id>", methods=["GET", "POST"])
@login_required
def manage_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        flash("You are not assigned to this trek.", "danger")
        return redirect(url_for("staff_dashboard"))

    if request.method == "POST":

        trek.available_slots = request.form["available_slots"]

        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek Updated Successfully", "success")

        return redirect(url_for("staff_dashboard"))

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "manage_trek.html",
        trek=trek,
        bookings=bookings
    )

@app.route("/user-dashboard")
@login_required
def user_dashboard():
    if current_user.role != "user":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))
    return render_template("user_dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully.", "info")
    return redirect(url_for("login"))

@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        current_user.name = request.form["name"]
        current_user.email = request.form["email"]

        db.session.commit()

        flash("Profile Updated Successfully", "success")

        return redirect(url_for("user_dashboard"))

    return render_template("edit_profile.html")

@app.route("/view-treks")
@login_required
def view_treks():

    search = request.args.get("search")

    treks = Trek.query

    if search:

        treks = treks.filter(
            (Trek.name.contains(search)) |
            (Trek.location.contains(search)) |
            (Trek.id == search)
        )

    treks = treks.all()

    return render_template(
        "view_treks.html",
        treks=treks,
        search=search
    )

@app.route("/edit-trek/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = request.form["duration"]
        trek.available_slots = request.form["slots"]
        trek.start_date = request.form["start_date"]
        trek.end_date = request.form["end_date"]

        db.session.commit()

        flash("Trek Updated Successfully", "success")

        return redirect(url_for("view_treks"))

    return render_template(
        "edit_trek.html",
        trek=trek
    )

@app.route("/delete-trek/<int:trek_id>")
@login_required
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)

    db.session.commit()

    flash("Trek Deleted Successfully", "success")

    return redirect(url_for("view_treks"))

@app.route("/manage-staff")
@login_required
def manage_staff():

    search = request.args.get("search")

    staff = User.query.filter_by(role="staff")

    if search:
        staff = staff.filter(
            (User.name.contains(search)) |
            (User.email.contains(search)) |
            (User.id == search)
        )

    staff = staff.all()

    return render_template(
        "manage_staff.html",
        staff=staff,
        search=search
    )

@app.route("/approve-staff/<int:user_id>")
@login_required
def approve_staff(user_id):

    staff = User.query.get_or_404(user_id)

    staff.status = "active"

    db.session.commit()

    flash("Staff Approved Successfully", "success")

    return redirect(url_for("manage_staff"))

@app.route("/blacklist-staff/<int:user_id>")
@login_required
def blacklist_staff(user_id):

    staff = User.query.get_or_404(user_id)

    staff.status = "blacklisted"

    db.session.commit()

    flash("Staff Blacklisted Successfully", "success")

    return redirect(url_for("manage_staff"))

@app.route("/assign-staff/<int:trek_id>", methods=["GET", "POST"])
@login_required
def assign_staff(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    staffs = User.query.filter_by(
        role="staff",
        status="active"
    ).all()

    if request.method == "POST":

        trek.staff_id = request.form["staff"]

        db.session.commit()

        flash(
            "Staff Assigned Successfully",
            "success"
        )

        return redirect(
            url_for("view_treks")
        )

    return render_template(
        "assign_staff.html",
        trek=trek,
        staffs=staffs
    )

@app.route("/activate-user/<int:user_id>")
@login_required
def activate_user(user_id):

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)

    user.status = "active"

    db.session.commit()

    flash("User activated successfully!", "success")

    return redirect(url_for("manage_users"))

@app.route("/blacklist-user/<int:user_id>")
@login_required
def blacklist_user(user_id):

    user = User.query.get_or_404(user_id)

    user.status = "blacklisted"

    db.session.commit()

    flash("User Blacklisted Successfully", "success")

    return redirect(url_for("manage_users"))

@app.route("/manage-users")
@login_required
def manage_users():

    search = request.args.get("search")

    users = User.query.filter_by(role="user")

    if search:
        users = users.filter(
            (User.name.contains(search)) |
            (User.email.contains(search)) |
            (User.id == search)
        )

    users = users.all()

    return render_template(
        "manage_users.html",
        users=users,
        search=search
    )

@app.route("/view-bookings")
@login_required
def view_bookings():

    bookings = Booking.query.all()

    return render_template(
        "view_bookings.html",
        bookings=bookings
    )
 
@app.route("/available-treks")
@login_required
def available_treks():

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")

    treks = Trek.query.filter_by(status="Open")

    if search:
        treks = treks.filter(Trek.name.contains(search))

    if difficulty:
        treks = treks.filter(Trek.difficulty == difficulty)

    if location:
        treks = treks.filter(Trek.location.contains(location))

    treks = treks.all()

    return render_template(
        "available_treks.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        location=location
    )

@app.route("/book-trek/<int:trek_id>")
@login_required
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    # Allow booking only if trek is open
    if trek.status != "Open":
        flash("This trek is not open for booking.", "danger")
        return redirect(url_for("available_treks"))

    # Prevent overbooking
    if trek.available_slots <= 0:
        flash("No slots available for this trek.", "danger")
        return redirect(url_for("available_treks"))

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by(
    user_id=current_user.id,
    trek_id=trek.id,
    status="Booked"
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("my_bookings"))

    # Create booking
    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_date=datetime.now().strftime("%d-%m-%Y")
    )

    db.session.add(booking)

    # Reduce available slots
    trek.available_slots -= 1

    db.session.commit()

    flash("Trek Booked Successfully", "success")

    return redirect(url_for("my_bookings"))

@app.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "view_bookings.html",
        bookings=bookings
    )

if __name__ == "__main__":
    app.run(debug=True)


