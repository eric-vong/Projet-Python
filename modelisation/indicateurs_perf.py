
import pandas as pd

def indicateurs_perf (resultats) :
    """ 
    Fonction qui calcule les indicateurs de performance MAE, MSE, RMSE et MAPE 
    
    Entrée : 
        - resultats : DataFrame contenant les 'Loyers effectifs' et 'Loyers prédis' du jeu de données test
    
    ! Modifie la base resultats en rajoutant des colonnes !
    """   
    resultats['Ecarts_abs'] = abs(resultats['Loyers prédis']-resultats['Loyers effectifs'])
    resultats['Ecarts^2'] = resultats['Ecarts_abs']**2
    resultats['Percentage'] = resultats['Ecarts_abs']/resultats['Loyers effectifs']
    
    MAE = resultats['Ecarts_abs'].mean()
    MSE = resultats['Ecarts^2'].mean()
    RMSE = MSE**0.5
    MAPE = resultats['Percentage'].mean()

    return pd.DataFrame({'MAE' : [MAE], 'MSE' : [MSE], 'RMSE' : [RMSE], 'MAPE' : [MAPE]})