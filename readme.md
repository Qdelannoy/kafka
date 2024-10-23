
# Pré-requis :

## Execution WSL : 

Si besoin d'executer docker dans WSL, 
Utiliser : 

cd /mnt/d/Documents/kafka/

pour être dans le bon dossier

## Lancement du service kafka : 


Le fichier docker-compose permet d'executer kafka qui depend de zookeeper. 


Il s'execute avec la commande : docker-compose up ou docker-compose up -d pour une execution en arriére plan 

Remarque : par defaut le service qui sera lancé portera le nom du dossier qui le contient.

Ce script est équivalent aux deux docker run suivant : 

--lancement de zookeeper
docker run -d --name zookeeper -p 2181:2181 \
  -e ZOOKEEPER_CLIENT_PORT=2181 \
  -e ZOOKEEPER_TICK_TIME=2000 \
  confluentinc/cp-zookeeper:7.5.0

-- lancement de kafka en utilisant : 
docker run -d --name kafka -p 9092:9092 \
  --link zookeeper:zookeeper \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:7.5.0

## arrêt des service en cours d'execution : 

Pour arrêt les service il faut lancer : 

 - docker-compose down depuis le dossier qui contient le docker compose 
 - Ou docker-compose -f /chemin/vers/ton/fichier/docker-compose.yml down

# Creation de topic : 

## avec un script d'init : 

La grosse difficulté lié à cette vision est la suivante, les server:port comme KAFKA_ADVERTISED_LISTENERS ont du mal à fonctionné en interne et externe : 

- Si on met localhost/9092 on peut intéroger depuis l'extérieur mais la script de creation de topic ne fonctionne pas (ref au server localhost:9092 ne fonctionne pas)
- Si on met kafka/9092 on peut pas l'intéroger facilement depuis l'extérieur mais la creation de topic fonctionne

C'est pour cette raison que le script est aussi compliqué car il permet de combiner les deux.

Sans utiliser de volume docker recrééer systématiquement le topic ce qui va lui perméttre de fonctionner. Cependant les données seront perdus

## A la main : 
Pour pouvoir créeer des topic, il faut pouvoir rentrer dans le conteneur kafka qui est en cours d'execution. Dans mon cas cela correspond à la commande : 

docker exec -it kafka-kafka-1 /bin/bash

Si on ne connait pas le nom du docker : docker ps permet de le connaitre. 

Finalement on peut crééer un topic grâce au commande contenu dans les fichier create_topic.bat (En dehors du conteneur) ou create_topic.sh (dans le conteneur)

# TODO : 

- Centraliser au maximum les informations sur les variable dans le docker-compose
- Connexion à une bdd postgre exitante au lieu d'en crééer une
- Sécuriser l'accés aux APIs avec Traefik
- Fixer les version des dépendances installé avec apt-get voir les monters ?
-Push git Attention au git-ignore
- étude des logs kafka etc pour voir si on peut opti
- ajouter la db dans la base de données init

# Erreur rencontré : 

## Driver postgre : 

L'erreur rencontré été la suivante : 

('IM003', "[IM003] Le pilote spécifié n'a pas été chargé en raison de l'erreur système  127: La procédure spécifiée est introuvable. (PostgreSQL Unicode(x64), C:\\Program Files\\psqlODBC\\1700\\bin\\psqlodbc35w.dll). (160) (SQLDriverConnect)"). 

Elle se produisait lors d'une connexion essayé à travers un script python mais dans dans le jupyter notebook. Pour corriger ce problème, un import explicite de la librairie ssl à permis de résoudre le pb. 


## Problème de cluster ID (kafka): 

kafka-kafka-1         | kafka.common.InconsistentClusterIdException: The Cluster ID eFur_aPPT0unsXaLNoS_wg doesn't match stored clusterId Some(_gn_mq-yTYGCoJwYx5nkCw) in meta.properties. The broker is trying to join the wrong cluster. Configured zookeeper.connect may be wrong

Ce problème se produit lorsque les données de zookeeper ne persiste pas et on a donc un mismatch entre le cluster ID qui persiste grâce au volume de l'image kafka et celui qui se trouve dans les meta data (meta.properties) de zookeeper. 

Ces lignes ont permi de résoudre le problème (dans l'image zookeeper): 
    volumes : 
      - zookeeper-data:/var/lib/zookeeper/data
      - zookeeper-datalog:/var/lib/zookeeper/log

