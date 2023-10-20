
import datetime
now = datetime.datetime.utcnow
from . import db_manager as db



# categories
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    slug = db.Column(db.Text, nullable=False, unique=True)

# taula products
class Product(db.Model):
    __tablename__ = "products"
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title   = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo   = db.Column(db.Text, nullable=False)
    price   = db.Column(db.Numeric(10,2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    seller_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created     = db.Column(db.DateTime, default=now)
    updated     = db.Column(db.DateTime, default=now)


# taula users

class User(db.Model):
    __tablename__ = "users"
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.Text, nullable=False, unique=True)
    email   = db.Column(db.Text, nullable=False, unique=True)
    password= db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=now)
    update  = db.Column(db.DateTime, default=now)
