from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.admin import AdminClient
import pyodbc
import time
import os
import sys
import ssl
print(ssl.OPENSSL_VERSION,flush=True)
import ctypes.util
import json
print(ctypes.util.find_library('ssl'),flush=True)
print(sys.executable,flush=True)
sys.path.append('')
print("path" , sys.path,flush=True)
print("driver pyodbc : ",pyodbc.drivers(),flush=True)
from dotenv import load_dotenv

load_dotenv()

######## Config general :

## Postgre :
server = os.getenv('SQL_SERVER',"localhost")
port = os.getenv('SQL_PORT') 
if port is None : 
    port = os.getenv("SQL_PORT_LOCAL")
database = "mydb"
username = "quentin"

pwd_file =  os.path.join('.', 'data', 'postgre_pwd.txt')
with open(pwd_file) as f :
    password = f.read()

# Construire la chaîne de connexion
connection_string = f"DRIVER={{PostgreSQL Unicode}};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};"


## kafka : 

kafka_server = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
if kafka_server is None : 
    kafka_server = 'localhost:' + os.getenv("KAFKA_PORT_LOCAL")
topic_name = os.getenv('KAFKA_TOPIC', 'test-topic-init')

# # Wait topic have been created : 

# Fonction pour vérifier si le topic existe
def wait_for_topic_creation(topic, timeout=3600):
    admin_client = AdminClient({'bootstrap.servers': kafka_server})
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # Lister les topics existants
        topics_metadata = admin_client.list_topics(timeout=10).topics
        if topic in topics_metadata:
            print(f"Topic {topic} trouvé.",flush=True)
            return True
        print(f"En attente de la création du topic {topic}...",flush=True)
        time.sleep(5)

    raise KafkaException(f"Le topic {topic} n'a pas été trouvé après {timeout} secondes.")

# Attendre que le topic soit créé
wait_for_topic_creation(topic_name)

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': kafka_server,  # Adresse du serveur Kafka
    'group.id': 'my-consumer-group',        # Identifiant du groupe de consommateurs
    'auto.offset.reset': 'earliest'         # Commence à lire les messages depuis le début si aucun offset n'est défini
}

# Créer le consommateur
consumer = Consumer(consumer_config)

# Abonner le consommateur à un ou plusieurs topics
consumer.subscribe([topic_name])

# Lire les messages depuis le topic
try:
    while True:
        msg = consumer.poll(1)  # Attend jusqu'à 1 seconde pour recevoir un message

        if msg is None:
            continue  # Si aucun message n'est reçu, continue la boucle
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Fin de la partition atteinte
                print(f"Fin de partition : {msg.topic()} [{msg.partition()}] offset {msg.offset()}",flush=True)
            else:
                print(f"Erreur : {msg.error()}",flush=True)
        else:
            # Afficher le message reçu
            msg_to_print = msg.value().decode('utf-8')
            print(f"Message reçu : {msg_to_print},with type {type(msg_to_print)}",flush=True)

            message_dict = json.loads(msg_to_print)

        try:
            conn = pyodbc.connect(connection_string)

            insert_query = """
            INSERT INTO sensor_data (sensor_id, temperature, humidity, msg)
            VALUES (?, ?, ?, ?);
            """
            # Se connecter à la base de données
            cursor = conn.cursor()

            # Exécuter l'insertion
            cursor.execute(insert_query, 
                           message_dict['sensor_id'], 
                           message_dict['temperature'], 
                           message_dict['humidity'], 
                           message_dict['msg'])

            # Valider la transaction
            conn.commit()

            print("Données insérées avec succès !",flush=True)

            # Fermer la connexion
            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}",flush=True)


except KeyboardInterrupt:
    # Interrompre le consommateur proprement avec Ctrl+C
    pass
finally:
    # Fermer le consommateur correctement
    consumer.close()


# Requête d'insertion SQL

