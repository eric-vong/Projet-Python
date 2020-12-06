"""
Creation d'une nouvelle base de données où toutes les variables sont sous forme numérique
"""

import pandas as pd
import geopandas

#Import des donneés :
import os
DONNEES_PATH = os.path.join(os.getcwd()[:-14]+"\\data","donnees_augmentees.geojson")
donnees = geopandas.read_file(DONNEES_PATH)

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer


"""
Variable 'meuble_txt' : transformée en une variable binaire 'meuble_bin' telle que :
    - meuble_bin = 1 si l'appartement est meublé
    - meuble_bin = 0 si l'appartement est non-meublé

Comme on n'a que deux modalités, on peut utiliser LabelEncoder.
"""

donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])

#Suppression de 'meuble_txt' :
donnees.drop('meuble_txt',axis=1,inplace=True)



"""
Variable 'id_quartier' : 
il y a 80 modalités, donc on crée 80 nouvelles variables 'q_i' pour 1<=i<=80 telles que : 
    - q_i = 1 si id_quartier = i
    - q_i = 0 si id_quartier != i

Comme on a 80 modalités, on utilise cette fois OneHotEncoder
"""

donnees = donnees.sort_values('id_quartier').reset_index()
ohe_id_quartier = pd.DataFrame(LabelBinarizer().fit_transform(donnees['id_quartier']))

# On renomme les colonnes sous la forme : q_[1-80]
colonnes = {}
for i in range(80) :
    colonnes[i] = 'q_'+str(i+1)
ohe_id_quartier.rename(columns=colonnes, inplace=True)

# Ajout des nouvelles variables et suppression de 'nom_quartier' et 'id_quartier' :
donnees = donnees.join(ohe_id_quartier)
donnees.drop(['nom_quartier','id_quartier','index'],axis=1,inplace=True)



"""
Variable 'epoque' : 
il y a 4 modalités, donc on crée 4 nouvelles variables 'epoque_i' pour 0<=i<=3 telles que : 
    - 'epoque_0' = 1 si 'epoque' = 'Avant 1946', et 0 sinon
    - 'epoque_1' = 1 si 'epoque' =  '1946-1970', et 0 sinon
    - 'epoque_2' = 1 si 'epoque' = '1971-1990', et 0 sinon
    - 'epoque_3' = 1 si 'epoque' =  'Apres 1990', et 0 sinon

On utilise encore une fois OneHotEncoder
"""

ohe_epoque = pd.DataFrame(LabelBinarizer().fit_transform(donnees['epoque']))

# On renomme les colonnes sous la forme : epoque_[0-79]

#donnees[['epoque']].head(10) #pour savoir comment renommer chaque colonne
colonnes = {0 : 'epoque_1', 1 : 'epoque_2', 2 : 'epoque_3', 3 : 'epoque_0'}  
ohe_epoque.rename(columns=colonnes, inplace=True)

# Ajout des nouvelles variables et suppression de 'epoque' :
donnees = donnees.join(ohe_epoque)
donnees.drop(['epoque'],axis=1,inplace=True)



"""
Export des donnees sous le nom 'donnees_num.geojson'
"""

donnees.to_file("donnees_num.geojson", driver="GeoJSON",encoding = 'utf-8')