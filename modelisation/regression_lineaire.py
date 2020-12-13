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
from sklearn.metrics import mean_squared_error
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

pieces_meuble,distance_centre_meuble = reglinear.coef_
print(pieces_meuble,distance_centre_meuble)
ordonnee_meuble = reglinear.intercept_

reglinear.fit(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])
reglinear.score(np.delete(donnees_non_meubles, yindex, axis = 1),donnees_non_meubles[:,yindex])

pieces_non_meuble,distance_centre_non_meuble =reglinear.coef_
ordonnee_non_meuble = reglinear.intercept_ 

ref_meuble,piec_meuble,dist_meuble = donnees_meubles[:,0],donnees_meubles[:,1],donnees_meubles[:,2]
ref_non_meuble,piec_non_meuble,dist_non_meuble = donnees_non_meubles[:,0],donnees_non_meubles[:,1],donnees_non_meubles[:,2]

ref_predict_meuble = piec_meuble*pieces_meuble+dist_meuble*distance_centre_meuble+ordonnee_meuble
ref_predict_non_meuble = piec_meuble*pieces_non_meuble+dist_meuble*distance_centre_non_meuble+ordonnee_non_meuble

mean_squared_error(ref_meuble,ref_predict_meuble)
mean_squared_error(ref_non_meuble,ref_predict_non_meuble)

xx,yy=np.meshgrid(range(5),range(8))
z_meuble = xx*pieces_meuble+yy*distance_centre_meuble+ordonnee_meuble
z_non_meuble = xx*pieces_non_meuble+yy*distance_centre_non_meuble+ordonnee_non_meuble

plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z_meuble)
plt3d.plot_surface(xx, yy, z_non_meuble)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(piec_meuble,dist_meuble,ref_meuble,c='red',label='Meublé')
ax.scatter(piec_non_meuble,dist_non_meuble,ref_non_meuble,c='blue',label='Non meublé')
ax.set_xlabel('Nombre de pièce')
ax.set_ylabel('Distance du centre de Paris')
ax.set_zlabel('Prix du m^2')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z_meuble)
ax = plt.gca()
ax.hold(True)
ax.scatter(piec_meuble,dist_meuble,ref_meuble,c='red')
ax.set_xlabel('Nombre de pièce')
ax.set_ylabel('Distance du centre de Paris')
ax.set_zlabel('Prix du m^2')
plt.title('Régression linéaire pour les appartements meublés')
plt.legend()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z_non_meuble)
ax = plt.gca()
ax.scatter(piec_non_meuble,dist_non_meuble,ref_non_meuble,c='red')
ax.set_xlabel('Nombre de pièce')
ax.set_ylabel('Distance du centre de Paris')
ax.set_zlabel('Prix du m^2')
plt.title('Régression linéaire pour les appartements non meublés')
plt.legend()
plt.show()

resultats_meuble = pd.DataFrame({'Loyers effectifs' : ref_meuble, 'Loyers prédis' : ref_predict_meuble})
resultats_non_meuble = pd.DataFrame({'Loyers effectifs' : ref_non_meuble, 'Loyers prédis' : ref_predict_non_meuble})

fig,ax = plt.subplots(1, 2, figsize=(12, 6)) 
sns.scatterplot(data=resultats_meuble, x='Loyers effectifs',y='Loyers prédis',ax = ax[0])
identite = [i for i in range(int(resultats_meuble['Loyers effectifs'].min()),int(resultats_meuble['Loyers effectifs'].max()))]
sns.lineplot(x=identite,y=identite,style=True, dashes=[(2,2)],color="red",ax = ax[0])
ax[0].set_title("Loyers prédis en fonction des loyers effectifs")

sns.kdeplot(resultats_meuble['Ecarts_abs'],ax = ax[1], fill=True, alpha=.3)
ax[1].set_title("Répartition des écarts entre loyers prédis et loyers effectifs \n (en valeur absolue)") 


fig,ax = plt.subplots(1, 2, figsize=(12, 6)) 
sns.scatterplot(data=resultats_non_meuble, x='Loyers effectifs',y='Loyers prédis',ax = ax[0])
identite = [i for i in range(int(resultats_non_meuble['Loyers effectifs'].min()),int(resultats_non_meuble['Loyers effectifs'].max()))]
sns.lineplot(x=identite,y=identite,style=True, dashes=[(2,2)],color="red",ax = ax[0])
ax[0].set_title("Loyers prédis en fonction des loyers effectifs \n ")
    
sns.kdeplot(resultats_non_meuble['Ecarts_abs'],ax = ax[1], fill=True, alpha=.3)
ax[1].set_title("Répartition des écarts entre loyers prédis et loyers effectifs \n (en valeur absolue)") 