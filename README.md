# Projet de Bases de Données Avancées - Master 1
Code source pour la création et l'administration d'une base de données SQL sous PostgreSQL en Python avec Psycopg2 dans le cadre d'un projet du cours de Bases de Données Avancées en Master 1 à l'Université de Bordeaux, cours assuré par Bruno Pinaud en 2020/2021. 

## Introduction
L'objectif de ce projet était d'apprendre à manipuler une base de données dans un langage de plus haut niveau, ici Python, et d'illustrer certaines des propriétés liées aux requêtes telle que l'optimisation du temps de calcul grâce à l'utilisation d'index. La modélisation de la base de données ainsi que la création des fichiers d'import de données ont aussi représenté une part importante du travail total. 

### Données
Les données qu'il nous était proposé d'utiliser pour ce projet sont les données de l'INSEE concernant les communes, départements, et régions françaises. En particulier, nous avons utilisé les fichiers "séries historiques" concernant les communes, contenant de nombreuses statistiques dont la population des communes de France pour les années 1968, 1975, 1982, 1990, 1999, 2007, 2012 et 2017 (<a href="https://www.insee.fr/fr/statistiques/4515941">Séries historiques en 2017 | Insee</a>). L'intérêt de ces données est que le découpage géographique utilisé est le plus récent, et on évite ainsi toutes les questions liées au fusionnement des communes.

Concernant les données liées aux départements et aux régions, il s'agit des statistiques intitulées <a href="https://www.insee.fr/fr/statistiques/2512993">Développement durable&nbsp;: 20 indicateurs régionaux et départementaux</a> (source : Insee), qui regroupent des indicateurs économiques (e.g. taux de chômage), sociaux, environnementaux, et autres.

### Modèle relationnel
Voici une illustration avec Libreoffice Base du modèle relationnel que nous avons finalement utilisé pour représenter ces données.
<img src="images/schema.png" alt="modèle relationnel"/>

## Contenu
Les fichiers "tables.sql" et "stats.sql" permettent de créer les tables et d'insérer les méta-données concernant les statistiques. Ensuite, l'import des données provenant des fichiers CSV se fait directement à partir des scripts Python se trouvant dans le fichier 'src'.
