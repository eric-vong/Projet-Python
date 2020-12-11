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

data = standardisation(donnees.copy())
yindex = donnees.columns.get_loc("ref")
lasso1 = Lasso(fit_intercept=False,normalize=False)
lasso1.fit(np.delete(data, yindex, axis = 1),data[:,yindex])
print(lasso1.coef_)

donnees_meubles = donnees[donnees['meuble_bin']>0].copy() #POURQUOI TU MARCHES PAS
#donnees_meubles = donnees_meubles.drop(columns=['meuble_bin'])
yindex = donnees_meubles.columns.get_loc("ref")

reglinear = LinearRegression(fit_intercept=True,normalize=False)
reglinear.fit(np.delete(donnees_meubles, yindex, axis = 1),donnees_meubles[:,yindex])
print(reglinear.coef_)


donnees_non_meubles = donnees[donnees['meuble_bin']==0].copy()
donnees_non_meubles = donnees_non_meubles.drop(columns=['meuble_bin'])

reglinear1 = LinearRegression(fit_intercept=True,normalize=False)
reglinear1.fit(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])
print(reglinear1.coef_)

