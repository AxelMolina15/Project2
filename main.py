import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import numpy as np
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

msft = pd.read_csv('/Users/axelmolina/Desktop/Noveno Semestre/Trading/Pairs Trading/msft_stock_prices.csv').dropna()
amd = pd.read_csv('/Users/axelmolina/Desktop/Noveno Semestre/Trading/Pairs Trading/amd_stock_prices.csv').dropna()

amd.index
amd.head()
msft.head()

msft['Date'] = pd.to_datetime(msft['Date'])
msft.dtypes

# Crear la figura y los ejes
fig, ax1 = plt.subplots()

# Graficar MSFT en el primer eje
ax1.set_xlabel('Fecha')
ax1.set_ylabel('MSFT', color='tab:blue')
ax1.plot(msft.index, msft['Close'], color='tab:blue', label='MSFT')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Crear un segundo eje para AMD
ax2 = ax1.twinx()
ax2.set_ylabel('AMD', color='tab:red')
ax2.plot(amd.index, amd['Close'], color='tab:red', label='AMD')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Añadir leyenda
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Mostrar el gráfico
plt.title('Comparación de precios de MSFT y AMD')
plt.tight_layout()  # Ajusta para que no se solapen los elementos
plt.show();

msft_w_dates = msft
amd_w_dates = msft

msft = msft.Close
amd = amd.Close

def adf_test(series, ticker_name):
    result = adfuller(series)
    print(f"Resultados del ADF Test para {ticker_name}:")
    print(f"Estadístico ADF: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Conclusión:", "Estacionaria" if result[1] < 0.05 else "No estacionaria")
    print("-" * 50)

# Aplicar el test a cada serie
adf_test(msft, "MSFT")
adf_test(amd, "AMD")

# Alinear datos en el tiempo (por si alguna fecha falta en una de las series)
df = pd.concat([msft, amd], axis=1, keys=["MSFT", "AMD"]).dropna()

# Definir variables dependiente (Y) e independiente (X)
X = df["AMD"]  # Variable independiente
Y = df["MSFT"]   # Variable dependiente

# Agregar constante para la regresión
X = sm.add_constant(X)

# Ajustar modelo OLS
model = sm.OLS(Y, X).fit()

# Imprimir resumen de la regresión
print(model.summary())

residuals = model.resid

# Aplicar adf a residuales
adf_test(residuals, "Linear Relation")

df = pd.concat([msft, amd], axis = 1)
df.columns = ["msft", "amd"]
df

johansen_test = coint_johansen(df, det_order=0, k_ar_diff=1)

# 📌 4. Extraer y mostrar resultados clave
print("📊 **Resultados del Test de Cointegración de Johansen** 📊")

# Eigenvalues (Autovalores)
#print("\n🔹 **Eigenvalues (Autovalores):**")
#print(johansen_test.eig)

# Eigenvectors (Autovectores)
print("\n🔹 **Eigenvectors (Autovectores):**")
print(johansen_test.evec)
'''
# Trace Statistics
print("\n🔹 **Trace Statistics:**")
print(johansen_test.lr1)

# Eigenvalue Statistics
print("\n🔹 **Eigenvalue Statistics:**")
print(johansen_test.lr2)

# Valores críticos a diferentes niveles (90%, 95%, 99%)
print("\n🔹 **Valores Críticos (Trace Test):**")
print(johansen_test.cvt)

print("\n🔹 **Valores Críticos (Eigenvalue Test):**")
print(johansen_test.cvm)
'''

u_t_list = []
for i in range (0,len(df)):
    u_t = johansen_test.evec[1,0]*df.amd[i] + johansen_test.evec[0,0]*df.msft[i]
    u_t_list.append(u_t)

# Crear la figura y los ejes
fig, ax = plt.subplots()

msft_w_dates["u_t_list"]= u_t_list

# Graficar u_t_list con las fechas correspondientes
ax.set_xlabel('Fecha')
ax.set_ylabel('u_t', color='tab:green')
ax.plot(msft_w_dates.index, u_t_list, color='tab:green', label='u_t')
ax.tick_params(axis='y', labelcolor='tab:green')

# Añadir leyenda
ax.legend(loc='upper left')

# Mostrar el gráfico
plt.title('u_t sin normalizar')
plt.tight_layout()  # Ajusta para que no se solapen los elementos
plt.show();

