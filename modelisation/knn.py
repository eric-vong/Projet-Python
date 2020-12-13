"""
Modèle kNN (k Nearest Neighbors):
  
Modèle de régression à partir de données sur lesquelles une métrique est définie.
On procède comme suit : 
    1) Preprocessing : on sélectionne les variables d'intérêt, que l'on met à la même échelle
       On divise également les données en un jeu test et un jeu d'entrainement
    2) Implémentation d'une fonction qui réalise le modèle kNN
    3) Choix de la valeur de l'hyperparamètre k
    4) Modèle kNN avec la valeur de l'hyperparamètre choisie à l'étape 3) et visualisation des résultats
"""

import geopandas as gpd
import pandas as pd

#Import des donneés :
import os
PREPROCESSING_DIR = os.getcwd()[:-13]+"\\preprocessing"
DONNEES_NUM_PATH = os.path.join(PREPROCESSING_DIR,"donnees_num.geojson")
donnees = gpd.read_file(DONNEES_NUM_PATH)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn import neighbors

from math import sqrt


"""
1) Preprocessing : 
    - On sélectionne les variables d'intéret 
    - On met à la même échelle toutes les variables explicatives, en les ramenant entre 0 et 1 par exemple.
"""
Y = donnees['ref']
X = donnees[['piece', 'distance_centre_paris', 'meuble_bin']]

import sys
sys.path.insert(1, PREPROCESSING_DIR)
from mise_echelle import mise_echelle

X = mise_echelle(X,0,1)

#Création d'un jeu de données test et d'un jeu de données d'entrainement :
xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size = 0.2, random_state = 0)



"""
2) Implémentation d'une fonction qui réalise le modèle kNN, et d'une fonction calculant les indicateurs de performance du modèle
"""

def kNN(xTrain, xTest, yTrain, yTest,k) :
    """ Fonction qui réalise un modèle kNN. 
    Entrées : 
        - xTrain,yTrain : jeux de données sur lesquels entrainer le modèle
        - xTest,yTest : jeux de données sur lesquels faire les prédictions
        - k : hyperparamètre correspondant au nombre de voisins à considérer 
    
    Sortie :
        - resultats : base de données contenant les loyers à prédire de yTest, et les loyers prédis par le modèle à partir de xTest
    """
    #Entrainement du modèle sur le jeu de données d'entrainement :
    knn = neighbors.KNeighborsRegressor(n_neighbors = k,metric="manhattan",weights="distance")  
    knn.fit(xTrain, yTrain)  
    
    #Prédictions sur le jeu de données test :
    prediction = knn.predict(xTest) 
    
    resultats = pd.DataFrame({'Loyers effectifs': list(yTest), 'Loyers prédis': list(prediction)})
    return resultats


def indicateurs_perf (resultats) :
    """ 
    Fonction qui calcule les indicateurs de performance MAE, MSE, RMSE et MAPE à partir de la base de données résultats du modèle knn.
    
    ! Modifie la base resultats en rajoutant des colonnes !
    """   
    resultats['Ecarts_abs'] = abs(resultats['Loyers prédis']-resultats['Loyers effectifs'])
    resultats['Ecarts^2'] = resultats['Ecarts_abs']**2
    resultats['Percentage'] = resultats['Ecarts_abs']/resultats['Loyers effectifs']
    
    MAE = resultats['Ecarts_abs'].mean()
    MSE = resultats['Ecarts^2'].mean()
    RMSE = MSE**0.5
    MAPE = resultats['Percentage'].mean()

    return pd.DataFrame({'MAE' : [MAE], 'MSE' : [MSE], 'RMSE' : [RMSE], 'MAPE' : [MAPE]})




"""
3) Choix de l'hyperparamètre k :

On réalise un graphique représentant l'erreur RMSE sur le jeu de données test en fonction de la valeur de $k$ choisie.
On cherche à identifier le meilleur paramètre k, en cherchant un point d'inflexion
"""

rmse = [] 

for k in range(1,21):
    resultats = kNN(xTrain, xTest, yTrain, yTest,k)
    indicateurs = indicateurs_perf (resultats)
    rmse.append(indicateurs['RMSE'][0])
    
sns.set_style("whitegrid")
sns.lineplot(x=[k for k in range(1,21)], y=rmse).set(title = r"Erreur RMSE du KNN sur le jeu de données test en fonction de l'hypermaramètre $k$ choisi", xlabel=r'$k$', ylabel='RMSE')
plt.axvline(3,0,3,color="red",linestyle="--",label = r"$k$=3")
plt.legend(loc='upper right')



"""
4) Modèle kNN avec la valeur de l'hyperparamètre choisie à l'étape 3) : k=3

Pour visualiser les résultats :
    - on affiche la table des indicateurs de performance 
    - on trace un scatter plot des loyers prédis en fonction des loyers effectifs pour le jeu de données test
    - on trace la répartition des écarts entre loyers prédis et effectifs pour le jeu de données test (en valeur absolue)
"""

k=3

resultats = kNN(xTrain, xTest, yTrain, yTest,k)
indicateurs = indicateurs_perf (resultats)

print("Indicateurs de performance du modèle kNN avec k="+str(k))
print(indicateurs)

fig,ax = plt.subplots(1, 2, figsize=(12, 6)) 
   
fig.suptitle(r'Modèle kNN avec $k=$'+str(k))
     
#Scatter plot :
sns.scatterplot(data=resultats, x='Loyers effectifs',y='Loyers prédis',ax = ax[0])
identite = [i for i in range(int(resultats['Loyers prédis'].min()),int(resultats['Loyers prédis'].max()))]
sns.lineplot(x=identite,y=identite,style=True, dashes=[(2,2)],color="red",ax = ax[0])
ax[0].set_title("Loyers prédis en fonction des loyers \n effectifs pour le jeu de données test")
        
#Densité :
sns.kdeplot(resultats['Ecarts_abs'],ax = ax[1], fill=True, alpha=.3)
ax[1].set_title("Répartition des écarts entre loyers prédis \n et loyers effectifs pour le jeu de données test \n (en valeur absolue)") 

