import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.executescript("""
DROP TABLE IF EXISTS orang;
DROP TABLE IF EXISTS nikah;
DROP TABLE IF EXISTS ortu;

CREATE TABLE orang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    jk TEXT
);

CREATE TABLE nikah (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suami INTEGER,
    istri INTEGER
);

CREATE TABLE ortu (
    anak_id INTEGER,
    ayah INTEGER,
    ibu INTEGER
);
""")

con.commit()
con.close()


