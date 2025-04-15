import sqlite3

# Connexion à la base (elle sera créée si elle n'existe pas)
conn = sqlite3.connect("db.sqlite")

# Création de la table
conn.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    content TEXT,
    direction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("Base de données initialisée ✅")
