import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web


moving_average_a = 50
moving_average_b = 200

start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()
stock = 'MSFT'

data = web.DataReader(stock, 'yahoo', start, end)
data[f'Simple Moving Average -{moving_average_a} days'] = data['Adj Close'].rolling(window=moving_average_a).mean()
data[f'Simple Moving Average -{moving_average_b} days'] = data['Adj Close'].rolling(window=moving_average_b).mean()

data = data.iloc[moving_average_b:]

buy_signals = []
sell_signals = []
trigger = -1
sold = 0
bought = 0
for i in range(len(data)):
    if data[f'Simple Moving Average -{moving_average_a} days'].iloc[i]\
            > data[f'Simple Moving Average -{moving_average_b} days'].iloc[i] and trigger != 1:
        buy_signals.append(data['Adj Close'].iloc[i])
        print(data['Adj Close'].iloc[i])
        bought += data['Adj Close'].iloc[i]
        sell_signals.append(float('nan'))
        trigger = 1
    elif data[f'Simple Moving Average -{moving_average_a} days'].iloc[i]\
            < data[f'Simple Moving Average -{moving_average_b} days'].iloc[i] and trigger != -1:
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[i])
        print(data['Adj Close'].iloc[i])
        sold += data['Adj Close'].iloc[i]
        trigger = -1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))
if(trigger == 1):
    buy_signals.append(float('nan'))
    sell_signals.append(data['Adj Close'].iloc[-1])
    print(data['Adj Close'].iloc[-1])
    sold += data['Adj Close'].iloc[-1]
    trigger = -1

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

print(data)
shares_invested = 100
print("Number of Shares:", shares_invested)
print("Initial Balance:", (bought * shares_invested))
print("End Balance:", (sold * shares_invested))


def rate_of_return(total_sold, total_bought):
    return "{:.1%}".format(((total_sold - total_bought) / total_bought))


print("Profit:", ((sold - bought) * shares_invested))
print("Return: " + rate_of_return(sold, bought))

plt.plot(data['Adj Close'], label=stock + " PRICE", alpha=0.5)
plt.plot(data[f'Simple Moving Average -{moving_average_a} days'],
         label=f"Simple Moving Average -{moving_average_a} days", color="blue", linestyle='--')
plt.plot(data[f'Simple Moving Average -{moving_average_b} days'],
         label=f"Simple Moving Average -{moving_average_b} days", color="purple", linestyle='--')
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=2)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=2)
plt.legend(loc="upper left")
plt.show()
