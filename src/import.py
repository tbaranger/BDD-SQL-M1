import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

## Import des régions
with open('../data/region.csv', newline='', encoding="utf8") as f:
	cur.copy_from(file=f, table='region', sep=',', columns=('codereg', 'nomreg'))

## Import des départements
with open('../data/departement.csv', newline='') as f:
	cur.copy_from(file=f, table='departement', sep=',', columns=('codedep', 'codereg', 'nomdep'))

## Import des communes
with open('../data/commune.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='commune', sep=',', columns=('codecom', 'codedep', 'nomcom'))

## Import des chefs-lieux régionaux
with open('../data/chef_lieu_reg.csv', newline='', encoding='latin-1') as f:
	cur.copy_from(file=f, table='cheflieureg', sep=',', columns=('codereg', 'codecom'))

## Import des chefs-lieux départementaux
with open('../data/chef_lieu_dep.csv', newline='', encoding='latin-1') as f:
	cur.copy_from(file=f, table='cheflieudep', sep=',', columns=('codedep', 'codecom'))

## Import des statistiques régionales
with open('../data/statsreg.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statsreg', sep=',', columns=('codereg', 'idstat', 'valeur', 'annee'))

## Import des statistiques départementales
with open('../data/statsdep.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statsdep', sep=',', columns=('codedep', 'idstat', 'valeur', 'annee'))

## Import des populations des communes
with open('../data/pop.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statscom', sep=',', columns=('codecom', 'idstat', 'valeur', 'annee'))

## Import des superficies des communes
with open('../data/superf.csv', newline='', encoding='utf8') as f:
	cur.copy_from(file=f, table='statscom', sep=',', columns=('codecom', 'idstat', 'valeur', 'annee'))

# Validation
conn.commit()

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
