"""
Récupération des données de la mairie de Paris sur l'encadrement des loyers 2019

Ajout de deux nouvelles variables : 
    - distance_centre_paris : distance du centre de chaque quartier au centre de Paris
    - superficie_quartier : superficie de chaque quartier
"""

import pandas as pd
import geopandas as gpd


"""
1. Récupération des données de la mairie de Paris 
"""

donnees_brutes = gpd.read_file('https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/download/?format=geojson&timezone=Europe/Berlin&lang=fr')
#donnees_brutes.columns

# Sélection des variables d'intérêt :
donnees = donnees_brutes[['nom_quartier','id_quartier','ref','min','max','epoque','meuble_txt','piece','geometry']]



"""
2. Ajout de distance_centre_paris 
"""

#Centres des quartiers :
df = donnees.centroid 
df = df.to_crs(epsg=2154)

#Centre de Paris (coordonnées trouvées sur internet): 
longitude = [2.3488 for i in range(2560)]
latitude = [48.8534 for i in range(2560)]
df2 = gpd.GeoDataFrame(geometry = gpd.points_from_xy(longitude, latitude),crs={'init': 'epsg:4326'})
df2 = df2.to_crs(epsg=2154)

#Ajout de distance_centre_paris :
distances = pd.DataFrame(df.distance(df2)*10**(-3),columns=["distance_centre_paris"])  #la multiplication par 10^3 convertit les mètres en kms
donnees = donnees.join(distances)



"""
3. Ajout de superficie_quartier 
"""

df3 = donnees.geometry
df3 = df3.to_crs(epsg=2154)

donnees['superficie_quartier'] = df3.area.div(10**6)  #La division convertit les m² en km²
