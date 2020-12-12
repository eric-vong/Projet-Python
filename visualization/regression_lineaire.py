#On s'intéresse ici à la prédiction linéaire par le modèle de LASSO.
#On trace graphiquement les prédictions, pour avoir une visualisation graphique on a fait le choix de tracer d'une part les biens meublés et de l'autre les non meublés (puisque c'est une variable binaire)

import geopandas
import os
PREPROCESSING_DIR = os.getcwd()[:-13]+"\Projet_Python\preprocessing"
DONNEES_NUM_PATH = os.path.join(PREPROCESSING_DIR,"donnees_num.geojson")
donnees = geopandas.read_file(DONNEES_NUM_PATH)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

pieces_meuble,distance_centre_meuble = reglinar.coef_
ordonnee_meuble = reglinear.intercept_ #Le prix au m^2 descend bien avec le nombre de pièces, rendements marginaux décroissants

reglinear.fit(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])
reglinear.score(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])

pieces_non_meuble,distance_centre_non_meuble =reglinear.coef_
ordonnee_non_meuble = reglinear.intercept_ #Même commentaire
#Ordonnée à l'origine plus haute pour meublé, c'est ce à quoi on s'attend

###Visualisation de la régression
ref_meuble,piec_meuble,dist_meuble = donnees_meubles[:,0],donnees_meubles[:,1],donnees_meubles[:,2]
ref_non_meuble,piec_non_meuble,dist_non_meuble = donnees_non_meubles[:,0],donnees_non_meubles[:,1],donnees_non_meubles[:,2]

#Visualisation des points 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(piec_meuble,dist_meuble,ref_meuble,c='red')
ax.scatter(piec_non_meuble,dist_non_meuble,ref_non_meuble,c='blue')
ax.set_xlabel('Nombre de pièce')
ax.set_ylabel('Distance du centre de Paris')
ax.set_zlabel('Prix du m^2')
plt.show()