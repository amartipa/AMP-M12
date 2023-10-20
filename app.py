from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3,datetime,os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.utils import secure_filename

DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
now = datetime.datetime.utcnow
app = Flask(__name__)
# ruta carpeta imatges
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ruta d'aquesta carpeta
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/database.db"
# mostrar sql
app.config["SQLALCHEMY_ECHO"] = True

# Inicio SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# categories
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    slug = db.Column(db.Text, nullable=False, unique=True)

# taula orders
 
# class Order(db.Model):
#     __tablename__ = "orders"
#     id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id  = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
#     buyer_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     created     = db.Column(db.DateTime, default=now)
#     UniqueConstraint("product_id", "buyer_id", name="uc_product_buyer")

# taula confirmed_orders
# class Confirmed_order(db.Model):
#     __tablename__ = "confirmed_orders"
#     order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
#     created = db.Column(db.DateTime, default=now, )


# taula products
class product(db.Model):
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

class user(db.Model):
    __tablename__ = "users"
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.Text, nullable=False, unique=True)
    email   = db.Column(db.Text, nullable=False, unique=True)
    password= db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=now)
    update  = db.Column(db.DateTime, default=now)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return render_template('hello.html')

def get_db_connection():
    sqlite3_database_path =('database.db')
    con = sqlite3.connect(sqlite3_database_path)
    con.row_factory = sqlite3.Row
    return con

    
@app.route("/list")
def llista_dades():
    datos = db.session.query(product).all()
    return render_template("products/list.html", datos = datos)
    
@app.route("/products/create", methods = ["GET", "POST"])
def crearProducte():
    try:
        if request.method == 'GET':
            return render_template('/products/create.html')
        elif request.method == 'POST':
            datos = request.form
            titulo = datos.get("titulo")
            desc = datos.get("descripcion")       
            precio= int(datos.get("precio"))
            foto = request.files['foto'].filename
            created = datetime.datetime.now()
            updated = datetime.datetime.now()
            archivo = request.files['foto']
            filename = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            nou_producte = product()
            nou_producte.title = titulo
            nou_producte.description = desc
            nou_producte.photo = foto
            nou_producte.price = precio
            nou_producte.seller_id = 1
            nou_producte.category_id = 1
            nou_producte.created = created
            nou_producte.updated = updated

            db.session.add(nou_producte)
            db.session.commit()

            return redirect(url_for("llista_dades"))
        
    except:

        return ("Error al crear el producte")
    
@app.route("/products/update/<int:product_id>", methods = ['POST', 'GET'])
def updateProduct(product_id):
    producte = db.session.query(product).filter(product.id == product_id).one()

    if request.method == 'GET':
        datos = db.session.query(product).filter(product.id == product_id).one()
        app.logger.info(datos) 
        return render_template("/products/update.html", datos = datos)
    else:
        titol = request.form['titulo']
        desc = request.form['descripcion']
        foto = request.files['foto'].filename
        archivo = request.files['foto']
        filename = secure_filename(archivo.filename)
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        precio = float(request.form['precio'])

        producte.title = titol
        producte.description = desc
        producte.photo = foto
        producte.price = precio

        db.session.add(producte)
        db.session.commit()

        return redirect(url_for("llista_dades"))
    

@app.route("/products/delete/<int:product_id>", methods=["GET"])
def eliminar_producte(product_id):
    producte = db.session.query(product).filter(product.id == product_id).first()
    if producte:
        db.session.delete(producte)
        db.session.commit()
    return redirect(url_for("llista_dades"))

@app.route("/products/read/<int:product_id>")
def ver_producte(product_id):
    producte = db.session.query(product).filter(product.id == product_id).one()
    return render_template("products/read.html", producte=producte)