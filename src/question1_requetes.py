import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

## Choix de la région

# Récupération de la liste des régions
cur.execute("select * from region;")
rows = cur.fetchall()

liste_codereg = []
page = 'Liste des régions de France :\n'
for d in rows:
	page += 'Code ' + d['codereg'] + " : " + d['nomreg'] + "\n"
	liste_codereg.append(d['codereg'])
print(page)

codereg = input("Entrez le code de la région souhaitée : ")
max_attempts = 3
nb_attempts = 0
while ((codereg not in liste_codereg) and nb_attempts < max_attempts) :
	nb_attempts += 1
	codereg = input("Code invalide. Entrez le code de la région souhaitée : ")
if ((codereg not in liste_codereg) and nb_attempts == max_attempts):
	print("Nombre maximal de tentatives atteint. Déconnexion.\n")
	deconnexion.disconnect(cur,conn)
	exit()

# Récupération de la ligne correspondant au choix de l'utilisateur
for r in rows:
	if r['codereg'] == codereg:
		res = r

print("Vous avez choisi la région {} : {}\n".format(res['codereg'], res['nomreg']))

## Choix du département
# Récupération de la liste des régions
cur.execute("SELECT * FROM departement WHERE codereg = '" + res['codereg'] + "';")
rows = cur.fetchall()

liste_codedep = []
page = 'Liste des départements de ' + res['nomreg'] + ' :\n'
for d in rows:
	page += 'Code ' + d['codedep'] + " : " + d['nomdep'] + "\n"
	liste_codedep.append(d['codedep'])
print(page)

codedep = input("Entrez le code du département souhaité : ")
max_attempts = 3
nb_attempts = 0
while ((codedep not in liste_codedep) and nb_attempts < max_attempts) :
	nb_attempts += 1
	codedep = input("Code invalide. Entrez le code du département souhaité : ")
if ((codedep not in liste_codedep) and nb_attempts == max_attempts):
	print("Nombre maximal de tentatives atteint. Déconnexion.\n")
	deconnexion.disconnect(cur,conn)
	exit()

# Récupération de la ligne correspondant au choix de l'utilisateur
for r in rows:
	if r['codedep'] == codedep:
		res = r

print("Vous avez choisi le département {} : {}\n".format(res['codedep'], res['nomdep']))

## Calcul et affichage de quelques statistiques sur le département choisi
print("Voici quelques statistiques concernant le département " + res['nomdep'] + " :\n")

# Chef-lieu
cur.execute("SELECT nomcom FROM cheflieudep, commune WHERE cheflieudep.codecom = commune.codecom AND cheflieudep.codedep = '" + res['codedep'] + "';")
rows = cur.fetchall()
print("- Chef-lieu : {}".format(rows[0]['nomcom']))

# Superficie (somme des superficie des communes)
# Ici, on part du principe que la superficie n'est disponible que pour une année
cur.execute("SELECT SUM(valeur) as superficie FROM commune, statscom, labelstats WHERE commune.codedep = '" + res['codedep'] + "' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND labelstats.codestat = 'Superf';")
rows = cur.fetchall()
print("- Superficie : {}km²".format(rows[0]['superficie']))

# Population totale en 2017
# Ici, on part du principe que l'on connait l'année du dernier recensement
cur.execute("SELECT SUM(valeur) as population FROM commune, statscom, labelstats WHERE commune.codedep = '" + res['codedep'] + "' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND labelstats.codestat = 'Pop' AND annee = 2017;")
rows = cur.fetchall()
print("- Population totale en 2017 : {} habitants".format(rows[0]['population']))

# Commune la plus peuplée en 2017
command = (	"SELECT nomcom, valeur AS population "
			"FROM commune, statscom, labelstats "
			"WHERE commune.codedep = '" + res['codedep'] + "' "
			"AND statscom.codecom = commune.codecom "
			"AND statscom.idstat = labelstats.idstat "
			"AND labelstats.codestat = 'Pop' "
			"AND annee = 2017 "
			"AND valeur >= "
				"(SELECT MAX(valeur) FROM commune, statscom, labelstats WHERE commune.codedep = '" + res['codedep'] + "' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND codestat = 'Pop' AND annee = 2017);")
cur.execute(command)
rows = cur.fetchall()
for d in rows:
	print("- Commune la plus peuplée en 2017 : {} ({} habitants)".format(d['nomcom'], d['population']))

# Commune la moins peuplée en 2017
command = (	"SELECT nomcom, valeur AS population "
			"FROM commune, statscom, labelstats "
			"WHERE commune.codedep = '" + res['codedep'] + "' "
			"AND statscom.codecom = commune.codecom "
			"AND statscom.idstat = labelstats.idstat "
			"AND labelstats.codestat = 'Pop' "
			"AND annee = 2017 "
			"AND valeur <= "
				"(SELECT MIN(valeur) FROM commune, statscom, labelstats WHERE commune.codedep = '" + res['codedep'] + "' AND statscom.codecom = commune.codecom AND statscom.idstat = labelstats.idstat AND codestat = 'Pop' AND annee = 2017);")
cur.execute(command)
rows = cur.fetchall()
for d in rows:
	print("- Commune la moins peuplée en 2017 : {} ({} habitants)\n".format(d['nomcom'], d['population']))

# Liste des indicateurs départementaux
print("Liste des indicateurs départementaux pour le département : " + res['nomdep'] + "\n")

# Requête
cur.execute("SELECT departement.codedep, nomdep, labelstats.idstat, valeur, annee, description FROM statsdep, labelstats, departement WHERE statsdep.codedep = departement.codedep AND nomdep = '" + res['nomdep'] + "' AND labelstats.idstat = statsdep.idstat ORDER BY annee ASC, idstat ASC;")
rows = cur.fetchall()

for d in rows:
	print(d['description'] + " en " + str(d['annee']) + " : " + str(d['valeur']))

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
