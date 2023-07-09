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