import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/statsdep.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statsdep', sep=',', columns=('codedep', 'idstat', 'valeur', 'annee'))

conn.commit()

# Affichage des données importées
cur.execute("SELECT departement.codedep, nomdep, labelstats.idstat, valeur, annee, description FROM statsdep, labelstats, departement WHERE statsdep.codedep = departement.codedep AND nomdep = 'Gironde' AND labelstats.idstat = statsdep.idstat ORDER BY annee ASC, idstat ASC;")
rows = cur.fetchall()

page = 'Statistiques concernant la Gironde.\n'
for d in rows:
	page += d['description'] + " en " + str(d['annee']) + " : " + str(d['valeur']) + "\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
