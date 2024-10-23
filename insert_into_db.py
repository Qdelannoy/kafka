import pyodbc
import time
import os
import sys
import ssl
import ctypes.util
print(ctypes.util.find_library('ssl'))
print(ssl.OPENSSL_VERSION)
print(sys.executable)
sys.path.append('')
print("path" , sys.path)

# Chemin vers le fichier
file_path = r"C:\Program Files\psqlODBC\1700\bin\psqlodbc35w.dll"

# Vérifie si le fichier existe
if os.path.exists(file_path):
    print(f"Le fichier existe à : {file_path}")
else:
    print(f"Le fichier n'existe pas à : {file_path}")

# Remplacer par tes informations de connexion
server = "localhost"
port = "5433"          # Utilise 5433 si tu as configuré PostgreSQL pour un autre port
database = "mydb"
username = "quentin"

with open("D:\Documents\kafka\data\postgre_pwd.txt") as f :
    password = f.read()

# Construire la chaîne de connexion
connection_string = f"DRIVER={{PostgreSQL Unicode(x64)}};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};"

conn = pyodbc.connect(connection_string)

# Dictionnaire à insérer
message = {
    'sensor_id': '1234',
    'temperature': 25.6,
    'humidity': 60,
    'msg': "Message received"
}

# Requête d'insertion SQL
insert_query = """
    INSERT INTO sensor_data (sensor_id, temperature, humidity, msg)
    VALUES (?, ?, ?, ?);
"""

try:
    # Se connecter à la base de données
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Exécuter l'insertion
    cursor.execute(insert_query, message['sensor_id'], message['temperature'], message['humidity'], message['msg'])

    # Valider la transaction
    conn.commit()

    print("Données insérées avec succès !")

    # Fermer la connexion
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Erreur lors de l'insertion : {e}")

