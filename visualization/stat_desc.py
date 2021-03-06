import pandas as pd
import geopandas as gpd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer

donnees = gpd.read_file('donnees_augmentees.geojson')
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees=donnees.drop(['meuble_txt','max','min','id_quartier'],axis=1)
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)

sns.heatmap(donnees.corr(),annot = True,cmap='coolwarm',fmt='.1g')
plt.show()

sns.boxplot(x="piece", y="Prix_m2", data=donnees,whis=[0, 100], width=.6)
plt.show()

sns.boxplot(x="meuble_bin", y="Prix_m2", data=donnees,whis=[0, 100], width=.6)
plt.show()

sns.pairplot(donnees,hue='meuble_bin',palette='bright',height=1.9)
plt.show()

sns.pairplot(donnees,hue='piece',palette='bright',height=1.9)
plt.show()

donnees[donnees['meuble_bin'] == 1].plot(column = "Prix_m2",cmap = 'coolwarm',legend = True,legend_kwds = {'label':'Prix moyen au mètre carré (€) pour les appartements meublés'},figsize = (9,5))
plt.show()

donnees[donnees['meuble_bin'] == 0].plot(column = "Prix_m2",cmap = 'coolwarm',legend = True,legend_kwds = {'label':'Prix moyen au mètre carré (€) pour les appartements non meublés'},figsize = (9,5))
plt.show()
