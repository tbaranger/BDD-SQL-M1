import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/departement.csv', newline='') as f:
	cur.copy_from(file=f, table='departement', sep=',', columns=('codedep', 'codereg', 'nomdep'))

conn.commit()

# Affichage des données importées
cur.execute("select * from departement;")
rows = cur.fetchall()

page = ''
for d in rows:
	page += 'Code département : ' + d['codedep'] + " (région " + d['codereg'] + ") : " + d['nomdep'] + "\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
