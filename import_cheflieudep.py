import csv
import psycopg2
import psycopg2.extras
import sys

# Tentative de connexion à la base de données
print('Connexion à la base de données...')
USERNAME="erleroux"
PASS="9AjHbL8w3"
try:
	conn = psycopg2.connect("host=pgsql dbname=" + USERNAME + " user=" + USERNAME + " password=" + PASS)
except Exception as e:
	exit("Connexion impossible à la base de données: " + str(e))

print('Connecté à la base de données')

# Préparation de l'exécution des requêtes (à ne faire qu'une fois)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

with open('chef_lieu_dep.csv', newline='', encoding='latin-1') as f:
	cur.copy_from(file=f, table='cheflieudep', sep=',', columns=('codedep', 'codecom'))

conn.commit()

# Affichage des données importées
cur.execute("select nomdep, departement.codedep, nomcom from cheflieudep, departement, commune where departement.codedep = cheflieudep.codedep and cheflieudep.codecom = commune.codecom ORDER BY codedep;")
rows = cur.fetchall()

page = 'Liste des chefs lieux par département.\n'
for d in rows:
	page += d["nomdep"] + " (" + d["codedep"] + ") : " + d["nomcom"] + "\n"

# Fermeture de la connexion
cur.close()
conn.close()
print(page)
