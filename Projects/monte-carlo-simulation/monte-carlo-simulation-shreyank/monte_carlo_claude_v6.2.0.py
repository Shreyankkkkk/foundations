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
import sys
import traceback
from contextlib import contextmanager

# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

class SimulationError(Exception):
    """Base exception for simulation errors"""
    pass

class DatabaseError(SimulationError):
    """Database connection/query errors"""
    pass

class InputValidationError(SimulationError):
    """User input validation errors"""
    pass

class NumericalError(SimulationError):
    """Numerical computation errors"""
    pass

@contextmanager
def safe_database_connection(host, user, passwd, database):
    """Context manager for safe database operations"""
    conn = None
    cursor = None
    try:
        conn = sql.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database,
            connect_timeout=10
        )
        cursor = conn.cursor()
        
        if not conn.is_connected():
            raise DatabaseError("Failed to establish database connection")
        
        print(f"{GREEN}Database Connected{ENDC}")
        yield conn, cursor
        
    except sql.Error as e:
        raise DatabaseError(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print(f"{YELLOW}Database connection closed{ENDC}")

def safe_int_input(prompt, min_val=None, max_val=None, default=None):
    """Safely get integer input with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            
            value = int(user_input)
            
            if min_val is not None and value < min_val:
                print(f"{RED}Value must be >= {min_val}{ENDC}")
                continue
            if max_val is not None and value > max_val:
                print(f"{RED}Value must be <= {max_val}{ENDC}")
                continue
            
            return value
            
        except ValueError:
            print(f"{RED}Invalid input. Please enter a whole number.{ENDC}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Input cancelled by user{ENDC}")
            sys.exit(0)

def safe_float_input(prompt, min_val=None, max_val=None, default=None):
    """Safely get float input with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            
            value = float(user_input)
            
            if min_val is not None and value < min_val:
                print(f"{RED}Value must be >= {min_val}{ENDC}")
                continue
            if max_val is not None and value > max_val:
                print(f"{RED}Value must be <= {max_val}{ENDC}")
                continue
            
            return value
            
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{ENDC}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Input cancelled by user{ENDC}")
            sys.exit(0)

def validate_risk_levels(risk_levels):
    """Validate risk levels array"""
    if not risk_levels:
        raise InputValidationError("Risk levels cannot be empty")
    
    if not all(0 <= r <= 1 for r in risk_levels):
        raise InputValidationError("All risk levels must be between 0 and 1")
    
    return True

def safe_array_operation(func, *args, **kwargs):
    """Safely execute numpy operations with error handling"""
    try:
        result = func(*args, **kwargs)
        
        # Check for NaN or Inf
        if isinstance(result, np.ndarray):
            if np.any(np.isnan(result)):
                raise NumericalError("Operation produced NaN values")
            if np.any(np.isinf(result)):
                raise NumericalError("Operation produced infinite values")
        
        return result
        
    except FloatingPointError as e:
        raise NumericalError(f"Numerical error in array operation: {e}")
    except MemoryError:
        raise NumericalError("Insufficient memory for operation")

# ============================================================================
# COLOR CONSTANTS
# ============================================================================

L_GREEN = '\033[92m'
GREEN = '\033[32m'
RED = '\033[91m'
L_RED = '\033[31m'
YELLOW = '\033[93m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
ENDC = '\033[0m'

print()
start_time = datetime.now()
print(start_time)
print()

# ============================================================================
# USER INPUT & DATABASE SETUP WITH ERROR HANDLING
# ============================================================================

try:
    a = safe_int_input(f"{PURPLE}Enter Password : {ENDC}")
    
    try:
        conn = sql.connect(
            host='localhost',
            user='root',
            passwd=str(a),
            database='monte_carlo',
            connect_timeout=10
        )
        cursor = conn.cursor()
        
        if not conn.is_connected():
            raise DatabaseError("Failed to establish database connection")
        
        print(f"{GREEN}Connected: {ENDC}")
    except sql.Error as e:
        raise DatabaseError(f"Database connection failed: {e}")
    
    print(f'\n{PURPLE}--------------------Monte Carlo Simulation--------------------{ENDC}\n')
    
    mode = input(f"{CYAN}Press: (1) for New Run / (2) to Reproduce Previous Run: {ENDC} ")
    
    if mode == '1':
        seed = random.randint(1, 1000000)
        print(f"{YELLOW}Generated new seed: {seed}{ENDC}")
    
        def random_number_of_trades():
            return random.randint(150, 624)
    
        while True:
            n = safe_int_input(
                f"{CYAN}(1) Random Number of Trades per year \n(2) Enter a Number: \nPress 1 / 2 : {ENDC}",
                min_val=1,
                max_val=2
            )
            if n == 1:
                trades = random_number_of_trades()
                print(f'{YELLOW}Evaluating {trades} number of trades a year{ENDC}')
                break
            elif n == 2:
                trades = safe_int_input(f"{CYAN}Number of Trades :{ENDC}", min_val=1)
                break
        print()
    
        def risk():
            risk_level = []
            try:
                n = safe_int_input(f"{CYAN}Number of Risk : (like 2 = 1% and 0.5%) :{ENDC}", min_val=1)
            except ValueError:
                print(f"{RED}Invalid Input: Please enter whole number{ENDC}")
                return []
            for i in range(1, n + 1):
                while True:
                    try:
                        user_input = safe_float_input(
                            f'{CYAN}Input Risk {i} (%) :{ENDC}',
                            min_val=0,
                            max_val=100
                        )
                        risk_level.append(user_input / 100)
                        break
                    except ValueError:
                        print(f"{RED}Invalid Input: Please enter a number.{ENDC}")
            return risk_level 
        
        runs = safe_int_input(f"{CYAN}Number of Runs :{ENDC}", min_val=1)
        n_people = safe_int_input(f'{CYAN}Number of People :{ENDC}', min_val=1)
        account_size = safe_float_input(f"{CYAN}Account Size :{ENDC}", min_val=1)
        win_ratee = safe_float_input(f"{CYAN}Minimum Win Rate :{ENDC}", min_val=0, max_val=100)
        lower_limit_rr = safe_float_input(f"{CYAN}Minimum RR :{ENDC}", min_val=0)
        upper_limit_rr = safe_float_input(f"{CYAN}Maximum RR :{ENDC}", min_val=lower_limit_rr)
        commission_per_trade = safe_float_input(f"{CYAN}Enter $ Commission per trade :{ENDC}", min_val=0)
        break_even_per_cent = safe_float_input(f"{CYAN}Enter Break Even Percentage :{ENDC}", min_val=0, max_val=100)
        print()
    
        while True:
            risk_levels = risk()
            if len(risk_levels) >= 1:
                break
            else:
                print(f"{RED}Risk has to be entered :{ENDC}")
    
        while True:
            print(f"{YELLOW}\nRange is 0-10, realistically it doesnt increase above that{ENDC}")
            win_rate_change = safe_float_input(
                f"{CYAN}Changes in Win rate depending on the month :{ENDC}",
                min_val=0,
                max_val=10
            )
            break
        
        # NEW: Missed trade percentage
        print(f"\n{YELLOW}Execution Realism Settings{ENDC}")
        missed_trade_pct = safe_float_input(
            f"{CYAN}Missed Trade Percentage (5-10% realistic) :{ENDC}",
            min_val=0,
            max_val=50,
            default=7.5
        )
        
        risk_levels_str = ','.join(str(r) for r in risk_levels)
    
        try:
            cursor.execute("""
    INSERT INTO monte_carlo_runs
    (seed, num_trades, account_size, min_win_rate, min_rr, max_rr, commission, win_rate_change, risk_levels, runs, n_people)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
          commission_per_trade, win_rate_change, risk_levels_str, runs, n_people))
            conn.commit()
            print(f"{GREEN}Parameters saved to database{ENDC}")
        except sql.Error as e:
            raise DatabaseError(f"Failed to save parameters: {e}")
    
    elif mode == '2':
        run_id = safe_int_input(f"{CYAN}Enter the Run ID to reproduce: {ENDC}", min_val=1)
        
        try:
            cursor.execute("SELECT * FROM monte_carlo_runs WHERE run_id = %s", (run_id,))
            result = cursor.fetchone()
            
            if result:
                (run_id, seed, trades, account_size, win_ratee, lower_limit_rr, upper_limit_rr,
                 commission_per_trade, win_rate_change, risk_levels_str, runs, n_people, created_at) = result
                risk_levels = [float(r) for r in risk_levels_str.split(',') if r.strip()]
                print(f"{YELLOW}Reproducing run with seed: {seed}{ENDC}")
                break_even_per_cent = safe_float_input(f"{CYAN}Enter Break Even Percentage :{ENDC}", min_val=0, max_val=100)
                missed_trade_pct = safe_float_input(
                    f"{CYAN}Missed Trade Percentage (5-10% realistic) :{ENDC}",
                    min_val=0,
                    max_val=50,
                    default=7.5
                )
            else:
                raise DatabaseError(f"Run ID {run_id} not found")
        except sql.Error as e:
            raise DatabaseError(f"Database query failed: {e}")
    else:
        print(f"{RED}Invalid mode selection. Exiting.{ENDC}")
        exit()

except DatabaseError as e:
    print(f"\n{RED}Database Error: {e}{ENDC}")
    sys.exit(1)
except KeyboardInterrupt:
    print(f"\n{YELLOW}Cancelled by user{ENDC}")
    sys.exit(0)
except Exception as e:
    print(f"\n{RED}Unexpected Error: {e}{ENDC}")
    traceback.print_exc()
    sys.exit(1)

random.seed(seed)
np.random.seed(seed)
print()

while True:
    account_type = safe_int_input(
        f"{CYAN}Run for (1) Live Account / (2) Prop firm Trading : {ENDC}",
        min_val=1,
        max_val=2
    )
    if account_type in [1, 2]:
        if account_type == 1:
            target_goal = safe_float_input(f"{CYAN}Enter Target Goal :{ENDC}", min_val=account_size) 
            not_accepted_max_dd = None
        elif account_type == 2:
            print(f"{YELLOW}Prop Firm Trading selected. Enter Rules{ENDC}")
            not_accepted_max_dd = safe_float_input(
                f"{CYAN}Maximum Drawdown allowed :{ENDC}",
                min_val=0,
                max_val=100
            )
            target_goal = None
        break

risk_levels_np = np.array(risk_levels)

# ============================================================================
# VECTORIZED HELPER FUNCTIONS
# ============================================================================

@jit(nopython=True)
def generate_monthly_split(trades):
    """Vectorized monthly trade distribution"""
    array = np.array([0.8, 1.0, 1.2, 1.1, 1.3, 1.0, 0.9, 0.7, 1.1, 1.2, 0.9, 0.6])
    weights = array / array.sum()
    monthly_trades = (weights * trades).astype(np.int32)
    
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
def generate_regime_sequence(n_trades, avg_regime_length=20):
    """
    Generate regime sequence with state transitions
    States: 0=HOT, 1=NEUTRAL, 2=COLD
    """
    regimes = np.zeros(n_trades, dtype=np.int32)
    current_regime = 1  # Start neutral
    trades_in_regime = 0
    
    for i in range(n_trades):
        regimes[i] = current_regime
        trades_in_regime += 1
        
        # Regime change probability increases with time in regime
        change_prob = min(0.3, trades_in_regime / avg_regime_length * 0.15)
        
        if np.random.random() < change_prob:
            # Transition probabilities
            if current_regime == 0:  # HOT
                current_regime = 1 if np.random.random() < 0.7 else 2
            elif current_regime == 1:  # NEUTRAL
                rand = np.random.random()
                if rand < 0.4:
                    current_regime = 0  # To HOT
                elif rand < 0.8:
                    current_regime = 1  # Stay NEUTRAL
                else:
                    current_regime = 2  # To COLD
            else:  # COLD
                current_regime = 1 if np.random.random() < 0.6 else 0
            
            trades_in_regime = 0
    
    return regimes

@jit(nopython=True)
def vectorized_trade_simulation(n_trades, account_size, risk_levels, win_rate_base, 
                                lower_rr, upper_rr, commission, be_percent, 
                                max_dd_threshold, is_prop_firm, missed_trade_pct):
    """Core vectorized simulation loop with regimes and missed trades"""
    
    equity_curve = np.zeros(n_trades + 1)
    equity_curve[0] = account_size
    
    initial_account_size = account_size
    current_account = account_size
    risk_index = 0
    
    current_win_streak = 0
    current_loss_streak = 0
    longest_win_streak = 0
    longest_loss_streak = 0
    current_be_streak = 0
    longest_be_streak = 0
    
    # Generate regime sequence
    regimes = generate_regime_sequence(n_trades)
    
    # Generate all random numbers at once
    win_rolls = np.random.randint(1, 101, n_trades)
    htf_rolls = np.random.randint(1, 6, n_trades)
    sweep_rolls = np.random.randint(1, 6, n_trades)
    rr_ratios = generate_rr_ratios(n_trades, lower_rr, upper_rr)
    slippage = np.random.uniform(0.996, 1.004, n_trades)
    be_rolls = np.random.randint(1, 101, n_trades)
    t_dist_samples = np.abs(np.random.standard_t(3, n_trades))
    slip_apply = np.random.randint(1, 3, n_trades)
    additional_slip = np.random.uniform(0.75, 0.90, n_trades)
    apply_additional = np.random.random(n_trades) < 0.05
    
    # NEW: Missed trade rolls
    missed_rolls = np.random.random(n_trades) * 100
    
    wins = 0
    losses = 0
    be_count = 0
    missed_count = 0
    total_profit = 0.0
    total_loss = 0.0
    
    actual_rr_ratios = np.zeros(n_trades)
    rr_count = 0
    
    recent_wins = np.zeros(10, dtype=np.int32)
    recent_idx = 0
    
    stop_simulation = False
    actual_trades = 0
    
    for i in range(n_trades):
        if stop_simulation:
            break
        
        if current_account <= 0:
            stop_simulation = True
            break
        
        # Get current regime
        regime = regimes[i]
        
        # NEW: Missed trade logic - bias towards cold regimes
        miss_threshold = missed_trade_pct
        if regime == 2:  # COLD regime
            miss_threshold *= 1.5  # 50% more likely to miss in cold
        elif regime == 0:  # HOT regime
            miss_threshold *= 0.7  # 30% less likely to miss in hot
        
        if missed_rolls[i] < miss_threshold:
            missed_count += 1
            actual_trades += 1
            equity_curve[actual_trades] = current_account
            continue
        
        # HTF and Sweep checks
        htf = htf_rolls[i] <= 3
        swp = sweep_rolls[i] < 3
        
        # Adjust RR based on regime
        rr = rr_ratios[i]
        if htf and swp:
            rr += 0.75
        elif htf or swp:
            rr += 0.5
        
        # Regime RR modifiers
        if regime == 0:  # HOT - better RR tail
            rr *= 1.1
        elif regime == 2:  # COLD - worse RR
            rr *= 0.9
        
        actual_rr_ratios[rr_count] = rr
        rr_count += 1
        
        base_risk = initial_account_size * risk_levels[risk_index]
        max_risk_multiplier = min(2.0, current_account / initial_account_size)
        risk = base_risk * max_risk_multiplier
        
        # Base win probability
        win_prob = win_rate_base
        
        # Regime win rate modifiers
        if regime == 0:  # HOT
            win_prob += 5
        elif regime == 2:  # COLD
            win_prob -= 10
        
        # HTF/Sweep adjustments
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
        
        win_prob = min(win_prob, 95)
        
        # Break even check - regime affects BE probability
        be_threshold = be_percent
        if regime == 2:  # COLD - more BEs
            be_threshold *= 1.3
        
        if be_rolls[i] <= be_threshold:
            be_count += 1
            current_be_streak += 1
            current_win_streak = 0
            current_loss_streak = 0
            longest_be_streak = max(longest_be_streak, current_be_streak)
            actual_trades += 1
            equity_curve[actual_trades] = current_account
            continue
        
        # Determine win/loss
        is_win = win_rolls[i] < win_prob
        
        if is_win:
            profit_multiplier = min(t_dist_samples[i], 2.5)
            profit = profit_multiplier * rr * risk
            
            max_profit = 0.10 * current_account
            profit = min(profit, max_profit)
            
            if slip_apply[i] == 1:
                profit *= slippage[i]
            if apply_additional[i]:
                profit *= additional_slip[i]
            
            current_account += profit
            current_account -= commission
            total_profit += profit
            
            wins += 1
            current_win_streak += 1
            current_loss_streak = 0
            current_be_streak = 0
            longest_win_streak = max(longest_win_streak, current_win_streak)
            
            risk_index = 0
            
            if recent_idx < 10:
                recent_wins[recent_idx] = 1
            else:
                for j in range(9):
                    recent_wins[j] = recent_wins[j+1]
                recent_wins[9] = 1
            recent_idx += 1
            
        else:
            loss_multiplier = min(t_dist_samples[i], 2.5)
            loss = loss_multiplier * risk
            
            max_loss = 0.03 * current_account
            loss = min(loss, max_loss)
            
            if slip_apply[i] == 1:
                loss *= slippage[i]
            if apply_additional[i]:
                loss *= additional_slip[i]
            
            current_account -= loss
            current_account -= commission
            total_loss += loss
            
            losses += 1
            current_loss_streak += 1
            current_win_streak = 0
            current_be_streak = 0
            longest_loss_streak = max(longest_loss_streak, current_loss_streak)
            
            risk_index = min(risk_index + 1, len(risk_levels) - 1)
            
            if recent_idx < 10:
                recent_wins[recent_idx] = 0
            else:
                for j in range(9):
                    recent_wins[j] = recent_wins[j+1]
                recent_wins[9] = 0
            recent_idx += 1
        
        actual_trades += 1
        equity_curve[actual_trades] = current_account
        
        # Prop firm check
        if is_prop_firm and max_dd_threshold > 0:
            if actual_trades > 0:
                peak = equity_curve[0]
                for k in range(actual_trades + 1):
                    if equity_curve[k] > peak:
                        peak = equity_curve[k]
                
                if peak > 0:
                    dd = (peak - current_account) / peak
                    if dd >= max_dd_threshold:
                        stop_simulation = True
    
    return (equity_curve[:actual_trades+1], wins, losses, be_count, 
            longest_win_streak, longest_loss_streak, longest_be_streak, 
            stop_simulation, total_profit, total_loss, actual_rr_ratios[:rr_count],
            missed_count)

# ============================================================================
# RUN SIMULATIONS
# ============================================================================

print(f"{YELLOW}Running vectorized simulation with regime modeling...{ENDC}\n")

total_simulations = runs * n_people
all_results = []

regime_choices = np.random.choice([0, 1, 2], size=(total_simulations, 12))

try:
    for sim_idx in range(total_simulations):
        base_win_rate = win_ratee
        month_mod = np.random.randint(1, 4)
        if month_mod == 1:
            base_win_rate -= win_rate_change
        elif month_mod == 2:
            base_win_rate += win_rate_change
        
        if np.random.random() < 0.10:
            base_win_rate -= win_rate_change
        
        is_prop = 1 if account_type == 2 else 0
        dd_threshold = (not_accepted_max_dd / 100) if not_accepted_max_dd else 0
        
        result = vectorized_trade_simulation(
            trades, account_size, risk_levels_np, base_win_rate,
            lower_limit_rr, upper_limit_rr, commission_per_trade,
            break_even_per_cent, dd_threshold, is_prop, missed_trade_pct
        )
        
        all_results.append(result)
        
        if total_simulations >= 1000:
            milestone = max(1, total_simulations // 10)
            if (sim_idx + 1) % milestone == 0:
                print(f"Completed {sim_idx + 1}/{total_simulations} simulations ({((sim_idx + 1) / total_simulations * 100):.0f}%)")
        elif (sim_idx + 1) % 100 == 0:
            print(f"Completed {sim_idx + 1}/{total_simulations} simulations")

    print(f"{GREEN}Simulation complete!{ENDC}\n")

except Exception as e:
    print(f"{RED}Error during simulation: {e}{ENDC}")
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# EXTRACT RESULTS WITH ERROR HANDLING
# ============================================================================

print(f"{YELLOW}Extracting results...{ENDC}")
all_equity_curves = []
win_streaks = []
loss_streaks = []
be_streaks = []
final_account_balances = []
no_of_win = 0
no_of_loss = 0
be_count = 0
prop_lost = 0
total_profit = 0
total_loss = 0
all_rr_ratios = []
total_missed = 0

try:
    for idx, result in enumerate(all_results):
        if len(result) != 12:
            print(f"{RED}Warning: Result {idx} has {len(result)} elements instead of 12{ENDC}")
            continue
            
        equity, wins, losses, be, win_str, loss_str, be_str, failed, profit, loss_amt, rr_ratios, missed = result
        all_equity_curves.append(equity)
        win_streaks.append(win_str)
        loss_streaks.append(loss_str)
        be_streaks.append(be_str)
        final_account_balances.append(equity[-1])
        no_of_win += wins
        no_of_loss += losses
        be_count += be
        total_profit += profit
        total_loss += loss_amt
        all_rr_ratios.extend(rr_ratios)
        total_missed += missed
        if failed:
            prop_lost += 1
    
    print(f"{GREEN}Results extracted successfully!{ENDC}")
    
except Exception as e:
    print(f"{RED}Error extracting results: {e}{ENDC}")
    traceback.print_exc()
    exit()

executed_trades = no_of_win + no_of_loss + be_count

print(f"{YELLOW}Processing RR ratios...{ENDC}")
all_rr_ratios = np.array(all_rr_ratios)
print(f"{GREEN}RR ratios processed: {len(all_rr_ratios)} total{ENDC}\n")

# ============================================================================
# VECTORIZED METRICS CALCULATION WITH ERROR HANDLING
# ============================================================================

print(f"{YELLOW}Calculating percentile curves...{ENDC}")

try:
    all_equity_array = np.array([np.pad(curve, (0, trades + 1 - len(curve)), constant_values=np.nan) 
                                 for curve in all_equity_curves])

    print(f"{YELLOW}Calculating drawdowns and metrics...{ENDC}")
    max_drawdowns = np.array([calculate_max_drawdown(curve) for curve in all_equity_curves])
    time_unders = np.array([calculate_time_under_water(curve) for curve in all_equity_curves])
    sharpe_ratios = np.array([calculate_sharpe_ratio(curve) for curve in all_equity_curves])
    sortino_ratios = np.array([calculate_sortino_ratio(curve) for curve in all_equity_curves])

    print(f"{YELLOW}Calculating percentiles...{ENDC}")
    final_balances_array = np.array(final_account_balances)
    p0_curve = np.nanpercentile(all_equity_array, 0, axis=0)
    p5_curve = np.nanpercentile(all_equity_array, 5, axis=0)
    p50_curve = np.nanpercentile(all_equity_array, 50, axis=0)
    p95_curve = np.nanpercentile(all_equity_array, 95, axis=0)
    p100_curve = np.nanpercentile(all_equity_array, 100, axis=0)

    print(f"{YELLOW}Calculating risk metrics...{ENDC}")
    total_returns = (final_balances_array / account_size) - 1
    var_5 = np.percentile(total_returns, 5)
    expected_shortfall = np.mean(total_returns[total_returns <= var_5])
    probability_ruin = np.sum(final_balances_array < 0.5 * account_size) / len(final_balances_array)

    print(f"{GREEN}All calculations complete!{ENDC}\n")

except NumericalError as e:
    print(f"{RED}Numerical error in calculations: {e}{ENDC}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"{RED}Unexpected error in calculations: {e}{ENDC}")
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# PRINT RISK METRICS
# ============================================================================

print(f"{PURPLE}5% VaR:{ENDC} {RED}{round(var_5, 4)}{ENDC}")
print(f"{PURPLE}Expected Shortfall:{ENDC} {RED}{round(expected_shortfall, 4)}{ENDC}")
print(f"{PURPLE}Probability of Ruin (<50% account):{ENDC} {RED}{round(probability_ruin * 100, 2)}%{ENDC}")
print()

# ============================================================================
# OPTIMIZED PLOTTING - FIXES O(n²) ISSUE
# ============================================================================

def plot_equity_curves_optimized():
    """
    OPTIMIZED: O(1) plotting instead of O(n)
    Uses percentile bands instead of individual curves
    """
    print(f"\n{YELLOW}Generating Equity Curves Graph (Optimized)...{ENDC}\n")
    
    try:
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(14, 8))
        
        sample_size = min(50, len(all_equity_curves))
        sample_indices = np.random.choice(len(all_equity_curves), sample_size, replace=False)
        
        for idx in sample_indices:
            plt.plot(all_equity_curves[idx], color='white', alpha=0.05, linewidth=0.5)
        
        x_range = range(len(p50_curve))
        
        plt.plot(p50_curve, color='lime', label='Median (P50)', linewidth=2.5, zorder=5)
        plt.plot(p5_curve, color='red', linestyle='--', label='5th Percentile (P5)', linewidth=2)
        plt.plot(p95_curve, color='red', linestyle='--', label='95th Percentile (P95)', linewidth=2)
        
        plt.fill_between(x_range, p5_curve, p95_curve, color='gray', alpha=0.18, label='5th - 95th')
        plt.fill_between(x_range, p0_curve, p5_curve, color='gray', alpha=0.18, label='0th - 5th')
        plt.fill_between(x_range, p95_curve, p100_curve, color='turquoise', alpha=0.18, label='95th - 100th')
        
        plt.axhline(y=account_size, color='white', linestyle=':', alpha=0.5, label='Starting Balance')
        
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Account Balance', fontsize=12)
        plt.title(f'Monte Carlo Equity Curves - {len(all_equity_curves):,} Simulations (Regime-Based)', 
                  fontsize=14, weight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show(block=False)
        
        return True
        
    except Exception as e:
        print(f"{RED}Error generating equity curves: {e}{ENDC}")
        traceback.print_exc()
        return False

plot_equity_curves_optimized()

# ============================================================================
# PRINT SUMMARY METRICS
# ============================================================================

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

if total_loss > 0:
    profit_factor = total_profit / total_loss
else:
    profit_factor = float('inf')
print(f"{CYAN}Global Profit Factor :{ENDC} {YELLOW}{profit_factor:.2f}{ENDC}")
print()

print(f"{PURPLE}Average Sharpe Ratio :{ENDC} {GREEN}{np.mean(sharpe_ratios):.3f}{ENDC}")
print(f"{PURPLE}Average Sortino Ratio :{ENDC} {GREEN}{np.mean(sortino_ratios):.3f}{ENDC}")
print()

end_no_trades = trades * n_people
total_trades_attempted = end_no_trades * runs
actual_executed = executed_trades
print(f'{PURPLE}Total number of trades attempted :{ENDC} {total_trades_attempted}')
print(f'{PURPLE}Total number of trades executed :{ENDC} {actual_executed}')
print(f'{PURPLE}Total number of trades MISSED :{ENDC} {RED}{total_missed}{ENDC} ({RED}{(total_missed/total_trades_attempted)*100:.2f}%{ENDC})')
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

# ============================================================================
# TARGET GOAL OR PROP FIRM RESULTS
# ============================================================================

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

# ============================================================================
# RR DISTRIBUTION GRAPH - OPTIMIZED
# ============================================================================

def plot_rr_distribution_optimized():
    """Optimized RR distribution plotting with smart KDE/histogram switching"""
    print(f"\n{YELLOW}Generating RR Distribution Graph...{ENDC}\n")
    
    try:
        if len(all_rr_ratios) == 0:
            print(f"{RED}No RR ratios to plot{ENDC}")
            return False
        
        use_kde = len(all_rr_ratios) <= 1_000_000
        
        if not use_kde:
            print(f"{YELLOW}Large dataset ({len(all_rr_ratios):,} trades), using histogram for speed{ENDC}")
        
        mean_rr = np.mean(all_rr_ratios)
        median_rr = np.median(all_rr_ratios)
        r0_curve = np.percentile(all_rr_ratios, 0)
        r5_curve = np.percentile(all_rr_ratios, 5)
        r50_curve = np.percentile(all_rr_ratios, 50)
        r95_curve = np.percentile(all_rr_ratios, 95)
        r100_curve = np.percentile(all_rr_ratios, 100)
        
        plt.style.use('default')
        fig = plt.figure(figsize=(14, 7))
        
        if use_kde:
            sample_size = min(100_000, len(all_rr_ratios))
            if sample_size < len(all_rr_ratios):
                sampled_rr = np.random.choice(all_rr_ratios, sample_size, replace=False)
            else:
                sampled_rr = all_rr_ratios
            
            kde = gaussian_kde(sampled_rr)
            x_val = np.linspace(all_rr_ratios.min(), all_rr_ratios.max(), 1000)
            y_val = kde(x_val)
            
            plt.plot(x_val, y_val, color='darkblue', linewidth=2, label='RR Distribution')
            
            mask1 = (x_val >= r0_curve) & (x_val <= r5_curve)
            mask2 = (x_val >= r5_curve) & (x_val <= r95_curve)
            mask3 = (x_val >= r95_curve) & (x_val <= r100_curve)
            
            plt.fill_between(x_val[mask1], y_val[mask1], alpha=0.3, color='red', label='0th-5th Percentile')
            plt.fill_between(x_val[mask2], y_val[mask2], alpha=0.3, color='green', label='5th-95th Percentile')
            plt.fill_between(x_val[mask3], y_val[mask3], alpha=0.3, color='orange', label='95th-100th Percentile')
        else:
            plt.hist(all_rr_ratios, bins=100, density=True, alpha=0.7, color='darkblue', 
                    edgecolor='black', label='RR Distribution (Histogram)')
        
        plt.axvline(mean_rr, color='purple', linestyle='--', linewidth=2, label=f'Mean: {mean_rr:.2f}')
        plt.axvline(median_rr, color='cyan', linestyle='--', linewidth=2, label=f'Median: {median_rr:.2f}')
        
        counter = Counter(np.round(all_rr_ratios, 1))
        most_common_rr, count = counter.most_common(1)[0]
        plt.axvline(most_common_rr, color='black', linestyle=':', linewidth=1.5, 
                    label=f'Most Common: {most_common_rr:.1f}')
        
        plt.xlabel("Risk:Reward Ratio", fontsize=12, weight='bold')
        plt.ylabel("Density", fontsize=12, weight='bold')
        plt.title(f"Risk:Reward Distribution Across {len(all_rr_ratios):,} Trades (Regime-Adjusted)", 
                  fontsize=14, weight='bold')
        plt.legend(loc='upper right', fontsize=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        stats_text = f"""Statistics:
Min: {r0_curve:.2f}
5th %: {r5_curve:.2f}
Median: {r50_curve:.2f}
Mean: {mean_rr:.2f}
95th %: {r95_curve:.2f}
Max: {r100_curve:.2f}"""
        
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        print(f"{GREEN}RR Distribution Statistics:{ENDC}")
        print(f"  Mean RR: {mean_rr:.2f}")
        print(f"  Median RR: {median_rr:.2f}")
        print(f"  Most Common RR: {most_common_rr:.1f}")
        print(f"  Min RR: {r0_curve:.2f}")
        print(f"  Max RR: {r100_curve:.2f}")
        print(f"  5th Percentile: {r5_curve:.2f}")
        print(f"  95th Percentile: {r95_curve:.2f}")
        
        return True
        
    except Exception as e:
        print(f"{RED}Error generating RR distribution: {e}{ENDC}")
        traceback.print_exc()
        return False

plot_rr_distribution_optimized()

plt.show()