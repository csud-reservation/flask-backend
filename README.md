# Système de réservation CSUD

## Déploiement sur un serveur virtuel

Le système de réservation est complètement conteneurisé avec Docker. Pour pouvoir l'installer sur un serveur virtuel distant (VPS), il faut commencer par configurer le serveur distant pour pouvoir lancer des conteneurs Docker.

### Configuration initiale du serveur Ubuntu 16.04 LTS

1. Démarrer le serveur Ubuntu 16.04 LTS
2. Régler le nom de l'hôte distant dans la variable d'environnement `HOST`

   ```
   export HOST=csud-reservation.com
   ```

3. Si nécessaire, configurer la possibilité de se connecter par SSH en root avec
   mot de passe

3. Exécuter les commandes suivantes :

   ```{bash}
   cd vserver
   make ssh-register-public-key
   make init
   make setup-docker
   ```

### Pousser le code sur le serveur

La commande suivante doit être exécutée à chaque fois qu'il y a des modifiations
dans le code l'application serveur.

```bash
make push
```

S'il a des modifications dans les variables d'environnement, notamment pour la
configuration Let's encrypt, il faut exécuter les règles


```bash
make host.env.build
make backup.env.build
```


### Démarrage du projet

Pour démarrer le projet, il faut commencer par créer un environnement virtuel Python. Sous Cloud9, il faut faire

```{bash}
sudo pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pousser les données sur le serveur

Pour terminer, si des données sqlite sont disponibles, il est possible de les
pousser sur le serveur avec sqlite-data-push

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

La requête SQL pour déterminer les conflits se trouve dans le fichier
`sql/find_conflicts.sql`. 

```sql
-- un peu plus élaboré ... avec quelques dates à changer en dur ... Ce serait
-- super d'avoir une route qui sort tous ces conflits
SELECT r1.id, r1.start_date, r1.end_date, r1.reason_short, r1.reason_details, u1.sigle as "owner1", r2.id, r2.start_date, r2.end_date, r2.reason_short, r2.reason_details, u2.sigle as "owner2", rooms.name as "salle", timeslots.start_time, timeslots.end_time, weekdays.name
FROM (SELECT * FROM reservations WHERE end_date > '2019-09-16') as r1
INNER JOIN reservations_timeslots as rts1 ON r1.id = rts1.reservation_id
INNER JOIN (SELECT * FROM reservations WHERE end_date > '2019-09-16') as r2 ON r1.room_id = r2.room_id and r1.weekday_id = r2.weekday_id and r1.id <> r2.id
INNER JOIN reservations_timeslots as rts2 ON r2.id = rts2.reservation_id and rts1.timeslot_id = rts2.timeslot_id
INNER JOIN rooms ON rooms.id = r1.room_id
INNER JOIN weekdays ON weekdays.id = r1.weekday_id
INNER JOIN timeslots ON rts1.timeslot_id = timeslots.id
INNER JOIN users as u1 ON u1.id = r1.owner_id
INNER JOIN users as u2 ON u2.id = r2.owner_id
WHERE 
	-- filtrer les les réservations qui n'ont pas de conflit de date
	NOT (r1.end_date < r2.start_date OR r2.end_date < r1.start_date)
	-- il ne sert à rien de considérer les conflits intentionnels comme des
	-- conflits (par exemple TPs / branches spéciales dans la même salle, ceci
	-- est voulu par escada
	AND NOT (r1.end_date = '2020-07-05' and r2.end_date = '2020-07-05')
	-- pour casser la symétrie ... sinon chaque conflit apparaît deux fois de
	-- suite
	AND r1.id < r2.id

```

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


Pour charger les nouvelles données, exécuter la commande (voir également ci-dessus)

```bash
python manage.py load 
```

### Chargement des nouveaux professeurs au début de l'année

