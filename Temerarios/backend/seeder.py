import sqlite3 as sql

DB_PATH = "C:\\Users\\LENOVO\\Desktop\\Rincon-Temerario-del-Cafe-2\\Temerarios\\backend\\baseD.db"


def crear_db():
    """Crear la base de datos y sus tablas"""
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS CategoriaProducto (
            IdCatePro INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreCategoria TEXT NOT NULL
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Usuario (
            IdUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Nombres TEXT NOT NULL,
            Apellido TEXT NOT NULL,
            Correo TEXT NOT NULL UNIQUE,
            Contraseña TEXT NOT NULL
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Producto (
            IdProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            IdCatePro INTEGER NOT NULL,
            Nombre TEXT NOT NULL,
            Precio FLOAT NOT NULL,
            CantidadEnStock INTEGER NOT NULL,
            FOREIGN KEY (IdCatePro) REFERENCES CategoriaProducto(IdCatePro)
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Carrito (
            IdCarrito INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUsuario INTEGER NOT NULL,
            IdProducto INTEGER NOT NULL,
            CantidadPedido INTEGER NOT NULL,
            Fecha TEXT NOT NULL,
            Total FLOAT NOT NULL,
            FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
            FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto)
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Ordenes (
            IdOrden INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUsuario INTEGER NOT NULL,
            IdProducto INTEGER NOT NULL,
            DetallesProducto TEXT NOT NULL,
            Cantidad INTEGER NOT NULL,
            FechaOrden TEXT NOT NULL,
            FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
            FOREIGN KEY (IdProducto) REFERENCES Producto(IdProducto)
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Pago (
            IdPago INTEGER PRIMARY KEY AUTOINCREMENT,
            MetodoPago TEXT NOT NULL,
            IdUsuario INTEGER NOT NULL,
            IdOrden INTEGER NOT NULL,
            TotalPagar FLOAT NOT NULL,
            FechaPago TEXT NOT NULL,
            FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario),
            FOREIGN KEY (IdOrden) REFERENCES Ordenes(IdOrden)
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Cupones (
            IdCupon INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUsuario INTEGER NOT NULL,
            CodigoPromocional TEXT NOT NULL,
            DetallesCupon TEXT NOT NULL,
            FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Info_Producto (
            IdInfoProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            IdCatePro INTEGER NOT NULL,
            NombreProducto TEXT NOT NULL,
            Precio FLOAT NOT NULL,
            Url TEXT NOT NULL,
            FOREIGN KEY (IdCatePro) REFERENCES CategoriaProducto(IdCatePro)
        )"""
    )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CarrioVolatil(
            IdCarrito INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUser INTEGER NOT NULL,
            Producto TEXT NOT NULL,
            Cantidad INTEGER TEXT NOT NULL,
            Total INTEGER NOT NULL,
            FOREING KEY (IdUser) REFERENCES Usuario(IdUsuario)
        )
        """)

    conn.commit()
    conn.close()


def agregar_valor():
    """Agregar valores a la base de datos"""
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()

    # Datos para la tabla CategoriaProducto
    try:
        categorias = [
            ("Tazas",),
            ("Termos",),
            ("Libretas",),
            ("Cafés",),
            ("Postres",),
        ]
        cursor.executemany("""INSERT INTO CategoriaProducto (NombreCategoria) VALUES (?)""", categorias)

        # Datos para la tabla Usuario
        usuarios = [
            ("Carobolita", "Carolina", "Reyes", "carolreyes@gmail.com", "caradebolita123"),
            ("Anitaloquita", "Ana", "Rosales", "anaMaria@gmail.com", "miaumiau12"),
            ("Josesss", "Jose", "Arauz", "josemartinezA@gmail.com", "123opppo"),
        ]
        cursor.executemany("""INSERT INTO Usuario (Username, Nombres, Apellido, Correo, Contraseña) VALUES (?, ?, ?, ?, ?)""", usuarios)

        # Datos para la tabla Info_Producto
        productos = [
            (1, "Taza con Cuchara", 10.99, "Taza3.png"),
            (1, "Taza Negra", 12.99, "Taza4.png"),
            (1, "Taza Blanca", 14.99, "Taza1.png"),
            (2, "Termo Clasico", 10.99, "Termo3.png"),
            (2, "Termo Tipo Stanley", 12.99, "Termo5.png"),
            (2, "Termo Blanco", 14.99, "Termo6.png"),
            (3, "Libreta Clasica Negra", 10.99, "Libreta1.png"),
            (3, "Libreta Verde", 12.99, "Libreta6.png"),
            (3, "Libreta Negra", 14.99, "Libreta7.png"),
            (4, "Café con Vainilla", 10.99, "vainilla.png"),
            (4, "Café con Chocolate", 12.99, "Chocolate.png"),
            (4, "Cafe Puro", 14.99, "Cafépuro.png"),
            (5, "Selva Negra", 10.99, "selvanegra.png"),
            (5, "Red Velvet", 12.99, "redvelvet.png"),
            (5, "Tres Leches", 14.99, "tresleches.png"),
        ]
        cursor.executemany("""INSERT INTO Info_Producto (IdCatePro, NombreProducto, Precio, Url) VALUES (?, ?, ?, ?)""", productos)

        conn.commit()
    except sql.Error as e:
        print(f"Error al insertar datos: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    crear_db()
    print("roger mama huevo")
    agregar_valor()
