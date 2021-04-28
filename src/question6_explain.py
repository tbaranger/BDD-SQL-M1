import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

## Partie 1 - Analyse théorique des requêtes avec la commande EXPLAIN

print("\nQuestion 6.1 - Plans d'éxécution pour différentes requêtes.\n")
# Récupération de la liste des communes
query = "EXPLAIN SELECT * FROM commune;"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde
query = "EXPLAIN SELECT * FROM commune WHERE codedep = '33';"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde par jointure avec departement
query = "EXPLAIN SELECT codecom, nomcom, commune.codedep \n\tFROM commune, departement \n\tWHERE commune.codedep = departement.codedep \n\tAND nomdep = 'Gironde';\n"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde par tri sur codecom
query = "EXPLAIN SELECT * \n\tFROM commune \n\tWHERE codecom BETWEEN '33000' AND '33999';\n"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

## Partie 2- Comparaison des temps d'exécution

print("\nQuestion 6.2 - Comparaison des temps d'exécution.\n")
# Récupération de la liste des communes
query = "EXPLAIN ANALYZE SELECT * FROM commune;"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde
query = "EXPLAIN ANALYZE SELECT * FROM commune WHERE codedep = '33';"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde par jointure avec departement
query = "EXPLAIN ANALYZE SELECT codecom, nomcom, commune.codedep \n\tFROM commune, departement \n\tWHERE commune.codedep = departement.codedep \n\tAND nomdep = 'Gironde';\n"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Récupération de la liste des communes de Gironde par tri sur codecom
query = "EXPLAIN ANALYZE SELECT * \n\tFROM commune \n\tWHERE codecom BETWEEN '33000' AND '33999';\n"
cur.execute(query)
rows = cur.fetchall()
print(query)
for d in rows:
	print(d)
print('\n-----------------------------')

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
