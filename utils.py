import matplotlib.pyplot as plt

def plot_data(df, x_label, y_label, title):
    """
    Grafica una serie temporal.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
