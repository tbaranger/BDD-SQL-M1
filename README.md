# BDD-SQL-M1
Code source pour la création et l'administration d'une base de données SQL sous PostgreSQL en Python avec Psycopg2 dans le cadre d'un projet de Master 1. L'objectif était d'apprendre à manipuler une base de données dans un langage de plus haut niveau, ici Python, et d'illustrer certaines des propriétés liées aux requêtes telle que l'optimisation du temps de calcul grâce à l'utilisation d'index, etc. La modélisation de la base de données ainsi que la création des fichiers d'import de données ont aussi représenté une part importante du travail total. 

![image](images/schema.png)


Les fichiers "tables.sql" et "stats.sql" permettent de créer les tables et d'insérer les méta-données concernant les statistiques. Ensuite, l'import des données provenant des fichiers CSV se fait directement à partir des scripts Python se trouvant dans le fichier 'src'.
