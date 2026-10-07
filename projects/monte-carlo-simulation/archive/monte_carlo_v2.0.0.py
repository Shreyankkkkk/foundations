import random
import matplotlib
import statistics 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import deque, Counter
import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde
import mysql.connector as sql
import os

print()
start_time = datetime.now()
print(start_time)
print()

a=int(input("Enter Password : "))
conn = sql.connect(
    host='localhost',
    user='root',
    passwd=str(a),
    database='monte_carlo'

)
cursor = conn.cursor()
if conn.is_connected(): print("Connected: ")

# -------------------- Start of Monte Carlo Simulation --------------------
print('\n--------------------Monte Carlo Simulation--------------------\n')


# -------------------- NEW: Choose New Run or Reproduce --------------------
mode = input("Press: (1) for New Run / (2) to Reproduce Previous Run: ")

if mode == '1':
    # Generate new seed
    seed = random.randint(1, 1000000)
    print("Generated new seed:", seed)

    # -------------------- Input: Number of Trades --------------------
    def random_number_of_trades():
        return random.randint(150, 624)

    while True:
        n = int(input("(1) Random Number of Trades per year \n(2) Enter a Number: \nPress 1 / 2 : "))
        if n == 1:
            trades = random_number_of_trades()
            print(f'Evaluating {trades} number of trades a year')
            break
        elif n == 2:
            trades = int(input("Number of Trades :"))
            break
        else:
            print("Wrong Input~")
            continue
    print()

    # -------------------- Risk --------------------------------------
    def risk():
        risk_level=[]
        try:
            n=int(input("Number of Risk : (like 2 = 1% and 0.5%) :"))
        except ValueError:
            print("Invalid Input L: Please enter whole number")
            return []
        for i in range(1,n+1):
            while True:
                try:
                    user_input = float(input(f'Input Risk {i} (%) :'))
                    if 0<=user_input<=100:
                        risk_level.append(user_input/100)
                        break
                    else:
                        print("Please enter a value between 0 and 100")
                except ValueError:
                    print("Invalid Input: Please enter a number.")
        return risk_level 


    
    # -------------------- Input: User Parameters --------------------
    runs = int(input("Number of Runs :"))
    n_people = int(input('Number of People :'))
    account_size = int(input("Account Size :"))
    win_ratee = int(input("Minimum Win Rate :"))
    lower_limit_rr = float(input("Minimum RR :"))
    upper_limit_rr = float(input("Maximum RR :"))
    commission_per_trade = float(input("Enter $ Commission per trade :"))
    print()

    while True:
        risk_levels=risk()
        if len(risk_levels)>=1:
            break
        else:
            print("Risk has to be entered :")
    while True:
        print("Range is 0-10, realistically it doesnt increase above that")
        win_rate_change = float(input("Changes in Win rate depending on the month :"))
        if 0 <= win_rate_change <= 10:
            break
        else:
            print()
            continue
        
    # Convert risk_levels list to string
    risk_levels_str = ','.join(str(r) for r in risk_levels)

    cursor.execute("""
INSERT INTO monte_carlo_runs
(seed, num_trades, account_size, min_win_rate, min_rr, max_rr, commission, win_rate_change, risk_levels, runs, n_people)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
      commission_per_trade, win_rate_change, risk_levels_str, runs, n_people))
    conn.commit()


elif mode == '2':
    # Reproduce previous run
    run_id = int(input("Enter the Run ID to reproduce: "))
    cursor.execute("SELECT * FROM monte_carlo_runs WHERE run_id = %s", (run_id,))
    result = cursor.fetchone()
    if result:
        (run_id, seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
         commission_per_trade, win_rate_change, risk_levels_str, runs, n_people, created_at) = result
        risk_levels = [float(r) for r in risk_levels_str.split(',') if r.strip()]
        print(f"Reproducing run with seed: {seed}")
    else:
        print("Run ID not found. Exiting.")
        exit()

    # Set seeds
    random.seed(seed)
    np.random.seed(seed)

print()

# -------------------- Lists to Store Metrics --------------------
final_account_balances = []
win_streaks = []
loss_streaks = []
all_equity_curves = []
time_under = []
max_drawdown = []
max_duration = []
sharpe_list = []
sortino_list = []
calmar_list = []
rr_distribution = []
all_metrics = []
returns_window = deque(maxlen=20)
regimes = deque(maxlen=2)

# -------------------- Helper Functions --------------------

# Split trades across months
def random_monthly_split(trades):
    array = np.array([0.8, 1.0, 1.2, 1.1, 1.3, 1.0, 0.9, 0.7, 1.1, 1.2, 0.9, 0.6])
    weigh = np.random.dirichlet(array, size=1)[0]
    monthly_trades = (weigh * trades).astype(int)
    while sum(monthly_trades) < trades:
        monthly_trades[random.randint(0, 11)] += 1
    while sum(monthly_trades) > trades:
        monthly_trades[random.randint(0, 11)] -= 1
    return monthly_trades.tolist()

# Split trades across weekdays
def split_trades_week(trades):
    array = np.array([0.7, 0.8, 1.3, 1.4, 1.2])
    weigh = np.random.dirichlet(array, size=1)[0]
    weekday_trades = (weigh * trades).astype(int)
    while sum(weekday_trades) < trades:
        weekday_trades[random.randint(0, 4)] += 1
    while sum(weekday_trades) > trades:
        weekday_trades[random.randint(0, 4)] -= 1
    return weekday_trades.tolist()

# News event that can affect risk/reward
def news_event():
    global count2
    if random.random() < 0.005:
        count2 += 1
        multiplier = np.random.lognormal(mean=0,sigma=0.3)
        return min(multiplier,3.0)
    return 1

# Random win rate adjustment by month
def month():
    return random.randint(1, 3)

# Random counter-trend adjustment
def counter():
    if random.random() < 0.10:
        return True

# Maximum drawdown from peak
def max_draw(equity_curve):
    peak = equity_curve[0]
    max_dd = 0.0
    for x in equity_curve:
        peak = max(peak, x)
        drawdown = (peak - x) / peak
        max_dd = max(max_dd, drawdown)
    return max_dd

# Sharpe Ratio
def sharpe_ratio(equity_curve):
    returns = np.diff(equity_curve) / equity_curve[:-1]
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    if std_return == 0:
        return 0
    return mean_return / std_return

# Sortino Ratio
def sortino_ratio(equity_curve):
    returns = np.diff(equity_curve) / equity_curve[:-1]
    downside_returns = returns[returns < 0]
    downside_std = np.std(downside_returns)
    if downside_std == 0:
        return 0
    mean_return = np.mean(returns)
    return mean_return / downside_std

# Calmar Ratio
def calmar_ratio(equity_curve):
    total_return = (equity_curve[-1] / equity_curve[0]) - 1
    max_dd = max_draw(equity_curve)
    if max_dd == 0:
        return float('inf')
    return total_return / max_dd

# Drawdown duration (trades to recover)
def drawdown_duration(equity_curve):
    peak = equity_curve[0]
    durations = []
    in_drawdown = False
    start_index = 0
    for i, x in enumerate(equity_curve):
        if x < peak:
            if not in_drawdown:
                in_drawdown = True
                start_index = 1
        else:
            if in_drawdown:
                durations.append(i - start_index)
                in_drawdown = False
    if in_drawdown:
        durations.append(len(equity_curve) - start_index)
    return durations

# Time under water
def time_under_water(equity_curve):
    peak = equity_curve[0]
    tuw = 0
    current = 0
    for x in equity_curve:
        if x < peak:
            current += 1
            tuw = max(tuw, current)
        else:
            peak = x
            current = 0
    return tuw

# Higher Time Frame alignment
def htf_align():
    n = random.randint(1, 5)
    if n <= 3:
        return True
    elif n > 3:
        return False

# Sweep check
def sweep():
    n = random.randint(1, 5)
    if n < 3:
        return True
    elif n >= 3:
        return False

# Generate random Risk:Reward ratio
def risk_to_reward():
    b=8
    exponent = np.exp(-0.2*((upper_limit_rr - lower_limit_rr) - 1))
    a=max(0.1, 2*exponent)
    return lower_limit_rr + (upper_limit_rr - lower_limit_rr)*np.random.beta(a,b)

# -------------------- Core Simulation Function --------------------
def run_single_simulation(account_size, number_of_trades):
    global total_profit, total_loss, count3
    wX = []
    vY = []

    risk_index = 0
    trade_number = 1

    current_win_streak = 0
    current_loss_streak = 0
    longest_win_streak = 0
    longest_loss_streak = 0
    wins_losses = []

    reg = ['bull','bear','neutral']

    for month_trades in random_monthly_split(trades):
        regimes.append(random.choice(reg))
        new_win_rate = win_ratee
        
        n1 = month()
        if n1 == 1:
            new_win_rate -= win_rate_change
        elif n1 == 2:
            new_win_rate += win_rate_change
        if counter():
            new_win_rate -= win_rate_change

        if len(regimes) == 2:
            if regimes[1]=='neutral':
                momentum_bonus = 0
            elif regimes[0] == regimes[1]:
                momentum_bonus = 2
            elif regimes[0]=='neutral':
                momentum_bonus = 1
            else:
                momentum_bonus = -2
        elif len(regimes) == 1:
            momentum_bonus = 0
        new_win_rate += momentum_bonus
            

        week_block = split_trades_week(month_trades)
        weekdays = ['Mon','Tue','Wed','Thu','Fri']

        for day_index, n_trades in enumerate(week_block):

            for j in range(n_trades):
                htf = htf_align()
                swp = sweep()
                n5 = risk_to_reward()

                if htf and swp:
                    n5 += 0.75
                elif htf or swp:
                    n5 += 0.5

                risk = account_size * risk_levels[risk_index]
                n4 = random.randint(1, 100)

                if htf and swp:
                    n4 += 10
                elif htf or swp:
                    n4 += 5

                #current win streak increase confidence, higher chance of winnning
                if current_loss_streak == 0 and current_win_streak >=3:
                    n4 += min(current_win_streak, 10)
                elif current_win_streak == 0 and current_loss_streak >=3:
                    n4 -= min(current_loss_streak, 10)
                
                #overconfidence penalty and fatigue penalty
                if current_win_streak >= 9:
                    n4 -= 2
                elif current_loss_streak >= 9:
                    n4 -= 4

                #random psychological events
                if random.random() < 0.02 and current_loss_streak >= 5:
                    n4 -= random.randint(1,10)

                #memory of recent trades
                if len(wins_losses) >= 10:
                    recent_results = wins_losses[-10:]
                    confidence = recent_results.count(True) - recent_results.count(False)
                    n4 += confidence

                #capping the win rate
                if n4 >= 96:
                    n4 = 95

                if n4 < new_win_rate:
                    win = True
                else:
                    win = False

                # Calculate volatility for slippage
                if len(returns_window) > 2:
                    vol = statistics.pstdev(returns_window)
                else:
                    vol = 0.01

                base_slippage = 0.002
                k = 0.15
                slippage_fraction = base_slippage + k * vol
                slippage_pct = random.uniform(1 - slippage_fraction, 1 + slippage_fraction)
                slip = random.randint(1, 2)

                rr_distribution.append(n5)

                # News impact
                if day_index in [2, 3]:
                    news_multipler = news_event()
                    if news_multipler != 1:
                        if random.random() < 0.5:
                            count3 += 1
                            win = not win
                    n5 *= news_multipler

                # -------------------- Trade Execution --------------------
                if win:
                    profit = (n5 * risk)
                    
                    max_profit = 0.15 * account_size
                    profit = min(profit,max_profit)
                    
                    n = profit / account_size
                    returns_window.append(n)
                    if slip == 1:
                        profit *= slippage_pct
                    if random.random() < 0.05:
                        profit *= random.uniform(0.75, 0.90)

                    account_size += profit
                    total_profit += profit
                    account_size -= commission_per_trade

                    current_win_streak += 1
                    current_loss_streak = 0
                    risk_index = 0
                    if current_win_streak > longest_win_streak:
                        longest_win_streak = current_win_streak
                    wins_losses.append(True)

                else:
                    loss = risk
                    n = (-loss) / account_size
                    returns_window.append(n)
                    if slip == 1:
                        loss *= slippage_pct
                    if random.random() < 0.05:
                        loss *= random.uniform(0.75, 0.90)

                    account_size -= loss
                    total_loss += loss
                    account_size -= commission_per_trade

                    current_loss_streak += 1
                    current_win_streak = 0
                    if risk_index < len(risk_levels) - 1:
                        risk_index += 1
                    if current_loss_streak > longest_loss_streak:
                        longest_loss_streak = current_loss_streak
                    wins_losses.append(False)

                wX.append(trade_number)
                vY.append(account_size)
                trade_number += 1

    all_equity_curves.append(vY.copy())
    final_account_balances.append(account_size)

    tuw = time_under_water(vY)
    time_under.append(tuw)

    max_d = max_draw(vY)
    max_drawdown.append(max_d)

    duration = drawdown_duration(vY)
    max_duration.extend(duration)

    plt.plot(wX, vY, alpha=0.3)
    return longest_win_streak, longest_loss_streak
plt.show()

# -------------------- Run Simulation --------------------
count1 = 0
count2 = 0
count3 = 0
total_profit = 0
total_loss = 0

while count1 < runs:
    count = 1
    while count <= n_people:
        longest_win, longest_loss = run_single_simulation(account_size, trades)
        win_streaks.append(longest_win)
        loss_streaks.append(longest_loss)
        count += 1
    count1 += 1
print()

# -------------------- Metrics Calculation --------------------
# Calculate Value at Risk (VaR), Expected Shortfall, and Probability of Ruin
total_returns, worst_returns = [], []
for curve in all_equity_curves:
    pct_return = (curve[-1] / curve[0]) - 1
    total_returns.append(pct_return)

var_5 = np.percentile(total_returns, 5)

for r in total_returns:
    if r <= var_5:
        worst_returns.append(r)

expected_shortfall = sum(worst_returns)

ruin_count = 0
for curve in all_equity_curves:
    if curve[-1] < 0.5 * account_size:
        ruin_count += 1

probablity_ruin = ruin_count / len(all_equity_curves)

# -------------------- Print Risk Metrics --------------------
print(f"5% VaR: {round(var_5,4)}")
print(f"Expected Shortfall: {round(expected_shortfall,4)}")
print(f"Probability of Ruin (<50% account): {round(probablity_ruin*100,2)}%")
print()

# -------------------- Percentile Curves for Equity --------------------
equity_array = np.array(all_equity_curves)
p5_curve = np.percentile(equity_array, 5, axis=0)
p50_curve = np.percentile(equity_array, 50, axis=0)
p95_curve = np.percentile(equity_array, 95, axis=0)
p100_curve = np.percentile(equity_array, 100, axis=0)
p0_curve = np.percentile(equity_array, 0, axis=0)

# -------------------- Plot Monte Carlo Equity Curves --------------------
plt.figure(figsize=(12,7))

# Plot individual equity curves with low opacity
for curve in all_equity_curves:
    plt.plot(curve, color='black', alpha=0.1)

# Plot percentile curves
plt.plot(p50_curve, color='green', label='Median (P50)')
plt.plot(p5_curve, color='red', linestyle='--', label='5th Percentile (P5)')
plt.plot(p95_curve, color='red', linestyle='--', label='95th Percentile (P95)')

# Fill areas between percentiles
plt.fill_between(range(trades), p5_curve, p95_curve, color='green', alpha=0.5, label='5th - 95th')
plt.fill_between(range(trades), p0_curve, p5_curve, color='red', alpha=0.5, label='0th - 5th')
plt.fill_between(range(trades), p95_curve, p100_curve, color='red', alpha=0.5, label='95th - 100th')

# -------------------- Print Summary Metrics --------------------
final_p5 = p5_curve[-1]
final_p95 = p95_curve[-1]

print("Maximum :", max(final_account_balances))
print("Final 95th Percentile", final_p95)
print("Average :", (sum(final_account_balances)/len(final_account_balances)))
print("Final 5th Percentile", final_p5)
print("Minimum :", min(final_account_balances))
print()

# Win/Loss streaks
print("Average Longest Win Streak :", sum(win_streaks)/len(win_streaks))
print("Average Longest Loss Streak :", sum(loss_streaks)/len(loss_streaks))
print()

# Drawdowns
avg_max_dd = sum(max_drawdown)/len(max_drawdown) * 100
worst_max_dd = max(max_drawdown) * 100
print("Average Max Drawdown :", str(round(avg_max_dd)) + '%')
print("Worst Max Drawdown :", str(round(worst_max_dd)) + '%')
print()

# Drawdown duration
avg_max_duration = sum(max_duration)/len(max_duration)
worst_max_duration = max(max_duration)
print("Average Drawdown Duration Trades :", round(avg_max_duration, 2))
print("Worst Drawdown Duration Trades :", worst_max_duration)
print()

# Time under water
tuws = sum(time_under)/len(time_under)
print("Average Time under Water (Trades) :", tuws)
print()

# Global Profit Factor
if total_loss > 0:
    profit_factor = total_profit / total_loss
else:
    profit_factor = float('inf')
print("Global Profit Factor :", profit_factor)
print()

# Average return per trade
avg_return = (sum(final_account_balances)/len(final_account_balances) - account_size)/trades
avg_return_percent = (avg_return / account_size) * 100
print("Average Return per Trade (Absolute) :", round(avg_return, 2))
print("Average Return per Trade (%) :", str(round(avg_return_percent, 4)) + '%')
print()

# -------------------- Performance Ratios --------------------
for curve in all_equity_curves:
    sharpe_list.append(sharpe_ratio(curve))
    sortino_list.append(sortino_ratio(curve))
    calmar_list.append(calmar_ratio(curve))

print("Average Sharpe Ratio :", round(np.mean(sharpe_list), 3))
print("Average Sortino Ratio :", round(np.mean(sortino_list), 3))
print("Average Calmar Ratio :", round(np.mean(calmar_list), 3))
print()

# -------------------- Trades & Commission Summary --------------------
end_no_trades = (trades * n_people)
print('Total number of trades per run :', end_no_trades)
print('Total number of trades :', (end_no_trades * runs))
print(f'Total capital lost due to commission : {end_no_trades * runs * commission_per_trade}')
print()

# News trades
print("Total Number of Trades taken on News :", count2)
print("News Trades that were flipped from a win :", count3)
print("News Trades that weren't flipped :", count2 - count3)

# -------------------- End Time --------------------
end_time = datetime.now()
print(end_time)

# -------------------- Risk:Reward Distribution Plot --------------------
counter = Counter(rr_distribution)
most_common_rr = counter.most_common(1)
for rr_val, count in most_common_rr:
    plt.text(rr_val- 0.1, 1.90, f'Most Common RR: {round(rr_val, 2)}', horizontalalignment='center', color='black',
             fontsize=8)

# Convert RR distribution to numpy array
rr_distribution = np.array(rr_distribution).flatten()
mean_rr = np.mean(rr_distribution)
r0_curve = np.percentile(rr_distribution, 0)
r5_curve = np.percentile(rr_distribution, 5)
r95_curve = np.percentile(rr_distribution, 95)
r100_curve = np.percentile(rr_distribution, 100)

plt.figure(figsize=(12,6))
kde = gaussian_kde(rr_distribution)
x_val = np.linspace(rr_distribution.min(), rr_distribution.max(), 1000)
y_val = kde(x_val)

plt.plot(x_val, y_val, color='black', label = "RR Distribution")

# Mask for percentile regions
mask1 = (x_val >= r0_curve) & (x_val <= r5_curve)
mask2 = (x_val >= r5_curve) & (x_val <= r95_curve)
mask3 = (x_val >= r95_curve) & (x_val <= r100_curve)

plt.fill_between(x_val[mask1], y_val[mask1], alpha=0.3, color='red')
plt.fill_between(x_val[mask2], y_val[mask2], alpha=0.3, color='green')
plt.fill_between(x_val[mask3], y_val[mask3], alpha=0.3, color='red')

plt.xlabel("Risk:Reward Ratio")
plt.ylabel("Distribution")
plt.title("RRR Distribution")
plt.legend()
plt.grid(True)
plt.show()


'''
(1) - 250,000, 63, 2, 5, [1,0.5], 5
(2) - 2,500,000, 63, 2, 5, [1,0.5],5
(3) - 75,000
'''
