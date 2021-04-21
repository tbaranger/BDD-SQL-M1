import psycopg2
import psycopg2.extras
import sys

def connect():
        # Tentative de connexion à la base de données
        print('Connexion à la base de données...')
        USER="user"
        PASSWORD="password"
        try:
                conn = psycopg2.connect("host=pgsql dbname=" + USER + " user=" + USER + " password=" + PASSWORD)
        except Exception as e:
                exit("Connexion impossible à la base de données: " + str(e))

        print('Connecté à la base de données.')

        # Préparation de l'exécution des requêtes (à ne faire qu'une fois)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return(cur,conn)
