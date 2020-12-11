"""
Modèle Lasso :
    
Modèle permettant de sélectionner des variables d'intérêt de notre base de données.
On procède comme suit : 
    1) Preprocessing : on sélectionne les variables à tester, on supprime l'une des variables de chaque groupe de variables corrélées et on standardise les variables restantes
    2) Choix de la valeur de l'hyperparamètre alpha.
    3) Modèle LASSO avec la valeur de l'hypermaramètre choisie à l'étape 2). 
"""

import geopandas

#Import des donneés :
import os
PREPROCESSING_DIR = os.getcwd()[:-13]+"\\preprocessing"
DONNEES_NUM_PATH = os.path.join(PREPROCESSING_DIR,"donnees_num.geojson")
donnees = geopandas.read_file(DONNEES_NUM_PATH)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import Lasso, lasso_path

"""
Etape 1)
    
Suppression des variables que l'on en veut pas tester : 
    - 'min', 'max'
    - 'geometry'
Suppression de l'une des variables de chaque groupe de variables corrélées :
    - 'q_80' pour le groupe de variables corrélées 'q_i', 1<=i<=80
    - 'epoque_0' pour le groupe de variables corrélées 'epoque_i', 0<=i<=3
Et standardisation des variables restantes
"""

donnees.drop(['min','max','geometry','q_80','epoque_0'],axis=1,inplace=True)

import sys
sys.path.insert(1, PREPROCESSING_DIR)
from standardisation import standardisation

data = standardisation(donnees)



"""
Etape 2) 
    
Pour le choix de la valeur de l'hyperparamètre alpha, on teste le modèle LASSO avec différentes valeurs de alpha.
On trace ensuite le nombre de variables sélectionnées par le modèle en fonction de alpha, pour choisir notre valeur de l'hyperparamètre.    
"""

yindex = donnees.columns.get_loc("ref")
alphas = np.array([0.001,0.005]+[i/100 for i in range(1,30)]+[0.5,0.8,1.0])

alpha_for_path, coefs_lasso, _ = lasso_path(np.delete(data, yindex, axis = 1),data[:,yindex],alphas=alphas)
nb_non_zero = np.apply_along_axis(func1d=np.count_nonzero,arr=coefs_lasso,axis=0)

sns.set_style("whitegrid")
sns.lineplot(y=nb_non_zero, x=alpha_for_path).set(title = r"Nombres de variables sélectionnées par Lasso en fonction de l'hyper paramètre $\alpha$ choisi", xlabel=r'$\alpha$', ylabel='Nombre de variables sélectionnées')
plt.axvline(0.15, 0,80,color="red",linestyle="--",label = r"$\alpha$=0.15")
plt.legend(loc='upper right')
#plt.show()



"""
Etape 3)

Modèle LASSO avec pour hyperparamètre alpha = 0.15
"""

alpha = 0.15

lasso1 = Lasso(fit_intercept=False,normalize=False, alpha = alpha)
lasso1.fit(np.delete(data, yindex, axis = 1),data[:,yindex])

#print("Coefficients estimés par modèle LASSO avec alpha = "+str(alpha)+":")
#print(np.abs(lasso1.coef_))

#print("Variables sélectionnées par modèle LASSO avec alpha = "+str(alpha)+":")
#print(donnees.drop("ref", axis = 1).columns[np.abs(lasso1.coef_)>0])