
# L'API

L'API gère l'authentification des utilisateurs. Les utilisateurs acceptés sont 

* username : alice password : wonderland
* username : bob password : builder
* username : clementine password : mandarine 
* username : admin password : admin

La base des credentials est disponible en json dans l'api, encodé en base64 avec un secret (fichier secret.txt). En prod, ce secret est dans kubernetes et est lu comme variable d'environnement, mais en local, l'appli tourne en lisant ce fichier.

L'idée est de mettre secret.txt dans le gitignore et le dockerignore avant de build pour kubernetes

# Fonctionnalités 

* Une fonctionnalité /users/me permet d'avoir l'utilisateur connecté

* Une fonctionnalité get_score permet d'avoir le score sur le jeu de test d'un modèle en paramètre 

* Une fonctionnalité /sentiment permet d'avoir le sentiment d'une phrase avec un modèle en paramètre

* Les modèles sont les codes branches : agnostic_model, Disneyland_HongKong, Disneyland_California, Disneyland_Paris

# Lancer les tests par docker-compose

Pour lancer les tests, il suffit de build le docker compose (en mettant les identifiants en paramètre) puis l'exécuter.

`docker-compose build --build-arg USERNAME=alice --build-arg PASSWORD=wonderland`

`docker-compose up -d`

# Si besoin de lancer les tests un par un 

L'environnement se comporte d'un container contenant l'api, et 3 contenant chacun des tests. Les tests s'authentifient grâce aux identifiants passés en paramètre. 

J'ai estimé qu'on devrait passer les identifiants en paramètre pour ne jamais les avoir en dur dans le code. Je me suis assuré que les dockerfile (et par extension, le docker-compose) nécessite de passer ces paramètres lors du build. 

De plus, on utilise --net="host" pour s'assurer que les tests ping sur le même réseau (local) du container de l'api. L'alternative aurait été d'utiliser un network 

* build

`docker image build . -t testaccount4dstest/alice_core_image:latest`

* run

`docker container run --net="host" -p 8000:8000 testaccount4dstest/alice_core_image:latest`

* build

`docker image build . -t testaccount4dstest/test_sentiment_image:latest --build-arg USERNAME=alice --build-arg PASSWORD=wonderland `

* run

`docker container run --net="host" testaccount4dstest/test_sentiment_image:latest`

* build 

`docker image build . -t testaccount4dstest/test_user_image:latest --build-arg USERNAME=alice --build-arg PASSWORD=wonderland` 

* run

`docker container run --net="host" testaccount4dstest/test_user_image:latest`

* build

`docker image build . -t testaccount4dstest/test_score_image:latest --build-arg USERNAME=alice --build-arg PASSWORD=wonderland`

* run

`docker container run --net="host" testaccount4dstest/test_score_image:latest`

# Partie Kubernetes

S'assurer d'abord d'avoir build et push l'image `alice_core_image` avant de monter le cluster

# secret

Le "secret" utilisé pour encoder les identifiants est un fichier en local si on lance les tests en local, mais est enregistré sous forme d'un secret kubernetes si on lance sur kubernetes.

Le code s'adapte et prend l'un ou l'autre des secrets selon l'endroit de l'exécution. L'idéal serait qu'en prod, le secret soit en kubernetes et jamais sur github, mais pour pouvoir tester l'exercice en local, j'ai gardé le fichier secret.txt dans le dossier credentials 

`kubectl create -f alice-secret.yml`

# deploy

`kubectl create -f alice-deploy.yml`

# service

`kubectl create -f alice-service.yml`

# ingress

`kubectl create -f alice-ingress.yml`

Si vous êtes sur windows et que vous utilisez WSL 2 : L'Ingress risque de ne pas marcher. Pour vous assurer du bon fonctionnement du service, exécutez `minikube service web --url` pour exposer le service directement 