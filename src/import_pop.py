import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('../data/pop.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statscom', sep=',', columns=('codecom', 'idstat', 'valeur', 'annee'))

conn.commit()

# Affichage des données importées
cur.execute("SELECT commune.codecom, nomcom, valeur, annee FROM statscom, labelstats, commune, departement WHERE nomdep = 'Gironde' AND departement.codedep = commune.codedep AND statscom.codecom = commune.codecom AND codestat = 'Pop' AND labelstats.idstat = statscom.idstat AND annee = 2017 ORDER BY commune.codecom;")
rows = cur.fetchall()

page = 'Population en 2017 pour les communes de Gironde.\n'
for d in rows:
	page += d['nomcom'] + " : " + str(d['valeur']) + " habitants en " + str(d['annee']) + ".\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
