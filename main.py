import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from estrategias import backtesting
from analisis import adf_test, ols_regression, johansen_test

# 📌 Cargar los datos
msft = pd.read_csv("msft_stock_prices.csv")
amd = pd.read_csv("amd_stock_prices.csv")

# 📌 Convertir la fecha a formato datetime con el formato correcto (DD/MM/YY)
msft["Date"] = pd.to_datetime(msft["Date"], format="%d/%m/%y", errors="coerce")
amd["Date"] = pd.to_datetime(amd["Date"], format="%d/%m/%y", errors="coerce")

# 📌 Verificar si hay valores NaT en la columna Date
if msft["Date"].isna().sum() > 0 or amd["Date"].isna().sum() > 0:
    print("⚠️ Hay valores NaT en la columna Date. Verifica el formato de las fechas.")
    print(msft[msft["Date"].isna()])
    print(amd[amd["Date"].isna()])
    raise ValueError("❌ Hay fechas inválidas en la columna Date.")

# 📌 Unir los datos en un solo DataFrame
df = pd.DataFrame({
    "Date": msft["Date"],
    "MSFT": msft["Close"],
    "AMD": amd["Close"]
}).dropna()  # Eliminar filas con datos faltantes

# 📌 Aplicar pruebas de estacionariedad ADF
adf_test(df["MSFT"], "MSFT")
adf_test(df["AMD"], "AMD")

# 📌 Regresión OLS para encontrar relación lineal
model = ols_regression(df["MSFT"], df["AMD"])
residuals = model.resid

# 📌 Aplicar ADF a los residuos para verificar cointegración
adf_test(residuals, "Linear Relation")

# 📌 Prueba de cointegración de Johansen
johansen_test(df[["MSFT", "AMD"]])

# 📌 Calcular Spread_Signal (Z-Score de los residuos)
df["Spread_Signal"] = (residuals - residuals.mean()) / residuals.std()

# 📌 Calcular el ratio de cobertura dinámico (m)
df["m"] = model.params["AMD"]

# 📌 Guardar el archivo procesado
df.to_csv("datos_procesados.csv", index=False)

# 📌 Ejecutar el backtesting
portfolio_value = backtesting(df)

# 📌 Asegurar que los tamaños de las listas coincidan
df = df.iloc[:len(portfolio_value)]  # Cortar df si es más largo
portfolio_value = portfolio_value[:len(df)]  # Cortar portfolio_value si es más largo

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

# 📌 Graficar el Spread (Z-score)
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["Spread_Signal"], label="Spread (Z-score)", color='green')
plt.axhline(1.5, color="red", linestyle="--", label="+1.5 Sigma")
plt.axhline(-1.5, color="red", linestyle="--", label="-1.5 Sigma")
plt.xlabel("Fecha")
plt.ylabel("Spread (Z-score)")
plt.title("Señal de Trading basada en el Spread")
plt.legend()
plt.grid()
plt.show()

# 📌 Graficar la evolución del capital
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], portfolio_value, label="Capital", color='purple')
plt.xlabel("Fecha")
plt.ylabel("Capital")
plt.title("Evolución del Capital en el Backtesting")
plt.legend()
plt.grid()
plt.show()
