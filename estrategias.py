import numpy as np
import pandas as pd


def backtesting(df, n_shares=2000, com=0.00125, initial_capital=1_000_000):
    """
    Simula un backtest de una estrategia de pares trading.

    Parámetros:
    df (DataFrame): DataFrame con las columnas 'MSFT', 'AMD', 'Spread_Signal', 'm' y 'Date'.
    n_shares (int): Número de acciones a operar por transacción.
    com (float): Comisión de la operación (proporción, ej. 0.00125 para 0.125%).
    initial_capital (float): Capital inicial para el backtesting.

    Retorna:
    list: Evolución del capital en el tiempo.
    """
    # Asegurar que los nombres de las columnas están correctos
    expected_columns = {'MSFT', 'AMD', 'Spread_Signal', 'm', 'Date'}
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Faltan columnas en el DataFrame: {missing_columns}")

    # Convertir la columna de fecha a datetime si no lo está
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")

    # Verificar si hay valores NaT en la columna Date
    if df["Date"].isna().sum() > 0:
        print("⚠️ Hay valores NaT en la columna Date. Verifica el formato de las fechas.")
        print(df[df["Date"].isna()])
        raise ValueError("Hay valores inválidos en la columna Date.")

    capital = initial_capital
    active_positions = []
    active_short_positions = []
    portfolio_value = [capital]

    for i, row in df.iterrows():
        # SHORT (Vender en corto si Spread_Signal > 1.5)
        if row["Spread_Signal"] > 1.5 and not active_short_positions:
            cost = row["MSFT"] * com * n_shares
            if capital > cost and capital > 250_000:
                capital -= cost
                active_short_positions.append({
                    "date": row["Date"],  # CORREGIDO
                    "bought_at": row["MSFT"],
                    "shares": n_shares
                })

        # LONG (Comprar si Spread_Signal > 1.5)
        if row["Spread_Signal"] > 1.5 and not active_positions:
            n_shares_adjusted = n_shares * row["m"]
            cost = (row["AMD"] * n_shares_adjusted) * (1 + com)
            if capital > cost and capital > 250_000:
                capital -= cost
                active_positions.append({
                    "date": row["Date"],  # CORREGIDO
                    "bought_at": row["AMD"],
                    "shares": n_shares_adjusted
                })

        # Cerrar SHORT y LONG cuando Spread_Signal < 0.05
        if row["Spread_Signal"] < 0.05 and df["Spread_Signal"].shift(1).loc[row.name] > 0.05:
            for position in active_short_positions:
                capital += (position["bought_at"] - row["MSFT"]) * n_shares
            active_short_positions = []

            for position in active_positions:
                capital += (row["AMD"] * n_shares_adjusted) * (1 - com)
            active_positions = []

        # SHORT si Spread_Signal < -1.5
        if row["Spread_Signal"] < -1.5 and not active_short_positions:
            n_shares_adjusted = n_shares * row["m"]
            cost = row["AMD"] * com * n_shares_adjusted
            if capital > cost and capital > 250_000:
                capital -= cost
                active_short_positions.append({
                    "date": row["Date"],  # CORREGIDO
                    "bought_at": row["AMD"],
                    "shares": n_shares_adjusted
                })

        # LONG si Spread_Signal < -1.5
        if row["Spread_Signal"] < -1.5 and not active_positions:
            cost = (row["MSFT"] * n_shares) * (1 + com)
            if capital > cost and capital > 250_000:
                capital -= cost
                active_positions.append({
                    "date": row["Date"],  # CORREGIDO
                    "bought_at": row["MSFT"],
                    "shares": n_shares
                })

        # Cerrar SHORT y LONG cuando Spread_Signal > 0
        if row["Spread_Signal"] > 0 and df["Spread_Signal"].shift(1).loc[row.name] < 0:
            for position in active_short_positions:
                capital += (position["bought_at"] - row["AMD"]) * n_shares_adjusted
            active_short_positions = []

            for position in active_positions:
                capital += (row["MSFT"] * n_shares) * (1 - com)
            active_positions = []

        # Calcular valor total del portafolio
        short_val = sum([(position["bought_at"] - row["MSFT"]) * n_shares for position in active_short_positions])
        long_val = sum([row["AMD"] * n_shares_adjusted for position in active_positions])
        portfolio_value.append(long_val + short_val + capital)

    return portfolio_value
