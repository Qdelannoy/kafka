#!/bin/bash

# set the working directory
cd /usr/local/bin

# instalation des dépendances pour odbc : 

# Installer les dépendances pour les pilotes ODBC
apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer les pilotes PostgreSQL pour ODBC
apt-get update && apt-get install -y \
    odbc-postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/

# Instalation des dependance python : 

pip install -r /usr/local/bin/requirements.txt

# Installer netcat pour avoir la command nc.
# déja dispo dans create_topic.sh car l'image confluentinc/cp-kafka:7.5.0 la contient
apt-get update && apt-get install -y netcat-openbsd


# Fonction pour vérifier si Kafka est prêt
function wait_for_postgre() {
  echo "Attente que postgre soit prêt sur le port ${SQL_PORT} du server ${SQL_SERVER} ..."
  while ! nc -z ${SQL_SERVER} ${SQL_PORT} ; do   
    echo "Postgre n'est pas encore prêt... attente de 1 seconde."
    sleep 1 # Attendre 1 seconde avant de vérifier à nouveau
  done
  echo "Postgre est prêt."
}

# Fonction pour vérifier si Kafka est prêt
function wait_for_kafka() {
  echo "Attente que Kafka soit prêt sur ${KAFKA_BOOTSTRAP_SERVERS}..."
  while ! nc -z kafka 9092; do   
    echo "Kafka n'est pas encore prêt... attente de 1 seconde."
    sleep 1 # Attendre 1 seconde avant de vérifier à nouveau
  done
  echo "Kafka est prêt."
}

# # Fonction pour vérifier si le topic existe
# function wait_for_topic() {

#   echo "Vérification de l'existence du topic ${KAFKA_TOPIC}..."

#   # Boucle jusqu'à ce que le topic soit trouvé
#   while true; do
#     docker exec kafka-kafka-1 /usr/bin/kafka-topics --list --bootstrap-server ${KAFKA_BOOTSTRAP_SERVERS} | grep -w ${KAFKA_TOPIC}
#     if [ $? -eq 0 ]; then
#       echo "Le topic ${KAFKA_TOPIC} existe déjà."
#       break
#     else
#       echo "Le topic ${KAFKA_TOPIC} n'existe pas encore... Attente de 5 secondes."
#       sleep 5
#     fi
#   done
# }

# Appel des fonctions
wait_for_postgre
wait_for_kafka
# wait_for_topic


# Lancer le consommateur Python une fois que le topic est créé
echo "Lancement du consommateur Python..."
python3 -u /usr/local/bin/python_consumer.py
