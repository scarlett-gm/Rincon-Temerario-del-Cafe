from flask import Flask, redirect, url_for, render_template

from backend.models import db, Usuario, Producto, CategoriaProducto, Carrito, Ordenes, Pago, Cupones

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\LENOVO\Desktop\Rincon-Temerario-del-Cafe-2\Temerarios\backend\baseD.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# as
# Inicializamos la base de datos con la app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/Coffeeshop')
def Coffeeshop():
    return render_template('Coffeeshop.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
