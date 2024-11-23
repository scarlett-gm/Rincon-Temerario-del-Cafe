from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db, Usuario, InfoProducto,CategoriaProducto,CarrioVolatil        
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\LENOVO\Desktop\Rincon-Temerario-del-Cafe-4\Temerarios\backend\baseD.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False  # Solo en desarrollo
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SQLALCHEMY_ECHO'] = True 
app.secret_key = os.urandom(24)  # Cambiar por una clave segura en producción

# Inicializar la base de datos
db.init_app(app)


# Rutas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/Coffeeshop')
def coffeeshop():
    user = session.get('user')
    # Obtener los productos agrupados por categoría
    categorias = db.session.query(
        CategoriaProducto.IdCatePro, 
        CategoriaProducto.NombreCate  # Cambiado a NombreCate
    ).all()
    
    productos_por_categoria = {
        categoria.NombreCate: InfoProducto.query.filter_by(IdCatePro=categoria.IdCatePro).all()
        for categoria in categorias
    }
    
    return render_template(
        'Coffeeshop.html', 
        user=user, 
        productos_por_categoria=productos_por_categoria
    )



@app.route('/carrito')
def carrito():
    # Verificar si el usuario está autenticad
    total = 0
    user = session.get('user') 
    print(f"holaaaa {user}")
    user_id = user['id'] 
    print(f"Hola id {user_id}")
    if 'user' not in session:
        flash('Por favor, inicia sesión para acceder al carrito.', 'error')
        return redirect(url_for('login'))
    vali1 = CarrioVolatil.query.filter_by(IdUser= user_id).all()
    for i in vali1:
        total += float(i.Total)
    print(total)
    
    return render_template('carrito.html', vali1 = vali1, total = total)

@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    user_session = session.get("user")
    
    if not user_session or "id" not in user_session:
        return jsonify({"data": "not_found"}), 404

    user_id = user_session.get("id")
    try:
        # Eliminar todos los productos del carrito del usuario
        CarrioVolatil.query.filter_by(IdUser=user_id).delete()
        db.session.commit()
        return jsonify({"data": "success"})
    except Exception as e:
        print(f"Error al finalizar la compra: {e}")
        return jsonify({"data": "error"}), 500



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("ulises")
        name = request.form["Nombre"]
        apellido = request.form["Apellido"]
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validación básica
        if not all([name, apellido, username, email, password]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('register'))

        # Verificar si el email o username ya existen
        vali1 = Usuario.query.filter_by(Correo=email).first()
        vali2 = Usuario.query.filter_by(username=username).first()
  
        # Debería devolver una lista de usuarios registrados
        if vali1 or vali2:
            print("mama")
            flash('Ya existe una cuenta con este correo electrónico o nombre de usuario.', 'error')
            return redirect(url_for('register'))
        else:
            # Crear nuevo usuario
            print("lee")
            hashed_password = generate_password_hash(password)
            nuevo_usuario = Usuario(
                Nombres=name,
                Apellido=apellido,
                username=username,
                Correo=email,
                Contraseña=hashed_password
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Buscar usuario en la base de datos
        user = Usuario.query.filter_by(username=email).first()
        print(f"Hola me caes mal {user}")
        #print(user.Contraseña)
        if user and check_password_hash(user.Contraseña, password):
            # Guardar información básica del usuario en la sesión
            print("messi")
            print(f"Usuario autenticado: {user}")
            print(f"IdUsuario: {user.IdUsuario}, Username: {user.username}, Correo: {user.Correo}")

            session['user'] = {'id': user.IdUsuario, 'username': user.username, 'email': user.Correo}
            flash('Inicio de sesión exitoso.', 'success')
            print(f"Sesión actual: {session}")
            return redirect(url_for('coffeeshop'))

        flash('Correo o contraseña incorrectos.', 'error')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    # Cerrar sesión
    session.pop('user', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('index'))  # Redirige a la página principal


@app.route('/verify_user', methods=["POST"])
def verify_user():
    # Obtén el diccionario 'user' de la sesión y accede al 'id'
    user_session = session.get("user")
    name = request.form.get("name")
    price = request.form.get("price")
    id = request.form.get("id")
    print(f"Datos en la sesión: {user_session}")
    # Si no hay usuario en la sesión o no tiene 'id', devolver error
    if not user_session or 'id' not in user_session:
        return jsonify({"data": "not_found"}), 404

    user_id = user_session.get("id")
    print(f"ID del usuario extraído de la sesión: {user_id}")

    # Consultar la base de datos por el ID del usuarios
    user = Usuario.query.filter_by(IdUsuario=user_id).first()
    print(f"Usuario encontrado: {user}")

    # Si se encuentra el usuario, devuelve "verify", sino "not_found"
    if user:
        carrito = CarrioVolatil(
            IdUser = user_id,
            Producto = name,
            Cantidad = 1,
            Total = price
        )
        db.session.add(carrito)
        db.session.commit()
        return jsonify({"data": "verify"})
    else:
        return jsonify({"data": "not_found"}), 404
    

@app.route("/eliminar", methods= ["POST"])
def eliminar():
    id = request.form.get("id")
    if not id:
        return jsonify({'data' : 'error'}), 404
    else:
        producto = CarrioVolatil.query.get(id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({"data" : "succces"})
        else:
            return jsonify({'data' : 'error'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
