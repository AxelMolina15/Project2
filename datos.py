import pandas as pd
import yfinance as yf

def get_stock_prices(ticker, period="10y"):
    """
    Descarga los datos históricos de un ticker de Yahoo Finance.
    """
    data = yf.download(ticker, period=period)
    return data

def load_stock_data(file_name):
    """
    Carga los datos desde un archivo CSV.
    """
    return pd.read_csv(file_name).dropna()

def format_dates(df):
    """
    Convierte la columna de fecha a formato datetime.
    """
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    return df
