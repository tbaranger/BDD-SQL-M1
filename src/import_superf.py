import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/superf.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statscom', sep=',', columns=('codecom', 'idstat', 'valeur', 'annee'))

conn.commit()

# Affichage des données importées
cur.execute("SELECT commune.codecom, nomcom, valeur, annee FROM statscom, labelstats, commune, departement WHERE nomdep = 'Gironde' AND departement.codedep = commune.codedep AND statscom.codecom = commune.codecom AND codestat = 'Superf' AND labelstats.idstat = statscom.idstat ORDER BY commune.codecom;")
rows = cur.fetchall()

page = 'Superficie des communes de Gironde en 2020.\n'
for d in rows:
	page += d['nomcom'] + " : " + str(d['valeur']) + "km².\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
