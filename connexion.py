import psycopg2
import psycopg2.extras
import sys

# Tentative de connexion à la base de données
print('Connexion à la base de données...')
USERNAME="thbaranger"
PASS="scWjdDU9FePP9rN"
try:
	conn = psycopg2.connect("host=pgsql dbname=" + USERNAME + " user=" + USERNAME + " password=" + PASS)
except Exception as e:
	exit("Connexion impossible à la base de données: " + str(e))

print('Connecté à la base de données')

# Préparation de l'exécution des requêtes (à ne faire qu'une fois)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

command = 'SELECT * from labelstats'
print('Exécution de la requête: ', command)
try:
	# Lancement de la requête
	cur.execute(command)
except Exception as e:
	# Fermeture de la connexion
	cur.close()
	conn.close()
	exit("Erreur lors de l'exécution de : " + command + " : " + str(e))

print("Récupération de la requête\n")

print("Nombre de lignes dans le résultat: ", cur.rowcount)

rows = cur.fetchall()
# rows => liste de dictionnaires (chaque ligne du résultat de la requête est un dictionnaire dont la clé est le nom de l'attribut

# Traitement des résultats
page = ''
for d in rows:
	page += d['codestat'] + ":  " + d['description'] +"\n"

# Fermeture de la connexion
cur.close()
conn.close()
print(page)
