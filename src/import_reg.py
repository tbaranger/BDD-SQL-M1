import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/region.csv', newline='', encoding="utf8") as f:
	cur.copy_from(file=f, table='region', sep=',', columns=('codereg', 'nomreg'))

conn.commit()

# Affichage des données importées
cur.execute("select * from region;")
rows = cur.fetchall()

page = ''
for d in rows:
	page += d['codereg'] + ": " + d['nomreg'] + "\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
