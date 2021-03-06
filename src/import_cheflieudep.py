import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/chef_lieu_dep.csv', newline='', encoding='latin-1') as f:
	cur.copy_from(file=f, table='cheflieudep', sep=',', columns=('codedep', 'codecom'))

conn.commit()

# Affichage des données importées
cur.execute("select nomdep, departement.codedep, nomcom from cheflieudep, departement, commune where departement.codedep = cheflieudep.codedep and cheflieudep.codecom = commune.codecom ORDER BY codedep;")
rows = cur.fetchall()

page = 'Liste des chefs lieux par département.\n'
for d in rows:
	page += d["nomdep"] + " (" + d["codedep"] + ") : " + d["nomcom"] + "\n"


print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
