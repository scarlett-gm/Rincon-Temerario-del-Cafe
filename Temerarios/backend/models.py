"""importamos sqlAlchemy"""
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Usuario (db.Model):
    """Tabla Usuario"""
    __tablename__ = 'Usuario'
    IdUsuario=db.Column(db.Integer, primary_key=True, nullable=False)
    username=db.Column(db.String(50), unique=True, nullable=False)
    Nombres=db.Column(db.String(50), nullable=False)
    Apellido=db.Column(db.String(50), nullable=False)
    Correo=db.Column(db.String(50), unique=True, nullable=False)
    Contraseña=db.Column(db.String(50), nullable=False)

    # Relaciones
    carrito = db.relationship('Carrito', backref='usuario', lazy=True)
    ordenes = db.relationship('Ordenes', backref='usuario', lazy=True)
    cupones = db.relationship('Cupones', backref='usuario', lazy=True)
    
class Producto(db.Model):
    """Tabla Producto"""
    __tablename__ = 'Producto'
    IdProducto = db.Column(db.Integer, primary_key=True, nullable=False)
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.IdUsuario'))
    NombreP = db.Column(db.String(50))
    Precio = db.Column(db.Integer)
    CantidadStock = db.Column(db.Integer)

    # Clave foránea para CategoriaProducto
    IdCatePro = db.Column(db.Integer, db.ForeignKey('Categoria_Producto.IdCatePro'), nullable=False)

    # Relación opcional (ya gestionada por CategoriaProducto)
    carrito = db.relationship('Carrito', backref='producto', lazy=True)
    ordenes = db.relationship('Ordenes', backref='producto', lazy=True)

class CategoriaProducto(db.Model):
    """Tabla Categoria del Producto"""
    __tablename__ = 'Categoria_Producto'
    IdCatePro = db.Column(db.Integer, primary_key=True)
    NombreCate = db.Column(db.String(80), nullable=False, unique=True)

    # Relación inversa hacia Producto
    productos = db.relationship('Producto', backref='categoria_producto', lazy=True)

class Carrito(db.Model):
    """Tabla Carrito de compras"""
    __tablename__ = 'Carrito'
    IdCarrito=db.Column(db.Integer, primary_key=True)
    IdUsuario=db.Column(db.Integer, db.ForeignKey('Usuario.IdUsuario'))
    IdProducto=db.Column(db.Integer, db.ForeignKey('Producto.IdProducto'))
    CantidadP=db.Column(db.Integer)
    Fecha=db.Column(db.String(50))
    Total=db.Column(db.Float)

class Ordenes (db.Model):
    """Tabla Ordenes"""
    __tablename__='Ordenes'
    IdOrden=db.Column(db.Integer, primary_key=True)
    IdUsuario=db.Column(db.Integer, db.ForeignKey('Usuario.IdUsuario'))
    IdProducto=db.Column(db.Integer, db.ForeignKey('Producto.IdProducto'))
    DetallesP=db.Column(db.String(80))
    Cantidad=db.Column(db.Integer)
    FechaOrden=db.Column(db.String(50))

class Pago(db.Model):
    """Tabla de pago que gestionará y tendrá control del pago de orden"""
    __tablename__ = 'Pago'
    IdPago = db.Column(db.Integer, primary_key=True)
    MetodoPago = db.Column(db.String(50), nullable=False)
    IdOrden = db.Column(db.Integer, db.ForeignKey('Ordenes.IdOrden'))  # Aquí cambia de 'Orden.IdOrden' a 'Ordenes.IdOrden'
    IdUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.IdUsuario'))
    TotalPagar = db.Column(db.Integer)
    FechaPago = db.Column(db.String(50))

class Cupones(db.Model):
    """Tabla de Cupones que tendra el cliente"""
    __tablename__='Cupones'
    IdCupon=db.Column(db.Integer, primary_key=True)
    IdUsuario=db.Column(db.Integer, db.ForeignKey('Usuario.IdUsuario'))
    CodigoPromocional=db.Column(db.String(50))
    detallesCupon=db.Column(db.String(50))

class InfoProducto(db.Model):
    """Tabla Info_Producto"""
    __tablename__ = 'Info_Producto'
    IdProducto = db.Column(db.Integer, primary_key=True, nullable=False)
    IdCatePro = db.Column(db.Integer, db.ForeignKey('Categoria_Producto.IdCatePro'), nullable=False)
    NombreProducto = db.Column(db.String(100), nullable=False)
    Precio = db.Column(db.Integer, nullable=False)
    Url = db.Column(db.String(100))
    
    categoria = db.relationship('CategoriaProducto', backref='info_productos', lazy=True)
