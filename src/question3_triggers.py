import csv
import psycopg2
import psycopg2.extras
import sys
import connexion
import deconnexion

#Tentative de connexion
cur,conn = connexion.connect()

## Création de triggers pour empêcher la mise à jour des tables
## 'region', 'departement'

## Il est nécessaire de créer une fonction do_nothing() au préalable,
## car PostgreSQL requiert l'appel à une procédure dans les triggers.

query = "CREATE OR REPLACE function do_nothing() returns trigger language plpgsql AS $$ BEGIN return NULL; END $$;"
cur.execute(query)

## Création des triggers qui empêchent l'insertion, mise à jour, suppression
cur.execute("CREATE TRIGGER prevent_insert_region BEFORE INSERT ON region FOR EACH ROW EXECUTE PROCEDURE do_nothing();")
cur.execute("CREATE TRIGGER prevent_update_region BEFORE UPDATE ON region FOR EACH ROW EXECUTE PROCEDURE do_nothing();")
cur.execute("CREATE TRIGGER prevent_delete_region BEFORE DELETE ON region FOR EACH ROW EXECUTE PROCEDURE do_nothing();")

## Test du trigger, on tente d'insérer une région
cur.execute("INSERT INTO region(codereg, nomreg) VALUES ('00', 'Ancienne-Aquitaine');")
cur.execute("UPDATE region SET nomreg = 'Terre du Milieu' WHERE codereg = '75';")
cur.execute("DELETE FROM region WHERE codereg = '11';")

query = "SELECT * FROM region;"
print("\n" + query)
cur.execute(query)
rows = cur.fetchall()
for d in rows:
	print(d['codereg'] + ": " + d['nomreg'])

## On répète l'opération pour les départements

## Création des triggers qui empêchent l'insertion, mise à jour, suppression
cur.execute("CREATE TRIGGER prevent_insert_departement BEFORE INSERT ON departement FOR EACH ROW EXECUTE PROCEDURE do_nothing();")
cur.execute("CREATE TRIGGER prevent_update_departement BEFORE UPDATE ON departement FOR EACH ROW EXECUTE PROCEDURE do_nothing();")
cur.execute("CREATE TRIGGER prevent_delete_departement BEFORE DELETE ON departement FOR EACH ROW EXECUTE PROCEDURE do_nothing();")

## Test du trigger, on tente d'insérer une région
cur.execute("INSERT INTO departement(codedep, nomdep) VALUES ('00', 'Mordor');")
cur.execute("UPDATE departement SET nomdep = 'Rohan' WHERE codedep = '33';")
cur.execute("DELETE FROM departement WHERE codedep = '75';")

query = "SELECT * FROM departement WHERE codedep in ('00', '33', '75');"
print("\n" + query)
cur.execute(query)
rows = cur.fetchall()
for d in rows:
	print('Code département : ' + d['codedep'] + " (région " + d['codereg'] + ") : " + d['nomdep'])

# Fermeture de la connexion
deconnexion.disconnect(cur,conn)
