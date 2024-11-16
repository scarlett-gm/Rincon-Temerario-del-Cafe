"""importamos"""
from flask import Flask
#instanciamos de models (objeto db) db, y baseD (vinculamos)
from models import db, Usuario, Producto, CategoriaProducto, Carrito, Ordenes, Pago, Cupones

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///C:\\Users\\USUARIO\\Rincon-Temerario-del-Cafe\\Temerarios\\backend\\baseD.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos con la app
db.init_app(app)

#las rutas van aca
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        #HOLA
    app.run(debug=True)