import ipywidgets as widgets
import matplotlib.pyplot as plt
import yfinance as yf
from IPython.display import display


def plot_chart(interval):
    # '15m' only works for the last 60 days, so we adjust 'period' dynamically
    period = "30d" if interval == "15m" else "60d"

    df = yf.download("EURUSD=X", period=period, interval=interval)

    if df is None or df.empty:
        print(f"No data returend for {interval}")
        return
    if "Close" not in df.columns:
        print(f"No 'Close' column in data for {interval}")
        return

    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df["Close"], label=f"EUR/USD ({interval})")
    plt.title(f"EUR/USD Exchange Rate — {interval} Timeframe")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.show()


# Create dropdown toggle
toggle = widgets.ToggleButtons(
    options=["15m", "1h", "1d"],
    description="Timeframe:",
    button_style="info",
)

widgets.interactive(plot_chart, interval=toggle)