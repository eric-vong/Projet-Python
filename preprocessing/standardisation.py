
from sklearn.preprocessing import StandardScaler


def standardisation(df) :
    """
    Fonction renvoyant la version standardisée d'une base de données df passée en argument.
    
    ! df ne doit contenir que des variables numériques !
    """
    
    data = StandardScaler().fit(df).transform(df)
    
    return data

