# Système de réservation CSUD

## Déploiement sur un serveur virtuel

Le système de réservation est complètement conteneurisé avec Docker. Pour pouvoir l'installer sur un serveur virtuel distant (VPS), il faut commencer par configurer le serveur distant pour pouvoir lancer des conteneurs Docker.

### Configuration initiale du serveur Ubuntu 16.04 LTS

1. Démarrer le serveur Ubuntu 16.04 LTS
2. Régler le nom de l'hôte distant dans la variable d'environnement `HOST`

   ```
   export HOST=csud-reservation
   ```

3. Exécuter les commandes suivantes :

   ```{bash}
   cd vserver
   make init
   make setup-docker
   ```

### Démarrage du projet

Pour démarrer le projet, il faut commencer par créer un environnement virtuel Python. Sous Cloud9, il faut faire

```{bash}
sudo pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### ERAlchemy

Pour pouvoir générer les diagrammes entité-associations du modèle SQLAlchemy, il est nécessaire d'installer GraphViz de la manière suivante :

```{bash}
$ sudo apt-get install graphviz
$ sudo apt-get install libgraphviz-dev
$ pip install eralchemy
```

Pour installer le projet dans Cloud9, saisir les commandes suivantes dans le terminal pour pouvoir développer dans la branche `dev` :

```{bash}
$ rm -rf *
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ git init
$ git remote add origin https://github.com/csud-reservation/flask-backend.git
$ git fetch
$ git checkout -t origin/dev
```

### Référence de commandes utiles

#### Commande pour ajouter un utilisateur (secrétaire) manuellement

Commencer par ouvrir un terminal

```{bash}
$ docker exec -it <container> bash
$ python manage.py shell
```

Dans le shell Python, faire

```
secr = User(first_name='Prénom', last_name='Nom', email='email@edufr.ch', sigle='XXXX')
secr.set_password('...')
db.session.add(secr)
db.session.commit()
```

#### Commandes pour insérer les données de EDT

Dans un shell bash, utiliser la commande `load` en spécifiant les dates de début
et de fin des réservations à insérer :

```{bash}
python manage.py load --data_file data/edt_1819_ok.txt  2018-09-17 2019-07-05
```

#### Commande pour obtenir la liste des conflits

Cette commande est encore à déterminer mais la requête SQL va être du style

### Procédure pour introduire les nouveaux horaires de fin d'année

1.  Tirer la base de données sqlite en local
1.  Utiliser SQLite DB Browser pour travailler avec la base de données en local et **ne pas oublier d'enregistrer les modifications dans SQLite DB Browser** ... je me fais avoir à chaque fois.
    - Utiliser `sql/update-*.sql` pour modifier les dates de fin.
    - En particulier la requête qui fait le BACKUP des réservations qui se
      terminent après le **splitpoint** ==> je n'ai pas cette requête
1.  Déterminer la date à partir de laquelle l'horaire change
1.  modifier les réservations actuelles qui commencent au début de l'année et se terminent à la fin d l'année pour qu'elles se terminent le vendredi de la dernière semaine de l'horaire actuel
1.  Lister les réservations qui se terminent après la date charnière ... manifestement tout ne part pas avec la première manipulation.
1.  Travailler sur la machine locale avec des données à jour dans un premier temps
    1.  Importer les heures du fichier CSV en spécifiant les dates de début et de fin de la période
    1.  Tester en local que tout fonctionne
1.  Pousser les modifications sur le serveur


Pour charger les nouvelles données, exécuter la commande 

```bash
python manage.py load 
```
