#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
import contextily as ctx
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
import descartes


# In[2]:


#On importe les données, puis on transforme la variable textuelle "meuble_text" en variable binaire "meuble_bin"
#On choisit également de ne garder que la variable ref comme indicateur de prix car max et min sont une transformation affine de celle-ci.
donnees = gpd.read_file('donnees_augmentees.geojson')
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees=donnees.drop(['meuble_txt','max','min','id_quartier'],axis=1)
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)
donnees.sample(5)


# In[3]:


#Matrice de correlation
sns.heatmap(donnees.corr(),annot = True,cmap='coolwarm',fmt='.1g')


# In[4]:


sns.boxplot(x="piece", y="Prix_m2", data=donnees,
            whis=[0, 100], width=.6)
#La courbe dessinée par les médianes montre bien une décroissance convexe
#du prix du mètre carré en fonction du nombre de pièces.
#Comme on pouvait s'y attendre, le prix baisse, mais de moins en moins.


# In[5]:


sns.boxplot(x="meuble_bin", y="Prix_m2", data=donnees,
            whis=[0, 100], width=.6)
#Le prix du mètre carré d'un appartement meublé est plus cher que celui d'un non meublé.


# In[6]:


donnees=donnees.drop(['meuble_bin'],axis=1)
sns.pairplot(donnees,hue='piece',palette='bright',height=1.9)


# In[7]:


donnees = gpd.read_file('donnees_augmentees.geojson')
donnees=donnees.drop(['max','min','piece','id_quartier'],axis=1)
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)
sns.pairplot(donnees,hue='meuble_bin',palette='bright',height=1.9)


# In[8]:


#On réimporte les données pour avoir la base initiales 
donnees = gpd.read_file('donnees_augmentees.geojson')
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees=donnees.drop(['meuble_txt','max','min','id_quartier'],axis=1)
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)
donnees.sample(5)


# In[26]:


donnees.plot(column = "Prix_m2",cmap = 'coolwarm',legend = True,
             legend_kwds = {'label':'Prix moyen au mètre carré (€)'},
            figsize = (10,6))
#Carte des prix
donnees[donnees['meuble_bin'] == 1].plot(column = "Prix_m2",cmap = 'coolwarm',legend = True,
             legend_kwds = {'label':'Prix moyen au mètre carré (€) pour les appartements meublés'},
            figsize = (9,5))
#Carte des prix pour les appartements non meublés

donnees[donnees['meuble_bin'] == 0].plot(column = "Prix_m2",cmap = 'coolwarm',legend = True,
             legend_kwds = {'label':'Prix moyen au mètre carré (€) pour les appartements non meublés'},
            figsize = (9,5))
#Carte des prix pour les appartements non meublés


# In[11]:


donnees.plot(column = "distance_centre_paris",legend = True,
             legend_kwds = {'label':'Distance au centre de Paris (km)'},
            figsize = (10,6))
#Vérification graphique de la distance au centre de Paris


# In[25]:


donnees.plot(column = "piece",cmap = 'coolwarm',legend = True,
             legend_kwds = {'label':'nombre de piece moyen par appartement par quartier'},
            figsize = (9,5))
#Carte du nombre moyen de pièce par appartement dans chaque quartier

