import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen

def adf_test(series, ticker_name):
    """
    Aplica la prueba de Dickey-Fuller a una serie temporal.
    """
    result = adfuller(series)
    print(f"Resultados del ADF Test para {ticker_name}:")
    print(f"Estadístico ADF: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Conclusión:", "Estacionaria" if result[1] < 0.05 else "No estacionaria")
    print("-" * 50)

def ols_regression(Y, X):
    """
    Realiza una regresión OLS entre dos series temporales.
    """
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    print(model.summary())
    return model

def johansen_test(df):
    """
    Aplica el test de cointegración de Johansen.
    """
    test = coint_johansen(df, det_order=0, k_ar_diff=1)
    print("\n🔹 **Eigenvectors (Autovectores):**")
    print(test.evec)
    return test
