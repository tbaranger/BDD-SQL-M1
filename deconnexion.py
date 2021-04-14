import psycopg2
import psycopg2.extras
import sys

def disconnect(cur,conn):
    # Fermeture de la connexion
    cur.close()
    conn.close()

