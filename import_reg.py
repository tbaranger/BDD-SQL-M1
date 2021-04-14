import csv
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

with open('region.csv', newline='', encoding="utf8") as f:
	cur.copy_from(file=f, table='region', sep=',', columns=('codereg', 'nomreg'))

conn.commit()

# Affichage des données importées
cur.execute("select * from region;")
rows = cur.fetchall()

page = ''
for d in rows:
	page += d['codereg'] + ": " + d['nomreg'] + "\n"

# Fermeture de la connexion
cur.close()
conn.close()
print(page)
