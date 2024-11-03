# DNS et ip pour les services (conteneur) :

chaque conteneur (service) à sa propre adresse ip relative au réseau qui permet de au conteneur de communiquer les uns avec les autres.

Chacune de ces adresses ip possède un DNS correspondant au nom du conteneur. 

par exemple ici kafka, zoopkeeper etc



# Commande bash: 

pour retrouver les infos sur les objets <compose>-<service>-<instance> : 

sudo docker ps

Pour voir les log d'un conteneur :
sudo docker logs -f <compose>-<service>-<instance>

Pour exectuer une commande particuliére dans un conteneur particuier : 
sudo docker exec -it <compose>-<service>-<instance> command --args

Si on veut rentrer dans le docker avec bash : 

sudo docker exec -it <compose>-<service>-<instance> /bin/bash

# Fonctionnement : 

## vocabulaire : 

image : définit par un dockerfile c'est aussi ce qu'on trouve dans le docker hub (p.ex : 'python:3.11')

conteneur : c'est une instance d'une image 

docker-compose : application multi-conteneur (définit par la commande services)

## Commande / arguments docker-compose : 

depend_on : indique dans quel ordre lancer les service. Attention : ça ne veut pas dire que le service est prêt. 