def normalize_z_score(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    normalized_data = [(x - mean) / std_dev for x in data]
    return normalized_data

normalized_u_t_list = normalize_z_score(u_t_list)

mean = np.mean(normalized_u_t_list)
std_dev = np.std(normalized_u_t_list)

# Definir los valores para 1 sigma, 1.25 sigma, y 2 sigma (positivos y negativos)
sigma_values = {
    '1 sigma': (mean - std_dev, mean + std_dev),
    '1.5 sigma': (mean - 1.5 * std_dev, mean + 1.5 * std_dev),
    '2 sigma': (mean - 2 * std_dev, mean + 2 * std_dev),
}

# Crear la figura y los ejes
fig, ax = plt.subplots()

for key, (lower, upper) in sigma_values.items():
    ax.axhline(y=lower, color='orange' if key == '1 sigma' else 'green' if key == '1.25 sigma' else 'red', linestyle='--', label=f'{key}')
    ax.axhline(y=upper, color='orange' if key == '1 sigma' else 'green' if key == '1.25 sigma' else 'red', linestyle='--')

# Graficar u_t_list con las fechas correspondientes
ax.set_xlabel('Fecha')
ax.set_ylabel('u_t', color='tab:green')
ax.plot(msft_w_dates.index, normalized_u_t_list, color='tab:green', label='u_t')
ax.tick_params(axis='y', labelcolor='tab:green')

# Añadir leyenda
ax.legend(loc='upper left')

# Mostrar el gráfico
plt.title('u_t normalizada')
plt.tight_layout()  # Ajusta para que no se solapen los elementos
plt.show();

df["Datetime"] = msft_w_dates.Date
df["Spread_Signal"] = normalized_u_t_list
df["m"] = list_m
df

capital = 1_000_000
com = 0.125 / 100
n_shares = 1800

active_positions = []
active_short_positions = []
portfolio_value = [capital]
Closeactual = 0

for i, row in df.iterrows():
    # update the kalman filter

    # Por arriba
    # Shortear
    if row.Spread_Signal > 1.5 and active_short_positions == []:
        Close = row.msft
        cost = Close * com * n_shares
        # Do we have enough cash?
        if (capital > cost) and (capital > 250_000):
            # Spend money
            capital -= cost
            # Add position to portfolio
            active_short_positions.append({
                "datetime": row.Datetime,
                "bought_at": Close,
                "shares": n_shares
            })
    # Comprar
    if row.Spread_Signal > 1.5 and active_positions == []:
        Closebuy = row.amd
        # How expensive is the operation
        n_shares_adjusted = n_shares * row.m  # * 1.88
        cost = (Closebuy * n_shares_adjusted) * (1 + com)
        # So we have enough cash?
        if (capital > cost) and (capital > 250_000):
            # Spend Money
            capital -= cost
            # Add the position to a portfolio
            active_positions.append({
                "datetime": row.Datetime,
                "bought_at": Closebuy,
                "shares": n_shares
            })

        # Close Short positions
    if row.Spread_Signal < 0 and (df.Spread_Signal.shift(1).loc[row.name] > 0):
        # Close all positions in the portfolio
        for position in active_short_positions:
            cost = row.msft * n_shares * com  # Comisión por comprar
            value = (position["bought_at"] - row.msft) * n_shares
            capital += (value - cost)
        active_short_positions = []

        # Close long positions
    if row.Spread_Signal < 0 and (df.Spread_Signal.shift(1).loc[row.name] > 0):
        # Close all positions in the portfolio
        for position in active_positions:
            Closeactual = row.amd
            value = Closeactual * n_shares_adjusted * (1 - com)
            capital += value
        active_positions = []

    # Por abajo
    # Shortear
    if row.Spread_Signal < -1.5 and active_short_positions == []:
        Close = row.amd
        n_shares_adjusted = n_shares * row.m  # * 1.88
        cost = Close * com * n_shares_adjusted
        # Do we have enough cash?
        if (capital > cost) and (capital > 250_000):
            # Spend money
            capital -= cost
            # Add position to portfolio
            active_short_positions.append({
                "datetime": row.Datetime,
                "bought_at": Close,
                "shares": n_shares  #
            })

    # Comprar
    if row.Spread_Signal < -1.5 and active_positions == []:
        Closebuy = row.msft
        # How expensive is the operation
        cost = (Closebuy * n_shares) * (1 + com)
        # So we have enough cash?
        if (capital > cost) and (capital > 250_000):
            # Spend Money
            capital -= cost
            # Add the position to a portfolio
            active_positions.append({
                "datetime": row.Datetime,
                "bought_at": Close,
                "shares": n_shares
            })

        # Close Short positions
    if row.Spread_Signal > 0 and (df.Spread_Signal.shift(1).loc[row.name] < 0):
        # Close all positions in the portfolio
        for position in active_short_positions:
            cost = row.amd * n_shares_adjusted * com  # Comisión por comprar
            value = (position["bought_at"] - row.amd) * n_shares_adjusted
            capital += (value - cost)
        active_short_positions = []

        # Close long positions
    if row.Spread_Signal > 0 and (df.Spread_Signal.shift(1).loc[row.name] < 0):
        # Close all positions in the portfolio
        for position in active_positions:
            Closeactual = row.msft
            value = (Closeactual * n_shares) * (1 - com)
            capital += value
        active_positions = []

    # Calculate portfolio value
    short_val = sum([(position["bought_at"] - Close) * n_shares for position in active_short_positions])
    num_long_pos = len(active_positions)
    long_pos_val = Close * num_long_pos * n_shares
    # long_pos_val = Closeactual * num_long_pos * n_shares
    portfolio_value.append(long_pos_val + short_val + capital)


plt.plot(portfolio_value)


