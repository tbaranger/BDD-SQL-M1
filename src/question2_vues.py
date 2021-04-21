import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

## Departements

cur.execute("DROP VIEW IF EXISTS stats_calculees_reg;") 
cur.execute("DROP VIEW IF EXISTS stats_calculees_dep;") 
conn.commit()

# Statistiques obtenues par sommation
command = '''SELECT departement.codedep, nomdep, description as statistique, SUM(valeur) as valeur, annee
FROM commune, departement, labelstats, statscom
WHERE commune.codedep = departement.codedep
AND commune.codecom = statscom.codecom
AND labelstats.idstat = statscom.idstat
AND labelstats.codestat IN ('Pop', 'Superf')
GROUP BY (departement.codedep, description, annee)
ORDER BY codedep ASC, annee DESC;'''

cur.execute("CREATE VIEW stats_calculees_dep AS " + command)

# Validation
conn.commit()

## Regions

# Statistiques obtenues par sommation
command = '''SELECT region.codereg, nomreg, statistique, SUM(valeur) as valeur, annee
FROM region, departement, stats_calculees_dep
WHERE departement.codereg = region.codereg
AND departement.codedep = stats_calculees_dep.codedep
GROUP BY (region.codereg, statistique, annee)
ORDER BY codereg ASC, annee DESC;'''

cur.execute("CREATE VIEW stats_calculees_reg AS " + command)

# Validation
conn.commit()

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
