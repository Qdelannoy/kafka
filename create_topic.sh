#!/bin/bash

echo "Waiting for ZooKeeper to start..."
while ! nc -z zookeeper 2181; do   
  sleep 1 # Attendre 1 seconde avant de réessayer
done

# Attendre que Kafka soit prêt
while ! nc -z kafka 9092; do   
  echo "Attente de Kafka pour être prêt..."
  sleep 1 # Attendre 1 seconde avant de vérifier à nouveau
done

# Nom du topic
TOPIC_NAME="test-topic-init-bis"

# Vérifier si le topic existe déjà
if /usr/bin/kafka-topics --list --bootstrap-server kafka:9092 | grep -q "$TOPIC_NAME"; then
    echo "Le topic '$TOPIC_NAME' existe déjà."
else
    # Créer le topic si il n'existe pas
    /usr/bin/kafka-topics --create --topic "$TOPIC_NAME" --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1 
    echo "Topic '$TOPIC_NAME' créé avec succès."
fi