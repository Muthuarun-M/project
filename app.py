from flask import Flask, render_template,request, redirect, url_for, flash,session
from controller.database import db
import sqlite3
from controller.confige import Confige
from controller.model import *
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object(Confige)
db.init_app(app)

with app.app_context():
    # Create tables
    db.create_all()

    # Create roles if they don't exist
    roles = [
        {'role_id': 1, 'name': 'admin'},
        {'role_id': 2, 'name': 'staff'},
        {'role_id': 3, 'name': 'student'}
    ]

    for r in roles:
        existing_role = db.session.get(Role, r['role_id'])
        if not existing_role:
            db.session.add(Role(role_id=r['role_id'], name=r['name']))
    db.session.commit()

    # Create admin user if not exists
    admin_email = 'admin@gmail.com'
    admin_user = db.session.query(User).filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email=admin_email,
            password=generate_password_hash('admin123'),
            name='Admin User',
            phone='1234567890',
            city='Admin City',
            flag=1

        )
        db.session.add(admin_user)
        db.session.commit()

        # Assign admin role
        admin_role = db.session.query(Role).filter_by(name='admin').first()
        user_role = UserRole(user_id=admin_user.user_id, role_id=admin_role.role_id)
        db.session.add(user_role)
        db.session.commit()



@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]
        country = request.form["country"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            msg = "Passwords do not match!"
            return render_template("register.html", msg=msg)

        # Hash password
        hashed_password = generate_password_hash(password)

        # Save to database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT,
                username TEXT,
                email TEXT,
                phone TEXT,
                city TEXT,
                country TEXT,
                password TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO users (fullname, username, email, phone, city, country, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fullname, username, email, phone, city, country, hashed_password))

        conn.commit()
        conn.close()

        msg = "Registration Successful!"
        return render_template("register.html", msg=msg)

    return render_template("register.html", msg=msg)
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, username))
        user = cursor.fetchone()
        conn.close()

        if user:
            # user[7] = password column (based on register table structure)
            if check_password_hash(user[7], password):
                session["user"] = user[1]  # fullname
                return redirect(url_for("welcome"))
            else:
                msg = "Incorrect password!"
        else:
            msg = "User not found!"

    return render_template("login.html", msg=msg)


@app.route("/welcome")
def welcome():
    if "user" in session:
        return render_template("welcome.html", username=session["user"])
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)