import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

with open('chef_lieu_reg.csv', newline='', encoding='latin-1') as f:
	cur.copy_from(file=f, table='cheflieureg', sep=',', columns=('codereg', 'codecom'))

conn.commit()

# Affichage des données importées
cur.execute("select nomreg, region.codereg, nomcom from cheflieureg, region, commune where region.codereg = cheflieureg.codereg and cheflieureg.codecom = commune.codecom ORDER BY codedep;")
rows = cur.fetchall()

page = 'Liste des chefs lieux par département.\n'
for d in rows:
	page += d["nomreg"] + " (" + d["codereg"] + ") : " + d["nomcom"] + "\n"

print(page)
# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
