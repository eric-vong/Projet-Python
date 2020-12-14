# Projet Python pour le Data Scientist 

**Projet réalisé par Eric Vong, Thibaut Valour et Solène Blasco Lopez**

Ce projet Python utilise les données de l'OpenData de Paris sur l'encadrement des loyers de 2019, enrichies par l'intermédiaire de données web-scrapées sur internet. Il expérimente différents modèles de régression entrainés sur ces données, dans le but de révéler les déterminants des loyers de référence des appartements parisiens, et d'être capable de les prédire. 

L'objet de ce projet est donc de répondre à la problématique suivante : 
**Quels sont les déterminants du loyer d'un bien immobilier parisien ?**

Une première partie de ce projet est consacrée à la récupération des données, et à la création de nouvelles variables explicatives, à partir de la base initiale ou de webscraping. Dans un second temps, nous avons mené une analyse descriptive pour représenter les données et se faire une première idée de la manière dont les variables à notre disposition impactent les loyers parisiens. Enfin, nous avons implémenter des modèles de régressions pour tenter de prédire les loyers parisiens à partir des variables explicatives les plus pertinentes.


**Structure du code :** 

1) `data` : dossier contenant les codes ayant permis de récolter (`recuperation.py`) et enrichir (`ajout_score_metro.py`) les données.  

2) `preprocessing` : dossier contenant les codes ayant permis de créer une base de données `donnees_num.geojson` aux variables uniquement numériques (`variables_num.py`) ; et des fonctions utiles au preprocessing de certains modèles (`standardisation.py` pour la standardisation, `mise_echelle.py` utilisant `MinmaxScaler`)

3) `visualization` : dossier contenant les codes ayant permis une première analyse descriptive des données, et leur visualisation (`acp.py` pour la réalisation d'une acp, et `stat_desc.py` pour le reste des statistiques descriptives et de la visualisation). 

4) `modelisation` : dossier contenant les codes des différents modèles utilisés pour répondre à la problématique (`lasso.py` pour la sélection des variables d'intérêt, `regression_lineaire.py` pour la régression linéaire, `knn.py` pour le modèle k Nearest Neighbors, ...)
