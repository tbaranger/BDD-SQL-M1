import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

# Récupération de la liste des régions
cur.execute("EXPLAIN SELECT * from region;")
rows = cur.fetchall()

## Requêtes à analyser
# Chef-lieu
cur.execute("EXPLAIN SELECT nomcom FROM cheflieudep, commune WHERE cheflieudep.codecom = commune.codecom AND cheflieudep.codedep = '33';")
rows = cur.fetchall()
print("- Chef-lieu : {}".format(rows[0]['nomcom']))

# Superficie (somme des superficie des communes)
# Ici, on part du principe que la superficie n'est disponible que pour une année
cur.execute("EXPLAIN SELECT SUM(valeur) as superficie FROM commune, statscom, labelstats WHERE commune.codedep = '33' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND labelstats.codestat = 'Superf';")
rows = cur.fetchall()
print("- Superficie : {}km²".format(rows[0]['superficie']))

# Population totale en 2017
# Ici, on part du principe que l'on connait l'année du dernier recensement
cur.execute("EXPLAIN SELECT SUM(valeur) as population FROM commune, statscom, labelstats WHERE commune.codedep = '33' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND labelstats.codestat = 'Pop' AND annee = 2017;")
rows = cur.fetchall()
print("- Population totale en 2017 : {} habitants".format(rows[0]['population']))

# Commune la plus peuplée en 2017
command = (	"EXPLAIN SELECT nomcom, valeur AS population "
			"FROM commune, statscom, labelstats "
			"WHERE commune.codedep = '33' "
			"AND statscom.codecom = commune.codecom "
			"AND statscom.idstat = labelstats.idstat "
			"AND labelstats.codestat = 'Pop' "
			"AND annee = 2017 "
			"AND valeur >= "
				"(SELECT MAX(valeur) FROM commune, statscom, labelstats WHERE commune.codedep = '33' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND codestat = 'Pop' AND annee = 2017);")
cur.execute(command)
rows = cur.fetchall()
for d in rows:
	print("- Commune la plus peuplée en 2017 : {} ({} habitants)".format(d['nomcom'], d['population']))

# Commune la moins peuplée en 2017
command = (	"EXPLAIN SELECT nomcom, valeur AS population "
			"FROM commune, statscom, labelstats "
			"WHERE commune.codedep = '33' "
			"AND statscom.codecom = commune.codecom "
			"AND statscom.idstat = labelstats.idstat "
			"AND labelstats.codestat = 'Pop' "
			"AND annee = 2017 "
			"AND valeur <= "
				"(SELECT MIN(valeur) FROM commune, statscom, labelstats WHERE commune.codedep = '33' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND codestat = 'Pop' AND annee = 2017);")
cur.execute(command)
rows = cur.fetchall()
for d in rows:
	print("- Commune la moins peuplée en 2017 : {} ({} habitants)\n".format(d['nomcom'], d['population']))

# Liste des indicateurs départementaux
print("Liste des indicateurs départementaux pour le département Gironde :\n")

# Requête
cur.execute("EXPLAIN SELECT departement.codedep, nomdep, labelstats.idstat, valeur, annee, description FROM statsdep, labelstats, departement WHERE statsdep.codedep = departement.codedep AND nomdep = 'Gironde' AND labelstats.idstat = statsdep.idstat ORDER BY annee ASC, idstat ASC;")
rows = cur.fetchall()

for d in rows:
	print(d['description'] + " en " + str(d['annee']) + " : " + str(d['valeur']))

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
