from controller.database import db

class User(db.Model):
    __tablename__ = 'user'  # <-- corrected
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    city = db.Column(db.String(50))
    flag = db.Column(db.Integer, default=0)

class Role(db.Model):
    __tablename__ = 'role'  # <-- corrected
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class UserRole(db.Model):
    __tablename__ = 'user_role'  # <-- corrected
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
