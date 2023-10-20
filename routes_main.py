from flask import Flask, render_template, request, redirect, url_for,Blueprint,flash
import sqlite3,datetime,os
from werkzeug.utils import secure_filename
from . import db_manager as db
from .models import Category,Product,User
from .forms import DeleteForm, ItemForm

DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
now = datetime.datetime.utcnow
app = Flask(__name__)
# ruta carpeta imatges
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ruta d'aquesta carpeta

main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route("/")
def hello_world():
    return render_template('hello.html')

def get_db_connection():
    sqlite3_database_path =('database.db')
    con = sqlite3.connect(sqlite3_database_path)
    con.row_factory = sqlite3.Row
    return con

    
@main_bp.route("/list")
def llista_dades():
    datos = db.session.query(Product).all()
    return render_template("products/list.html", datos = datos)
    
@main_bp.route("/products/create", methods = ["GET", "POST"])
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

            
            nou_producte = Product()
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

            return redirect(url_for("main_bp.llista_dades"))
        
    except:

        return ("Error al crear el producte")
    
@main_bp.route("/products/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    item = db.session.query(Product).filter(Product.id == id).one()
    form = ItemForm()

    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.price = form.price.data

        photo = form.photo.data
      
        item.photo = photo.filename

        item.updated = datetime.datetime.now()

        db.session.add(item)
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main_bp.llista_dades'))

    else:
        form.title.data = item.title
        form.description.data = item.description
        form.price.data = item.price
        # Para la foto, no establecemos un valor ya que es un archivo

    return render_template('products/update.html', form=form, item=item)

@main_bp.route("/products/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    item = db.session.query(Product).filter(Product.id == id).one_or_none()
    if item is None:
        flash('Product not found!', 'danger')
        return redirect(url_for('main_bp.list'))
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('main_bp.llista_dades'))

    return render_template('products/delete.html', form=form, item=item)
     
@main_bp.route("/products/read/<int:product_id>")
def ver_producte(product_id):
    producte = db.session.query(Product).filter(Product.id == product_id).one()
    return render_template("products/read.html", producte=producte)