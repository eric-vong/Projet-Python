"""
Enrichissement de la base de données récupérée dans recuperation.py 

Ajout d'une variable score_metro calculée de la manière suivante :
    - on liste les lignes distinctes de métro et de rer qui passent dans chaque quartier
    - on attribue un score à chaque ligne, qui correspond à sa fréquentation annuelle 
    - le somme pour chaque quartier les scores de ses lignes de métro/rer
    - Le score d'un quartier correspond alors à cette somme, divisée par la plus grande valeur attribuée à un quartier
De cette manière, on obtient un score compris entre 0 et 1 pour chaque quartier.    
"""

import re 
import urllib
import pandas as pd
import geopandas as gpd
import bs4 

# Fonction pour transformer les coordonnées récoltées (sous format DMS nord-est) en format DD :
dd = lambda d,m,s : float(d) + float(m)/60 + float(s)/(60*60)
def dms_to_dd (dms):
    parts = re.split('[^\d\w]+', dms)
    lat = dd(parts[0], parts[1], parts[2])
    lng = dd(parts[4], parts[5], parts[6])
    return (lat, lng)


"""
1. Web-scraping de la liste des stations de métro et de rer et de lerus coordonnées
"""

nom = []
ligne = [] 
latitude = []
longitude = []

urls = ['https://fr.wikipedia.org/wiki/Liste_des_stations_du_m%C3%A9tro_de_Paris','https://fr.wikipedia.org/wiki/Liste_des_gares_du_RER_d%27%C3%8Ele-de-France']

for url in urls : 

    sock = urllib.request.urlopen(url).read() 
    page=bs4.BeautifulSoup(sock,features="lxml")

    liste_stations = page.find('table').findAll('tr')
    
    for station in liste_stations[1:] :
    
        #Nom de la station :    
        nom_station = station.find('a').text
    
        #Coordonnées géographiques de la station :
        url_station = "http://fr.wikipedia.org"+station.find('a').get('href')
    
        search = urllib.request.urlopen(url_station).read()
        search_station=bs4.BeautifulSoup(search,features="lxml")
    
        coord = search_station.find('a',{'class': "mw-kartographer-maplink"}).text
        lat,lng = dms_to_dd(coord)
    
        #Lignes desservies par la station :    
        lignes = station.find('span',{'style' : "white-space:nowrap"}).findAll('span')
    
        for l in lignes : 
            nom.append(nom_station)
            ligne.append(l.get('data-sort-value'))
            latitude.append(lat)
            longitude.append(lng)
            
stations = gpd.GeoDataFrame(pd.DataFrame({'nom' : nom, 'ligne' : ligne}),geometry=gpd.points_from_xy(longitude, latitude))



"""
2. Listing des lignes qui passent dans chaque quartier
"""

# Récupération de la base de données de l'OpenData de Paris contenant les quartiers administratifs
quartiers_bruts = gpd.read_file('https://parisdata.opendatasoft.com/explore/dataset/quartier_paris/download/?format=geojson&timezone=Europe/Berlin&lang=fr')
quartiers = quartiers_bruts[['l_qu','c_qu','geometry']]

# Attribution d'un quartier à chaque station de métro/rer : 
stations_quartiers = gpd.sjoin(stations, quartiers, op='intersects')

# Suppression des doublons pour avoir les lignes de chaques quartiers :
lignes_quartiers = stations_quartiers[['c_qu','ligne']].drop_duplicates()



"""
3. Création du score de chaque ligne de métro/rer par web-scraping 
"""

#Pour le rer, il faut aller sur chaque page Wikipédia de la ligne. Pour aller plus vite, on le fait manuellement (il n'y a que 5 lignes) :
lignes = ['A !','B !','C !','D !','E !']
frequentation = [309.36,165.5,140,145,60] 


#Pour le métro, il existe directement un classement sur Wikipédia :
sock = urllib.request.urlopen("https://fr.wikipedia.org/wiki/Liste_des_lignes_de_m%C3%A9tro_parisiennes_par_fr%C3%A9quentation").read() 
page=bs4.BeautifulSoup(sock,features="lxml")

liste_lignes = page.find('table').findAll('tr')

for ligne in liste_lignes[1:] :
    
    freq = ligne.find('bdi')
    
    for sous_ligne in ligne.findAll('span') :
        lignes.append(sous_ligne.get('data-sort-value'))
        frequentation.append(float(freq.text.replace(',','.')))
        
lignes_freq = pd.DataFrame({'ligne' : lignes,'fréquentation' : frequentation})

#Ajout du score des lignes à la table lignes_quartiers
lignes_quartiers_freq = lignes_quartiers.merge(lignes_freq, on='ligne')



"""
4. Création du score de chaque quartier
"""

quartiers_freq = lignes_quartiers_freq[['c_qu','fréquentation']].groupby('c_qu').sum()
m = max(quartiers_freq['fréquentation'])
quartiers_freq['fréquentation'] = quartiers_freq['fréquentation']/m



""" 
5. Ajout du score à la base de données et export de la base de données augmentée
"""

donnees = gpd.read_file("donnees.geojson")

donnees_augmentees = donnees.join(quartiers_freq, on='id_quartier')
donnees_augmentees.rename(columns={'fréquentation': 'score_metro'}, inplace=True)

donnees_augmentees.to_file("donnees_augmentees.geojson", driver="GeoJSON",encoding = 'utf-8')
