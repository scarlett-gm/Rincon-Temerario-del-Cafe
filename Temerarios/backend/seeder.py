"""Importamos sql"""
import sqlite3 as sql

DB_PATH="C:\\Users\\LENOVO\\Desktop\\Rincon-Temerario-del-Cafe-2\\Temerarios\\backend\\baseD.db"

#funcion para crear la conexion
def crear_db():
    """Creamos"""
    conn=sql.connect(DB_PATH)
    cursor=conn.cursor()

    cursor.execute(
        """ CREATE TABLE Usuario (
        IdUsuario INT PRIMARY KEY,
        Username TEXT,
        Nombres TEXT,
        Apellido TEXT,
        Correo TEXT,
        Contraseña TEXT
    )"""
    )

    cursor.execute(
        """CREATE TABLE Producto (
        IdProducto INT PRIMARY KEY,
        IdCatePro INT,
        Nombre TEXT,
        Precio FLOAT,
        CantidadEnStock INTEGER,
        FOREIGN KEY (IdCatePro) REFERENCES CategoriaProducto(IdCatePro)
    )"""
    )

    cursor.execute(
        """CREATE TABLE CategoriaProducto (
        IdCatePro INT PRIMARY KEY,
        NombreCategoria TEXT
    )"""
    )

    cursor.execute(
        """CREATE TABLE Carrito (
        IdCarrito INT PRIMARY KEY,
        IdUsuario INT,
        IdProducto INT,
        CantidadPedido INT,
        Fecha TEXT,
        Total FLOAT,
        FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
        FOREIGN KEY (IdUsuario) REFERENCES Producto(IdProducto)
    )"""
    )

    cursor.execute(
        """CREATE TABLE Ordenes (
        IdOrden INT PRIMARY KEY,
        IdUsuario INT,
        IdProducto INT,
        DetallesProducto TEXT,
        Cantidad INT,
        FechaOrden TEXT,
        FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
        FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto)
    )"""
    )

    cursor.execute(
        """CREATE TABLE Pago (
        IdPago INT PRIMARY KEY,
        MetodoPago TEXT,
        IdUsuario INT,
        IdOrden INT,
        TotalPagar FLOAT,
        FechaPago TEXT,
        FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
        FOREIGN KEY (IdOrden) REFERENCES Ordenes(IdOrden)

    )"""
    )
    cursor.execute(
        """CREATE TABLE Cupones (
        IdCupon INT PRIMARY KEY,
        IdUsuario INT,
        CodigoPromocional TEXT,
        DetallesCupon TEXT,
        FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
    )"""
    )
    conn.commit()
    conn.close()

def agregar_valor():
    """Agregamos valores a mi base de datos para probar"""
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()

    # Datos para la tabla Usuario
    data = [
        (1, "Carobolita", "Carolina", "Reyes", "carolreyes@gmail.com", "caradebolita123"),
        (2, "Anitaloquita", "Ana", "Rosales", "anaMaria@gmail.com", "miaumiau12"),
        (3, "Josesss", "Jose", "Arauz", "josemartinezA@gmail.com", "123opppo")
    ]
    cursor.executemany("""INSERT INTO Usuario VALUES (?, ?, ?, ?, ?, ?)""", data)

    # Datos para la tabla Producto
    data2 = [
        (1, 1, "Selva negra", 10.00, 10)
    ]
    cursor.executemany("""INSERT INTO Producto VALUES (?, ?, ?, ?, ?)""", data2)

    # Datos para la tabla CategoriaProducto
    data3 = [
        (1, "Postres")
    ]
    cursor.executemany("""INSERT INTO CategoriaProducto VALUES (?, ?)""", data3)

    # Datos para la tabla Carrito
    data4 = [
        (1, 1, 1, 2, "2024-11-15", 20.00),
        (2, 2, 1, 1, "2024-11-15", 10.00),
        (3, 3, 1, 3, "2024-11-15", 30.00)
    ]
    cursor.executemany("""INSERT INTO Carrito VALUES (?, ?, ?, ?, ?, ?)""", data4)

    # Datos para la tabla Ordenes
    data5 = [
        (1, 1, 1, "Selva negra", 2, "2024-11-15"),
        (2, 2, 1, "Selva negra", 1, "2024-11-15"),
        (3, 3, 1, "Selva negra", 3, "2024-11-15")
    ]
    cursor.executemany("""INSERT INTO Ordenes VALUES (?, ?, ?, ?, ?, ?)""", data5)

    # Datos para la tabla Pago
    data6 = [
        (1, "Tarjeta de crédito", 1, 1, 20.00, "2024-11-15"),
        (2, "PayPal", 2, 2, 10.00, "2024-11-15"),
        (3, "Efectivo", 3, 3, 30.00, "2024-11-15")
    ]
    cursor.executemany("""INSERT INTO Pago VALUES (?, ?, ?, ?, ?, ?)""", data6)

    # Datos para la tabla Cupones
    data7 = [
        (1, 1, "DESCUENTO10", "10% de descuento en tu próxima compra"),
        (2, 2, "BIENVENIDO15", "15% de descuento para nuevos clientes"),
        (3, 3, "FIESTA20", "20% de descuento en compras mayores a $50")
    ]
    cursor.executemany("""INSERT INTO Cupones VALUES (?, ?, ?, ?)""", data7)

    conn.commit()
    conn.close()


if __name__== "__main__":
    crear_db()
    print("Hola")
    agregar_valor()
