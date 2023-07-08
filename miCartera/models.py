from datetime import datetime
import sqlite3

class Movement:
    def __init__(self, id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, precio_unidad):
        # Inicializa la clase Movement con sus atributos
        self.id = id
        self.date = date
        self.time = time
        self.moneda_from = moneda_from
        self.cantidad_from = cantidad_from
        self.moneda_to = moneda_to
        self.cantidad_to = cantidad_to
        self.precio_unidad = precio_unidad


class MovementsDAOsqlite:
    def __init__(self, db_path):
        self.path = db_path

        # Crea la tabla "movements" si no existe
        query = """
        CREATE TABLE IF NOT EXISTS "movements" (
            "id"	INTEGER UNIQUE,
            "date"	TEXT NOT NULL,
            "time"	TEXT NOT NULL,
            "moneda_from"	TEXT NOT NULL,
            "cantidad_from"	REAL NOT NULL,
            "moneda_to"	TEXT NOT NULL,
            "cantidad_to"	REAL NOT NULL,
            "precio_unidad" REAL NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()

    def insert(self, movement):
        query = """
        INSERT INTO movements
                (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, precio_unidad)
        VALUES  (?,?,?,?,?,?)
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        # Ejecuta la consulta de inserción con los valores del movimiento
        cur.execute(query, (movement.date, movement.time, movement.moneda_from,
                            movement.cantidad_from, movement.moneda_to, movement.cantidad_to, movement.precio_unidad))

        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, precio_unidad
        FROM movements
        WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        # Ejecuta la consulta de selección con el ID proporcionado
        cur.execute(query, (id,))
        res = cur.fetchone()
        conn.close()

        if res is None:
            return None
        # Retorna un objeto Movement creado a partir de los resultados de la consulta
        return Movement(*res)

    def get_all(self):
        query = """
        SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, precio_unidad
        FROM movements
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(query)
        result = cur.fetchall()
        conn.close()

        # Return a list of Movement objects
        return [Movement(*res) for res in result]

    def update(self, movement):
        query = """
        UPDATE movements
        SET date = ?, time = ?, moneda_from = ?, cantidad_from = ?, moneda_to = ?, cantidad_to = ?, precio_unidad = ?
        WHERE id = ?
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(query, (movement.date, movement.time, movement.moneda_from,
                            movement.cantidad_from, movement.moneda_to, movement.cantidad_to, movement.precio_unidad, movement.id))

        conn.commit()
        conn.close()

    def delete(self, id):
        query = """
        DELETE FROM movements
        WHERE id = ?
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(query, (id,))

        conn.commit()
        conn.close()