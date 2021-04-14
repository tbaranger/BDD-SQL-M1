import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/statsreg.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statsreg', sep=',', columns=('codereg', 'idstat', 'valeur', 'annee'))

conn.commit()

# Affichage des données importées
cur.execute("SELECT region.codereg, nomreg, labelstats.idstat, valeur, annee, description FROM statsreg, labelstats, region WHERE statsreg.codereg = region.codereg AND labelstats.idstat = statsreg.idstat ORDER BY idstat ASC, codereg ASC;")
rows = cur.fetchall()

page = 'Statistiques concernant les régions.\n'
for d in rows:
	page += d['description'] + " - " + d['nomreg'] + " : " + str(d['valeur']) + " en " + str(d['annee']) + ".\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
