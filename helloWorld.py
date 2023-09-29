from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3,datetime,os
from werkzeug.utils import secure_filename

DATABASE = 'database.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return render_template('hello.html')

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

def get_db_connection():
    sqlite3_database_path =('database.db')
    con = sqlite3.connect(sqlite3_database_path)
    con.row_factory = sqlite3.Row
    return con



# @app.route("/list")
# def llista_dades():
#     try: 
#         conectar = get_db_connection()
#         cursor = conectar.cursor()
#         cursor.execute("SELECT * from products")
#         resultado = cursor.fetchall()
#         cursor.close()
#         conectar.close()
#         return render_template('products/list.html', datos = resultado)
#     except Exception as e:
#         return str(e), 500
    
@app.route("/list")
def llista_dades():
    try: 
        with get_db_connection() as con:
            res = con.execute("SELECT * FROM products")
            datos = res.fetchall()
        return render_template("products/list.html", datos = datos)
    except Exception as e:
        return str(e), 500
    
@app.route("/products/create", methods = ["GET", "POST"])
def crearProducte():
    # try:
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

            

            with get_db_connection() as con:
                sql = "INSERT into products(title, description, photo, price, created, updated) VALUES(?,?,?,?,?,?)" 
                con.execute(sql,(titulo, desc, foto, precio, created, updated))
                con.commit()
                con.close
            return redirect(url_for("llista_dades"))
        
    # except:

    #     return ("Error al crear el producte")
    



