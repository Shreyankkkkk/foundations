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
from numba import jit

print()
start_time = datetime.now()
print(start_time)
print()

L_GREEN = '\033[92m'
GREEN = '\033[32m'
RED = '\033[91m'
L_RED = '\033[31m'
YELLOW = '\033[93m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
ENDC = '\033[0m'

a = int(input(f"{PURPLE}Enter Password : {ENDC}"))
conn = sql.connect(
    host='localhost',
    user='root',
    passwd=str(a),
    database='monte_carlo'
)
cursor = conn.cursor()
if conn.is_connected(): 
    print(f"{GREEN}Connected: {ENDC}")

print(f'\n{PURPLE}--------------------Monte Carlo Simulation--------------------{ENDC}\n')

# Choose New Run or Reproduce
mode = input(f"{CYAN}Press: (1) for New Run / (2) to Reproduce Previous Run: {ENDC} ")

if mode == '1':
    seed = random.randint(1, 1000000)
    print(f"{YELLOW}Generated new seed: {seed}{ENDC}")

    def random_number_of_trades():
        return random.randint(150, 624)

    while True:
        n = int(input(f"{CYAN}(1) Random Number of Trades per year \n(2) Enter a Number: \nPress 1 / 2 : {ENDC}"))
        if n == 1:
            trades = random_number_of_trades()
            print(f'{YELLOW}Evaluating {trades} number of trades a year{ENDC}')
            break
        elif n == 2:
            trades = int(input(f"{CYAN}Number of Trades :{ENDC}"))
            break
        else:
            print(f"{RED}Wrong Input~{ENDC}")
            continue
    print()

    def risk():
        risk_level = []
        try:
            n = int(input(f"{CYAN}Number of Risk : (like 2 = 1% and 0.5%) :{ENDC}"))
        except ValueError:
            print(f"{RED}Invalid Input: Please enter whole number{ENDC}")
            return []
        for i in range(1, n + 1):
            while True:
                try:
                    user_input = float(input(f'{CYAN}Input Risk {i} (%) :{ENDC}'))
                    if 0 <= user_input <= 100:
                        risk_level.append(user_input / 100)
                        break
                    else:
                        print(f"{RED}Please enter a value between 0 and 100{ENDC}")
                except ValueError:
                    print(f"{RED}Invalid Input: Please enter a number.{ENDC}")
        return risk_level 
    
    runs = int(input(f"{CYAN}Number of Runs :{ENDC}"))
    n_people = int(input(f'{CYAN}Number of People :{ENDC}'))
    account_size = int(input(f"{CYAN}Account Size :{ENDC}"))
    win_ratee = float(input(f"{CYAN}Minimum Win Rate :{ENDC}"))
    lower_limit_rr = float(input(f"{CYAN}Minimum RR :{ENDC}"))
    upper_limit_rr = float(input(f"{CYAN}Maximum RR :{ENDC}"))
    commission_per_trade = float(input(f"{CYAN}Enter $ Commission per trade :{ENDC}"))
    break_even_per_cent = float(input(f"{CYAN}Enter Break Even Percentage :{ENDC}"))
    print()

    while True:
        risk_levels = risk()
        if len(risk_levels) >= 1:
            break
        else:
            print(f"{RED}Risk has to be entered :{ENDC}")

    while True:
        print(f"{YELLOW}\nRange is 0-10, realistically it doesnt increase above that{ENDC}")
        win_rate_change = float(input(f"{CYAN}Changes in Win rate depending on the month :{ENDC}"))
        if 0 <= win_rate_change <= 10:
            break
        
    risk_levels_str = ','.join(str(r) for r in risk_levels)

    cursor.execute("""
INSERT INTO monte_carlo_runs
(seed, num_trades, account_size, min_win_rate, min_rr, max_rr, commission, win_rate_change, risk_levels, runs, n_people)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
      commission_per_trade, win_rate_change, risk_levels_str, runs, n_people))
    conn.commit()

elif mode == '2':
    run_id = int(input(f"{CYAN}Enter the Run ID to reproduce: {ENDC}"))
    cursor.execute("SELECT * FROM monte_carlo_runs WHERE run_id = %s", (run_id,))
    result = cursor.fetchone()
    if result:
        (run_id, seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
         commission_per_trade, win_rate_change, risk_levels_str, runs, n_people, created_at) = result
        risk_levels = [float(r) for r in risk_levels_str.split(',') if r.strip()]
        print(f"{YELLOW}Reproducing run with seed: {seed}{ENDC}")
        break_even_per_cent = float(input(f"{CYAN}Enter Break Even Percentage :{ENDC}"))
    else:
        print(f"{RED}Run ID not found. Exiting.{ENDC}")
        exit()
else:
    print(f"{RED}Invalid mode selection. Exiting.{ENDC}")
    exit()

# Set seeds for reproducibility
random.seed(seed)
np.random.seed(seed)
print()

# Account type selection
while True:
    account_type = int(input(f"{CYAN}Run for (1) Live Account / (2) Prop firm Trading : {ENDC}"))
    if account_type in [1, 2]:
        if account_type == 1:
            target_goal = float(input(f"{CYAN}Enter Target Goal :{ENDC}")) 
            not_accepted_max_dd = None
        elif account_type == 2:
            print(f"{YELLOW}Prop Firm Trading selected. Enter Rules{ENDC}")
            not_accepted_max_dd = float(input(f"{CYAN}Maximum Drawdown allowed :{ENDC}"))
            target_goal = None
        break
    else:
        print(f"{RED}Invalid input. Please enter 1 or 2.{ENDC}")

# Convert risk_levels to numpy array
risk_levels_np = np.array(risk_levels)

# Vectorized Helper Functions
@jit(nopython=True)
def generate_monthly_split(trades):
    """Vectorized monthly trade distribution"""
    array = np.array([0.8, 1.0, 1.2, 1.1, 1.3, 1.0, 0.9, 0.7, 1.1, 1.2, 0.9, 0.6])
    # Simple normalization instead of Dirichlet for JIT compatibility
    weights = array / array.sum()
    monthly_trades = (weights * trades).astype(np.int32)
    
    # Adjust for rounding
    diff = trades - monthly_trades.sum()
    if diff > 0:
        for i in range(diff):
            monthly_trades[np.random.randint(0, 12)] += 1
    elif diff < 0:
        for i in range(-diff):
            idx = np.random.randint(0, 12)
            if monthly_trades[idx] > 0:
                monthly_trades[idx] -= 1
    return monthly_trades

@jit(nopython=True)
def generate_weekly_split(trades):
    """Vectorized weekly trade distribution"""
    array = np.array([0.7, 0.8, 1.3, 1.4, 1.2])
    weights = array / array.sum()
    weekday_trades = (weights * trades).astype(np.int32)
    
    diff = trades - weekday_trades.sum()
    if diff > 0:
        for i in range(diff):
            weekday_trades[np.random.randint(0, 5)] += 1
    elif diff < 0:
        for i in range(-diff):
            idx = np.random.randint(0, 5)
            if weekday_trades[idx] > 0:
                weekday_trades[idx] -= 1
    return weekday_trades

@jit(nopython=True)
def calculate_max_drawdown(equity_curve):
    """Numba-compatible max drawdown calculation"""
    if len(equity_curve) == 0:
        return 0.0
    
    peak = equity_curve[0]
    max_dd = 0.0
    
    for value in equity_curve:
        if value > peak:
            peak = value
        if peak > 0:
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
    
    return max_dd

@jit(nopython=True)
def calculate_time_under_water(equity_curve):
    """Numba-compatible time under water calculation"""
    if len(equity_curve) == 0:
        return 0
    
    peak = equity_curve[0]
    max_consecutive = 0
    current_consecutive = 0
    
    for value in equity_curve:
        if value < peak:
            current_consecutive += 1
            if current_consecutive > max_consecutive:
                max_consecutive = current_consecutive
        else:
            peak = value
            current_consecutive = 0
    
    return max_consecutive

@jit(nopython=True)
def calculate_sharpe_ratio(equity_curve):
    """Vectorized Sharpe ratio"""
    if len(equity_curve) < 2:
        return 0.0
    
    returns = np.diff(equity_curve) / equity_curve[:-1]
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    
    if std_return == 0:
        return 0.0
    return mean_return / std_return

@jit(nopython=True)
def calculate_sortino_ratio(equity_curve):
    """Vectorized Sortino ratio"""
    if len(equity_curve) < 2:
        return 0.0
    
    returns = np.diff(equity_curve) / equity_curve[:-1]
    downside_returns = returns[returns < 0]
    
    if len(downside_returns) == 0:
        return 0.0
    
    downside_std = np.std(downside_returns)
    if downside_std == 0:
        return 0.0
    
    mean_return = np.mean(returns)
    return mean_return / downside_std

@jit(nopython=True)
def generate_rr_ratios(n, lower_limit, upper_limit):
    """Vectorized RR generation"""
    b = 8
    exponent = np.exp(-0.2 * ((upper_limit - lower_limit) - 1))
    a = max(0.1, 2 * exponent)
    
    beta_samples = np.random.beta(a, b, n)
    return (1 + lower_limit) + (upper_limit - lower_limit) * beta_samples

@jit(nopython=True)
def vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, 
                                lower_rr, upper_rr, commission, be_percent, 
                                max_dd_threshold, is_prop_firm):
    """Core vectorized simulation loop"""
    
    # Pre-allocate arrays
    equity_curve = np.zeros(n_trades + 1)
    equity_curve[0] = account_size
    
    current_account = account_size
    risk_index = 0
    
    # Streak tracking
    current_win_streak = 0
    current_loss_streak = 0
    longest_win_streak = 0
    longest_loss_streak = 0
    current_be_streak = 0
    longest_be_streak = 0
    
    # Generate all random numbers at once
    win_rolls = np.random.randint(1, 101, n_trades)
    htf_rolls = np.random.randint(1, 6, n_trades)
    sweep_rolls = np.random.randint(1, 6, n_trades)
    rr_ratios = generate_rr_ratios(n_trades, lower_rr, upper_rr)
    slippage = np.random.uniform(0.996, 1.004, n_trades)
    be_rolls = np.random.randint(1, 101, n_trades)
    t_dist_samples = np.random.standard_t(3, n_trades)
    slip_apply = np.random.randint(1, 3, n_trades)
    additional_slip = np.random.uniform(0.75, 0.90, n_trades)
    apply_additional = np.random.random(n_trades) < 0.05
    
    # Counters
    wins = 0
    losses = 0
    be_count = 0
    
    recent_wins = np.zeros(10, dtype=np.int32)
    recent_idx = 0
    
    stop_simulation = False
    actual_trades = 0
    
    for i in range(n_trades):
        if stop_simulation:
            break
            
        # HTF and Sweep checks
        htf = htf_rolls[i] <= 3
        swp = sweep_rolls[i] < 3
        
        # Adjust RR
        rr = rr_ratios[i]
        if htf and swp:
            rr += 0.75
        elif htf or swp:
            rr += 0.5
        
        # Calculate risk
        risk = current_account * risk_levels[risk_index]
        
        # Base win probability
        win_prob = win_rate_base
        
        # Adjust for HTF/Sweep
        if htf and swp:
            win_prob += 10
        elif htf or swp:
            win_prob += 5
        
        # Streak adjustments
        if current_loss_streak == 0 and current_win_streak >= 3:
            win_prob += min(current_win_streak, 10)
        elif current_win_streak == 0 and current_loss_streak >= 3:
            win_prob -= min(current_loss_streak, 10)
        
        # Overconfidence penalty
        if current_win_streak >= 9:
            win_prob -= 2
        elif current_loss_streak >= 9:
            win_prob -= 2
        
        # Memory effect
        if recent_idx >= 10:
            confidence = np.sum(recent_wins) - (10 - np.sum(recent_wins))
            win_prob += confidence
        
        # Cap win rate
        win_prob = min(win_prob, 95)
        
        # Break even check
        if be_rolls[i] <= be_percent:
            be_count += 1
            current_be_streak += 1
            longest_be_streak = max(longest_be_streak, current_be_streak)
            actual_trades += 1
            equity_curve[actual_trades] = current_account
            continue
        
        # Determine win/loss
        is_win = win_rolls[i] < win_prob
        
        if is_win:
            # Win trade
            profit = abs(t_dist_samples[i] * rr * risk)
            max_profit = 0.15 * current_account
            profit = min(profit, max_profit)
            
            if slip_apply[i] == 1:
                profit *= slippage[i]
            if apply_additional[i]:
                profit *= additional_slip[i]
            
            current_account += profit
            current_account -= commission
            
            wins += 1
            current_win_streak += 1
            current_loss_streak = 0
            current_be_streak = 0
            longest_win_streak = max(longest_win_streak, current_win_streak)
            
            risk_index = 0
            
            # Update memory
            if recent_idx < 10:
                recent_wins[recent_idx] = 1
            else:
                recent_wins = np.roll(recent_wins, -1)
                recent_wins[-1] = 1
            recent_idx += 1
            
        else:
            # Loss trade
            loss = abs(t_dist_samples[i] * risk)
            max_loss = 0.05 * current_account
            loss = min(loss, max_loss)
            
            if slip_apply[i] == 1:
                loss *= slippage[i]
            if apply_additional[i]:
                loss *= additional_slip[i]
            
            current_account -= loss
            current_account -= commission
            
            losses += 1
            current_loss_streak += 1
            current_win_streak = 0
            current_be_streak = 0
            longest_loss_streak = max(longest_loss_streak, current_loss_streak)
            
            risk_index = min(risk_index + 1, len(risk_levels) - 1)
            
            # Update memory
            if recent_idx < 10:
                recent_wins[recent_idx] = 0
            else:
                recent_wins = np.roll(recent_wins, -1)
                recent_wins[-1] = 0
            recent_idx += 1
        
        actual_trades += 1
        equity_curve[actual_trades] = current_account
        
        # Prop firm check
        if is_prop_firm and max_dd_threshold > 0:
            if actual_trades > 0:
                peak = np.max(equity_curve[:actual_trades+1])
                if peak > 0:
                    dd = (peak - current_account) / peak
                    if dd >= max_dd_threshold:
                        stop_simulation = True
    
    return (equity_curve[:actual_trades+1], wins, losses, be_count, 
            longest_win_streak, longest_loss_streak, longest_be_streak, stop_simulation)

# Run batched simulations
print(f"{YELLOW}Running vectorized simulation...{ENDC}\n")

total_simulations = runs * n_people
all_results = []

# Pre-generate regime changes for all simulations
regime_choices = np.random.choice([0, 1, 2], size=(total_simulations, 12))  # 0=bull, 1=bear, 2=neutral

for sim_idx in range(total_simulations):
    # Calculate win rate adjustments based on regime
    base_win_rate = win_ratee
    month_mod = np.random.randint(1, 4)
    if month_mod == 1:
        base_win_rate -= win_rate_change
    elif month_mod == 2:
        base_win_rate += win_rate_change
    
    if np.random.random() < 0.10:
        base_win_rate -= win_rate_change
    
    # Run simulation
    is_prop = 1 if account_type == 2 else 0
    dd_threshold = (not_accepted_max_dd / 100) if not_accepted_max_dd else 0
    
    result = vectorized_trade_simulation(
        trades, account_size, risk_levels_np, base_win_rate,
        lower_limit_rr, upper_limit_rr, commission_per_trade,
        break_even_per_cent, dd_threshold, is_prop
    )
    
    all_results.append(result)
    
    if (sim_idx + 1) % 100 == 0:
        print(f"Completed {sim_idx + 1}/{total_simulations} simulations")

print(f"{GREEN}Simulation complete!{ENDC}\n")

# Extract results
all_equity_curves = []
win_streaks = []
loss_streaks = []
be_streaks = []
final_account_balances = []
no_of_win = 0
no_of_loss = 0
be_count = 0
prop_lost = 0

for equity, wins, losses, be, win_str, loss_str, be_str, failed in all_results:
    all_equity_curves.append(equity)
    win_streaks.append(win_str)
    loss_streaks.append(loss_str)
    be_streaks.append(be_str)
    final_account_balances.append(equity[-1])
    no_of_win += wins
    no_of_loss += losses
    be_count += be
    if failed:
        prop_lost += 1

executed_trades = no_of_win + no_of_loss + be_count

# Vectorized metrics calculation
all_equity_array = np.array([np.pad(curve, (0, trades + 1 - len(curve)), constant_values=np.nan) 
                             for curve in all_equity_curves])

# Calculate metrics using vectorization
max_drawdowns = np.array([calculate_max_drawdown(curve) for curve in all_equity_curves])
time_unders = np.array([calculate_time_under_water(curve) for curve in all_equity_curves])
sharpe_ratios = np.array([calculate_sharpe_ratio(curve) for curve in all_equity_curves])
sortino_ratios = np.array([calculate_sortino_ratio(curve) for curve in all_equity_curves])

# Calculate percentiles
final_balances_array = np.array(final_account_balances)
p0_curve = np.nanpercentile(all_equity_array, 0, axis=0)
p5_curve = np.nanpercentile(all_equity_array, 5, axis=0)
p50_curve = np.nanpercentile(all_equity_array, 50, axis=0)
p95_curve = np.nanpercentile(all_equity_array, 95, axis=0)
p100_curve = np.nanpercentile(all_equity_array, 100, axis=0)

# Risk metrics
total_returns = (final_balances_array / account_size) - 1
var_5 = np.percentile(total_returns, 5)
expected_shortfall = np.mean(total_returns[total_returns <= var_5])
probability_ruin = np.sum(final_balances_array < 0.5 * account_size) / len(final_balances_array)

# Print Risk Metrics
print(f"{PURPLE}5% VaR:{ENDC} {RED}{round(var_5, 4)}{ENDC}")
print(f"{PURPLE}Expected Shortfall:{ENDC} {RED}{round(expected_shortfall, 4)}{ENDC}")
print(f"{PURPLE}Probability of Ruin (<50% account):{ENDC} {RED}{round(probability_ruin * 100, 2)}%{ENDC}")
print()

# Plot
plt.style.use('dark_background')
plt.figure(figsize=(12, 7))

for curve in all_equity_curves[::10]:  # Plot every 10th for performance
    plt.plot(curve, color='white', alpha=0.1)

x_range = range(len(p50_curve))
plt.plot(p50_curve, color='green', label='Median (P50)', linewidth=2)
plt.plot(p5_curve, color='red', linestyle='--', label='5th Percentile (P5)', linewidth=2)
plt.plot(p95_curve, color='red', linestyle='--', label='95th Percentile (P95)', linewidth=2)

plt.fill_between(x_range, p5_curve, p95_curve, color='gray', alpha=0.18, label='5th - 95th')
plt.fill_between(x_range, p0_curve, p5_curve, color='gray', alpha=0.18, label='0th - 5th')
plt.fill_between(x_range, p95_curve, p100_curve, color='turquoise', alpha=0.18, label='95th - 100th')

plt.xlabel('Trade Number')
plt.ylabel('Account Balance')
plt.title('Monte Carlo Equity Curves (Vectorized)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Print Summary Metrics
final_p5 = p5_curve[np.where(~np.isnan(p5_curve))[0][-1]]
final_p95 = p95_curve[np.where(~np.isnan(p95_curve))[0][-1]]

print(f"{GREEN}Maximum :{ENDC} {GREEN}{np.max(final_balances_array):.2f}{ENDC}")
print(f"{L_GREEN}Final 95th Percentile:{ENDC} {L_GREEN}{final_p95:.2f}{ENDC}")
print(f"{YELLOW}Average :{ENDC} {GREEN}{np.mean(final_balances_array):.2f}{ENDC}")
print(f"{L_RED}Final 5th Percentile:{ENDC} {L_RED}{final_p5:.2f}{ENDC}")
print(f"{RED}Minimum :{ENDC} {RED}{np.min(final_balances_array):.2f}{ENDC}")
print()

print(f"{GREEN}Average Longest Win Streak :{ENDC} {L_GREEN}{np.mean(win_streaks):.2f}{ENDC}")
print(f'{CYAN}Average Break Even Streak :{ENDC} {YELLOW}{np.mean(be_streaks):.2f}{ENDC}')
print(f"{RED}Average Longest Loss Streak :{ENDC} {L_RED}{np.mean(loss_streaks):.2f}{ENDC}")
print()

avg_max_dd = np.mean(max_drawdowns) * 100
worst_max_dd = np.max(max_drawdowns) * 100
print(f"{L_GREEN}Average Max Drawdown :{ENDC} {L_RED}{round(avg_max_dd)}%{ENDC}")
print(f"{GREEN}Worst Max Drawdown :{ENDC} {RED}{round(worst_max_dd)}%{ENDC}")
print()

print(f"{CYAN}Average Time under Water (Trades) :{ENDC} {YELLOW}{np.mean(time_unders):.2f}{ENDC}")
print()

print(f"{PURPLE}Average Sharpe Ratio :{ENDC} {GREEN}{np.mean(sharpe_ratios):.3f}{ENDC}")
print(f"{PURPLE}Average Sortino Ratio :{ENDC} {GREEN}{np.mean(sortino_ratios):.3f}{ENDC}")
print()

end_no_trades = trades * n_people
print(f'{PURPLE}Total number of trades per run :{ENDC} {end_no_trades}')
print(f'{PURPLE}Total number of trades :{ENDC} {end_no_trades * runs}')
print(f'{PURPLE}Total number of trades won :{ENDC} {no_of_win}')
print(f'{PURPLE}Total number of trades that hit BE :{ENDC} {be_count}')
print(f'{PURPLE}Total number of trades lost :{ENDC} {no_of_loss}\n')

if executed_trades > 0:
    win_rate_actual = (no_of_win / executed_trades) * 100
    if win_rate_actual < win_ratee:
        print(f'{PURPLE}Win rate:{ENDC} {L_RED}{win_rate_actual:.2f}%{ENDC}')
    else:
        print(f'{PURPLE}Win rate:{ENDC} {L_GREEN}{win_rate_actual:.2f}%{ENDC}')

print(f'{PURPLE}Total capital lost due to commission :{ENDC} {executed_trades * commission_per_trade}')
print()

# Target Goal or Prop Firm Results
if account_type == 1 and target_goal:
    accounts_meeting_goal = np.sum(final_balances_array >= target_goal)
    percentage_met_goal = (accounts_meeting_goal / len(final_balances_array)) * 100
    
    print(f"{GREEN}Number of Accounts Meeting Target Goal (${target_goal}):{ENDC} {L_GREEN}{accounts_meeting_goal}{ENDC}")
    print(f"{GREEN}Percentage of Accounts Meeting Target Goal:{ENDC} {L_GREEN}{percentage_met_goal:.2f}%{ENDC}")

elif account_type == 2:
    print(f"\n{CYAN}Prop Firm Results:{ENDC}\n")
    total_accounts = len(final_balances_array)
    passed_accounts = total_accounts - prop_lost
    
    print(f"{RED}Number of Accounts Failed (>= {not_accepted_max_dd}%) :{ENDC} {L_RED}{prop_lost}{ENDC}")
    print(f"{GREEN}Number of Accounts Not Failed :{ENDC} {L_GREEN}{passed_accounts}{ENDC}")
    print()
    
    print(f"{RED}Accounts Failed :{ENDC} {L_RED}{(prop_lost / total_accounts) * 100:.2f}%{ENDC}")
    print(f"{GREEN}Accounts Passed :{ENDC} {GREEN}{(passed_accounts / total_accounts) * 100:.2f}%{ENDC}")

print(f'\n{PURPLE}------------------------end-----------------------------------{ENDC}\n')

end_time = datetime.now()
execution_time = end_time - start_time
print(f"Execution time: {execution_time}")
print(end_time)

plt.show()