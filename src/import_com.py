import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/commune.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='commune', sep=',', columns=('codecom', 'codedep', 'nomcom'))

conn.commit()

# Affichage des données importées
cur.execute("select * from commune;")
rows = cur.fetchall()

page = ''
for d in rows:
	page += d['codecom'] + " (département " + d['codedep'] + ") : " + d['nomcom'] + "\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
