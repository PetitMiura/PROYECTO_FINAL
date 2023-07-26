from datetime import datetime
import sqlite3, requests



class Movement:
    def __init__(self, id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to):
        # Inicializa la clase Movement con sus atributos
        self.id = id
        self.date = date
        self.time = time
        self.moneda_from = moneda_from
        self.cantidad_from = cantidad_from
        self.moneda_to = moneda_to
        self.cantidad_to = cantidad_to


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
                (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES  (?,?,?,?,?,?)
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        # Ejecuta la consulta de inserción con los valores del movimiento
        cur.execute(query, (movement.date, movement.time, movement.moneda_from,
                            movement.cantidad_from, movement.moneda_to, movement.cantidad_to))

        conn.commit()
        conn.close()

    def get(self, id):
        query = """
        SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
        FROM movements
        WHERE id = ?;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        # Ejecuta la consulta de selección con el ID proporcionado
        cur.execute(query)
        res = cur.fetchone()
        conn.close()

        if res is None:
            return None
        # Retorna un objeto Movement creado a partir de los resultados de la consulta
        return Movement(*res)

    def get_all(self):
        query = """
        SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to
        FROM movements;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        res = cur.execute(query)
        lista = []
        for movement in res:
            lista.append(Movement(*movement))       
        #lista = [Movement(*reg) for reg in res], es la conversion de las 3 linias de arriba (list comprenhension) 
        conn.close()
        return lista
    

    

    def saldos():
        connection = sqlite3.connect("data/movements.db")
        cur = connection.cursor()

        criptos = ['EUR', 'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'XRP', 'SOL', 'USDT', 'MATIC']
        saldos = {}
        for cripto in criptos:
            
            query = """SELECT cantidad_to FROM movements WHERE moneda_to = (?) """
            cur.execute(query, (cripto,))
            res = cur.fetchall()
            
            if len(res) > 0:
                total = 0
                for saldo in res:
                    total += saldo[0]
                saldos[cripto] = total
            else:
                saldos[cripto] = 0

        
        for cripto in criptos:
            
            query = """SELECT cantidad_from FROM movements WHERE moneda_from = (?) """
            cur.execute(query, (cripto,))
            res = cur.fetchall()
            
            if len(res) > 0:
                for saldo in res:
                    saldos[cripto] -= saldo[0]

        return saldos
    
    def precio_compra_euros():
        connection = sqlite3.connect("data/movements.db")
        cur = connection.cursor()

        query = """SELECT SUM(cantidad_to) FROM movements WHERE moneda_to = 'EUR'"""
        cur.execute(query)
        result = cur.fetchone()
        total_compra = result[0] if result else 0

        query = """SELECT SUM(cantidad_from) FROM movements WHERE moneda_from = 'EUR'"""
        cur.execute(query)
        result = cur.fetchone()
        total_venta = result[0] if result else 0

        connection.close()

        return total_compra - total_venta

    

                    
