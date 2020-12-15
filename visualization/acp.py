import geopandas as gpd
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
import os

#On importe les données

PREPROCESSING_DIR = os.getcwd()[:-13]+"\Projet_Python\data"
DONNEES_NUM_PATH = os.path.join(PREPROCESSING_DIR,"donnees_augmentees.geojson")
donnees = gpd.read_file(DONNEES_NUM_PATH)

#Numérisation des données

donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
ohe_epoque = pd.DataFrame(LabelBinarizer().fit_transform(donnees['epoque']))
colonnes = {0 : 'epoque_1', 1 : 'epoque_2', 2 : 'epoque_3', 3 : 'epoque_0'}  
ohe_epoque.rename(columns=colonnes, inplace=True)
donnees = donnees.join(ohe_epoque)
todrop = ['nom_quartier','id_quartier','min','max','epoque','meuble_txt','geometry','ref']
donnees.drop(todrop,axis=1,inplace=True)
donnees = donnees.fillna(0)

#On fait une ACP, on doit scaler nos valeurs

features = [donnees.columns[i] for i in range(len(donnees.columns))]
x = donnees.loc[:,features].values
x = StandardScaler().fit_transform(x)
n_components = len(donnees.columns)
pca = PCA(n_components=n_components)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component' + str(i+1) for i in range(len(donnees.columns))])

#Interprétation de l'ACP

pca.explained_variance_ratio_

#On voit que les 2 dernières variables de l'ACP sont inutiles (contribution de 2.5%), on peut prendre 7 composantes principales en négligeant la 3ème en partant de la fin car elle est inférieure à 1/9

ind = np.arange(0, n_components)
(fig, ax) = plt.subplots(figsize=(8, 6))
sns.pointplot(x=ind, y=pca.explained_variance_ratio_)
ax.set_title('Scree plot')
ax.set_xticks(ind)
ax.set_xticklabels(ind)
ax.set_xlabel('Component Number')
ax.set_ylabel('Explained Variance')
plt.show()

(fig, ax) = plt.subplots(figsize=(8, 8))
for i in range(0, pca.components_.shape[1]):
        ax.arrow(0,0,pca.components_[0, i],pca.components_[1, i],head_width=0.1,head_length=0.1)
        plt.text(pca.components_[0, i] + 0.05,pca.components_[1, i] + 0.05,donnees.columns.values[i])

an = np.linspace(0, 2 * np.pi, 100)
plt.plot(np.cos(an), np.sin(an)) #Cercle unité pour échelle
plt.axis('equal')
ax.set_title('Variable factor map')
plt.show()
