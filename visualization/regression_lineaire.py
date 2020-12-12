#On s'intéresse ici à la prédiction linéaire par le modèle de LASSO.
#On trace graphiquement les prédictions, pour avoir une visualisation graphique on a fait le choix de tracer d'une part les biens meublés et de l'autre les non meublés (puisque c'est une variable binaire)

import geopandas
import os
PREPROCESSING_DIR = os.getcwd()[:-13]+"\Projet_Python\preprocessing"
DONNEES_NUM_PATH = os.path.join(PREPROCESSING_DIR,"donnees_num.geojson")
donnees = geopandas.read_file(DONNEES_NUM_PATH)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.linear_model import LinearRegression
todrop = ['q_'+str(i+1) for i in range(80)]+['geometry','min','max','superficie_quartier','score_metro','epoque_1','epoque_2','epoque_3','epoque_0']
donnees.drop(todrop,axis=1,inplace=True)

donnees_meubles = donnees[donnees['meuble_bin']>0].copy()
donnees_meubles = donnees_meubles.drop(columns=['meuble_bin'])
donnees_meubles = donnees_meubles.to_numpy()

donnees_non_meubles = donnees[donnees['meuble_bin']==0].copy()
donnees_non_meubles = donnees_non_meubles.drop(columns=['meuble_bin'])
donnees_non_meubles = donnees_non_meubles.to_numpy()

yindex = donnees.columns.get_loc("ref")

reglinear = LinearRegression(fit_intercept=True,normalize=False)

reglinear.fit(np.delete(donnees_meubles, yindex, axis = 1),donnees_meubles[:,yindex])
reglinear.score(np.delete(donnees_meubles, yindex, axis = 1),donnees_meubles[:,yindex])

print(reglinear.coef_)
print(reglinear.intercept_) #On s'attendrait normalement à un prix à l'ordonné plus bas et qui monte avec le nombre de pièces

reglinear.fit(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])
reglinear.score(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])

print(reglinear.coef_)
print(reglinear.intercept_) #Même commentaire
#Ordonnée à l'origine plus haute pour meublé, c'est ce à quoi on s'attend

