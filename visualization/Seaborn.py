import pandas as pd
import geopandas as gpd
import contextily as ctx
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer

#On importe les données, puis on transforme la variable textuelle "meuble_text" en variable binaire "meuble_bin"
#On choisit également de ne garder que la variable ref comme indicateur de prix car max et min sont une transformation affine de celle-ci.
donnees = gpd.read_file('donnees_augmentees.geojson')
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees=donnees.drop(['meuble_txt','max','min','id_quartier'],axis=1)
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)
donnees.sample(5)


#Matrice de correlation
sns.heatmap(donnees.corr(),annot = True,cmap='coolwarm',fmt='.1g')


sns.boxplot(x="piece", y="Prix_m2", data=donnees,
            whis=[0, 100], width=.6)
#La courbe dessinée par les médianes montre bien une décroissance convexe
#du prix du mètre carré en fonction du nombre de pièces.
#Comme on pouvait s'y attendre, le prix baisse, mais de moins en moins.



sns.boxplot(x="meuble_bin", y="Prix_m2", data=donnees,
            whis=[0, 100], width=.6)
#Le prix du mètre carré d'un appartement meublé est plus cher que celui d'un non meublé.


donnees=donnees.drop(['meuble_bin'],axis=1)
sns.pairplot(donnees,hue='piece',palette='bright',height=1.9)


donnees = gpd.read_file('donnees_augmentees.geojson')
donnees=donnees.drop(['max','min','piece','id_quartier'],axis=1)
donnees['meuble_bin'] = 1 - LabelEncoder().fit_transform(donnees['meuble_txt'])
donnees.rename(columns={'ref': 'Prix_m2'}, inplace=True)
sns.pairplot(donnees,hue='meuble_bin',palette='bright',height=1.9)

