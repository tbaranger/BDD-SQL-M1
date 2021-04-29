import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

cur.execute("DROP VIEW IF EXISTS stats_calculees_dep;")
cur.execute("DROP VIEW IF EXISTS stats_calculees_reg;")
cur.execute("DROP VIEW IF EXISTS indicateurs_reg;")
cur.execute("DROP VIEW IF EXISTS indicateurs_dep;")
cur.execute("DROP VIEW IF EXISTS view_cheflieureg;")
cur.execute("DROP VIEW IF EXISTS view_cheflieudep;")
conn.commit()

## Statistiques obtenues par somme
# Départements
command = '''SELECT departement.codedep, nomdep, description as statistique, SUM(valeur) as valeur, annee
FROM commune, departement, labelstats, statscom
WHERE commune.codedep = departement.codedep
AND commune.codecom = statscom.codecom
AND labelstats.idstat = statscom.idstat
AND labelstats.codestat IN ('Pop', 'Superf')
GROUP BY (departement.codedep, description, annee)
ORDER BY codedep ASC, annee DESC;'''
cur.execute("CREATE VIEW stats_calculees_dep AS " + command)

# Régions
command = '''SELECT region.codereg, nomreg, statistique, SUM(valeur) as valeur, annee
FROM region, departement, stats_calculees_dep
WHERE departement.codereg = region.codereg
AND departement.codedep = stats_calculees_dep.codedep
GROUP BY (region.codereg, statistique, annee)
ORDER BY codereg ASC, annee DESC;'''
cur.execute("CREATE VIEW stats_calculees_reg AS " + command)

## Indicateurs régionaux
command = "SELECT region.codereg, nomreg, description, valeur, annee FROM statsreg, labelstats, region WHERE statsreg.codereg = region.codereg AND labelstats.idstat = statsreg.idstat ORDER BY codereg ASC, labelstats.idstat ASC, annee ASC;"
cur.execute("CREATE VIEW indicateurs_reg AS " + command)

## Indicateurs départementaux
command = "SELECT departement.codedep, nomdep, description, valeur, annee FROM statsdep, labelstats, departement WHERE statsdep.codedep = departement.codedep AND labelstats.idstat = statsdep.idstat ORDER BY codedep ASC, labelstats.idstat ASC, annee ASC;"
cur.execute("CREATE VIEW indicateurs_dep AS " + command)

## Informations diverses pour les départements
# Chef-lieu région
command = "SELECT region.codereg, nomreg as région, nomcom as cheflieu, commune.codecom, nomdep as département FROM departement, region, cheflieureg, commune WHERE cheflieureg.codecom = commune.codecom AND cheflieureg.codereg = region.codereg AND commune.codedep = departement.codedep;"
cur.execute("CREATE VIEW view_cheflieureg AS " + command)

# Chef-lieu département
command = "SELECT departement.codedep, nomdep as département, nomcom as cheflieu, commune.codecom FROM departement, cheflieudep, commune WHERE cheflieudep.codecom = commune.codecom AND cheflieudep.codedep = departement.codedep;"
cur.execute("CREATE VIEW view_cheflieudep AS " + command)

# Validation
conn.commit()
print("La vue 'stats_calculees_reg' a bien été créée.")
print("La vue 'stats_calculees_dep' a bien été créée.")
print("La vue 'indicateurs_reg' a bien été créée.")
print("La vue 'indicateurs_dep' a bien été créée.")
print("La vue 'view_cheflieureg' a bien été créée.")
print("La vue 'view_cheflieudep' a bien été créée.")

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
