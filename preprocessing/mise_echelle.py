
from sklearn.preprocessing import MinMaxScaler

def mise_echelle(df,mini,maxi) :
    """
    Fonction renvoyant une version de la base de données df dans laquelle les colonnes ont été mises à l'échelle : 
    à l'aide de MinMaxScaler, les données sont comprises entre mini et maxi.
    
    ! df ne doit contenir que des variables numériques !
    """
    
    data = MinMaxScaler(feature_range=(mini, maxi)).fit(df).transform(df)
    
    return data
