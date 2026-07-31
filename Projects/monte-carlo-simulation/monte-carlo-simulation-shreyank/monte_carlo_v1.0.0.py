import random
import matplotlib
import statistics 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import deque,Counter
import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde

#Monte Carlo Simulation for Use
    #varying risk starting at 1%. if loss: 0.5% until a new win
start_time=datetime.now()
print(start_time)

print('\n--------------------Monte Carlo Simulation--------------------')
print()
    #To get number of trades
def random_number_of_trades():
    return random.randint(150,624)
while True:
    n=int(input("(1) Random Number of Trades per year \n(2) Enter a Number: \nPress 1 / 2 : "))
    if n==1:
        trades=random_number_of_trades()
        print(f'Evaluating {trades} number of trades a year')
        break
    elif n==2:
        trades=int(input("Number of Trades :"))
        break
    else:
        print("Wrong Input~")
        continue
print()


    #To get all the user input data
runs=int(input("Number of Runs :"))
n_people = int(input('Number of People :'))
account_size = int(input("Account Size :"))
win_ratee = int(input("Minimum Win Rate :"))
lower_limit_rr=float(input("Minimum RR :"))
upper_limit_rr=float(input("Maximum RR :"))
commission_per_trade = float(input("Enter $ Commission per trade :"))


while True:
    print("Range is 0-10, realistically it doesnt increase above that")
    win_rate_change = float(input("Changes in Win rate depending on the month :"))
    if 0 <= win_rate_change <= 10:
        break
    else:
        print()
        continue
    

    #lists to find the max,min,average and pf
list1=[]
win_streaks=[]
loss_streaks=[]
all_equity_curves = []
time_under = []
max_drawdown = []
max_duration = []
sharpe_list = []
sortino_list = []
calmar_list = []
rr_distribution = []
all_metrics=[]
returns_window=deque(maxlen=20)

    #to seperate number of trades in 12 different blocks: months  
def random_monthly_split(trades):
    array = np.array([0.8, 1.0, 1.2, 1.1, 1.3, 1.0, 0.9, 0.7, 1.1, 1.2, 0.9, 0.6]) #used to create an array of 12 elements
    weigh = np.random.dirichlet(array,size=1)[0] #randomly distributes decimal places amongst 12 elements, sums up to 1
    monthly_trades = (weigh*trades).astype(int)
    while sum(monthly_trades) < trades: #if number is less, adds 1 to a random position
        monthly_trades[random.randint(0,11)] += 1
    while sum(monthly_trades) > trades: #if number is more, subtracts 1 from random position
        monthly_trades[random.randint(0,11)] -= 1
    return monthly_trades.tolist() #converts array into list
    

    #constants
total_profit = 0
total_loss = 0
count1=0
count2=0
count3=0

    #Spliting trades accross mon-fri
def split_trades_week(trades):
    array = np.array([0.7, 0.8, 1.3, 1.4, 1.2]) #used to create an array of 12 elements
    weigh = np.random.dirichlet(array,size=1)[0] #randomly distributes decimal places amongst 12 elements, sums up to 1
    weekday_trades = (weigh*trades).astype(int)
    while sum(weekday_trades) < trades: #if number is less, adds 1 to a random position
        weekday_trades[random.randint(0,4)] += 1
    while sum(weekday_trades) > trades: #if number is more, subtracts 1 from random position
        weekday_trades[random.randint(0,4)] -= 1
    return weekday_trades.tolist() #converts array into list

    #news_event()
def news_event():
    global count2
    if random.random() < 0.01:
        count2+=1
        return random.uniform(3,5)
    return 1

    #Win rate change depending on month
def month():
    return random.randint(1,3)

    #win rate change depending on counter trend
def counter():
    if random.random()<0.10:
        return True
    
    #maximum drawdown from its peak
def max_draw(equity_curve):
    peak=equity_curve[0]
    max_dd = 0.0
    for x in equity_curve:
        peak = max(peak,x)
        drawdown = (peak-x)/peak
        max_dd = max(max_dd,drawdown)
    return max_dd

    #Sharpe Ratio
def sharpe_ratio(equity_curve):
    returns=np.diff(equity_curve)/equity_curve[:-1]
    mean_return=np.mean(returns)
    std_return=np.std(returns)
    if std_return==0:
        return 0
    return mean_return/std_return
    
    #Sortino Ratio
def sortino_ratio(equity_curve):
    returns=np.diff(equity_curve)/equity_curve[:-1]
    downside_returns=returns[returns<0]
    downside_std=np.std(downside_returns)
    if downside_std==0:
        return 0
    mean_return=np.mean(returns)
    return mean_return/downside_std

    
    #Calmar Ratio
def calmar_ratio(equity_curve):
    total_return = (equity_curve[-1] / equity_curve[0])-1
    max_dd = max_draw(equity_curve)
    if max_dd == 0:
        return float('inf')
    return total_return / max_dd


    #number of trades to get out of drawdown
def drawdown_duration(equity_curve):
    peak = equity_curve[0]
    durations=[]
    in_drawdown=False
    start_index=0
    for i,x in enumerate(equity_curve):
        if x<peak:
            if not in_drawdown:
                in_drawdown=True
                start_index=1
        else:
            if in_drawdown:
                durations.append(i-start_index)
                in_drawdown=False
    if in_drawdown:
        durations.append(len(equity_curve)-start_index)
    return durations

    #Time under water, peak of account, for psycology
def time_under_water(equity_curve):
    peak = equity_curve[0]
    tuw = 0
    current = 0
    for x in equity_curve:
        if x<peak:
            current+=1
            tuw = max(tuw,current)
        else:
            peak = x
            current = 0
    return tuw

    #Higher Time Frame alignment
def htf_align():
    n=random.randint(1,5)
    if n<=3:
        return True
    elif n>3:
        return False

    #To check sweeps
def sweep():
    n=random.randint(1,5)
    if n<3:
        return True
    elif n>=3:
        return False

    #to generate random risk_to_reward 
def risk_to_reward():
    return random.uniform(lower_limit_rr,upper_limit_rr)

    #function to do all the calculation
def function_control(account_size,number_of_trades):
    global count_check,total_profit,total_loss,count3
    wX = []
    vY = []

    risk_levels = [0.01,0.005]
    risk_index = 0

    trade_number=1

    current_win_streak = 0
    current_loss_streak = 0
    longest_win_streak = 0
    longest_loss_streak = 0

    wins_losses = []
    for month_trades in random_monthly_split(trades):
        new_win_rate=win_ratee
        n1=month()
        if n1==1:
            new_win_rate-=win_rate_change
        elif n1==2:
            new_win_rate+=win_rate_change
            
        if counter():
            new_win_rate-=win_rate_change

        week_block = split_trades_week(month_trades)
        weekdays = ['Mon','Tue','Wed','Thu','Fri']

        for day_index,n_trades in enumerate(week_block):
            for j in range(n_trades):
                htf = htf_align()
                swp = sweep()
                
                n5 = risk_to_reward()
                if htf and swp: #condition for risk changes
                    n5+=0.75
                elif htf or swp:
                    n5+=0.5
                risk = account_size * risk_levels[risk_index]

                n4=random.randint(1,100)    #htf and sweep
                if htf and swp:
                    n4+=10
                elif htf or swp:
                    n4+=5

                if n4 < new_win_rate:      #win and not win
                    win=True
                else:
                    win=False
                
                if len(returns_window)>2: #slippage
                    vol = statistics.pstdev(returns_window)
                else:
                    vol=0.01
                    
                base_slippage=0.002           #slippage and fraction slippage
                k=0.15
                slippage_fraction = base_slippage + k*vol
                slippage_pct = random.uniform(1-slippage_fraction,1+slippage_fraction)
                slip = random.randint(1,2)

                rr_distribution.append(n5)

                if day_index in [2,3]:            #news
                    news_multipler = news_event()
                    if news_multipler != 1:
                        if random.random() < 0.5:
                            count3+=1
                            win = not win
                    n5 *= news_multipler
                              
                if win:
                    profit = (n5*risk)  #if trade is a win

                    n=profit/account_size
                    returns_window.append(n)
                    if slip==1:
                        profit *= slippage_pct

                    if random.random() < 0.15: #partial profits
                        profit *= random.uniform(0.75,0.90)
                    
                    account_size += profit
                    total_profit += profit

                    account_size -= commission_per_trade  #comission

                    current_win_streak += 1
                    current_loss_streak = 0
                    risk_index = 0
                    if current_win_streak > longest_win_streak: #to calculate win streak
                        longest_win_streak = current_win_streak
                    wins_losses.append(True)
                    
                else:
                    loss = risk     #if trade is a loss

                    n=(-loss)/account_size
                    returns_window.append(n)
                    if slip==1:
                        loss *= slippage_pct

                    if random.random() < 0.15: #early exit
                        loss *= random.uniform(0.75,0.90)
                    
                    account_size -= loss
                    total_loss += loss

                    account_size -= commission_per_trade  #comission

                    current_loss_streak += 1
                    current_win_streak = 0
                    if risk_index < len(risk_levels) -1: #to change the risk 
                        risk_index += 1
                    if current_loss_streak > longest_loss_streak:#to calculate losing streak
                        longest_loss_streak = current_loss_streak
                    wins_losses.append(False)
                    
                wX.append(trade_number)
                vY.append(account_size)
                trade_number += 1
        
    all_equity_curves.append(vY.copy()) #to get list of final values
    list1.append(account_size)

    tuw = time_under_water(vY) #to get time under water
    time_under.append(tuw)

    max_d=max_draw(vY) #to get max drawdown
    max_drawdown.append(max_d)

    duration = drawdown_duration(vY) #to calculate number of trades to get out
    max_duration.extend(duration)     #of maximum and worst drawdowj
    
    plt.plot(wX,vY,alpha=0.3) #to plot the graph and return
    return longest_win_streak,longest_loss_streak
    
#Number of Runs for the simulation
while count1 < runs:
    count=1
    while count <= n_people:
        longest_win,longest_loss=function_control(account_size,trades)
        win_streaks.append(longest_win)
        loss_streaks.append(longest_loss)
        count += 1
    count1+=1
print()

#Value at Risk, Expected Shortfall, Probablity of Ruin
total_returns,worst_returns=[],[]
for curve in all_equity_curves:
    pct_return = (curve[-1]/curve[0]) - 1
    total_returns.append(pct_return)
var_5 = np.percentile(total_returns,5)
for r in total_returns:
    if r <= var_5:
        worst_returns.append(r)
expected_shortfall = sum(worst_returns)
ruin_count = 0
for curve in all_equity_curves:
    if curve[-1] < 0.5*account_size:
        ruin_count += 1
probablity_ruin = ruin_count / len(all_equity_curves)


print(f"5% VaR: {round(var_5,4)}")
print(f"Expected Shortfall: {round(expected_shortfall,4)}")
print(f"Probability of Ruin (<50% account): {round(probablity_ruin*100,2)}%")
print()

#to print the equity curve
equity_array = np.array(all_equity_curves)
p5_curve = np.percentile(equity_array,5,axis=0)
p50_curve = np.percentile(equity_array,50,axis=0)
p95_curve = np.percentile(equity_array,95,axis=0)

p100_curve = np.percentile(equity_array,100,axis=0)
p0_curve = np.percentile(equity_array,0,axis=0)

plt.figure(figsize=(12,7))
for curve in all_equity_curves:
    plt.plot(curve,color='black',alpha=0.1)
    
plt.plot(p50_curve,color='green',label='Median (P50)')
plt.plot(p5_curve,color='red',linestyle='--',label='5th Percentile (P5)')
plt.plot(p95_curve,color='red',linestyle='--',label='95th Percentile (P95)')
plt.fill_between(range(trades),p5_curve,p95_curve,color='green',alpha=0.5,label='5th - 95th')
plt.fill_between(range(trades),p0_curve,p5_curve,color='red',alpha=0.5,label='0th - 5th')
plt.fill_between(range(trades),p95_curve,p100_curve,color='red',alpha=0.5,label='95th - 100th')

final_p5 = p5_curve[-1]
final_p95 = p95_curve[-1]

#to prind the maximum value, 95th percentile, average, 5th percentile, minimum
print("Maximum :",max(list1))
print("Final 95th Percentile", final_p95)
print("Average :",(sum(list1)/len(list1)))
print("Final 5th Percentile", final_p5)
print("Minimum :",min(list1))
print()

#to print the longest win and losing streak
print("Average Longest Win Streak :", sum(win_streaks)/len(win_streaks))
print("Average Longest Loss Streak :", sum(loss_streaks)/len(loss_streaks))
print()

#to print average and max drawdown from the peak
avg_max_dd = sum(max_drawdown)/len(max_drawdown)*100
worst_max_dd = max(max_drawdown)*100
print("Average Max Drawdown :", str(round(avg_max_dd))+'%')
print("Worst Max Drawdown :",str(round(worst_max_dd))+'%')
print()

#to print the number of trades to get out of drawdown
avg_max_duration = sum(max_duration)/len(max_duration)
worst_max_duration = max(max_duration)
print("Average Drawdown Duration Trades :", round(avg_max_duration,2))
print("Worst Drawdown Duration Trades :", worst_max_duration)
print()

#to print the time under water
tuws = sum(time_under)/len(time_under)
print("Average Time under Water (Trades) :",tuws)
print()

#to prind the global profit factor
if total_loss > 0:
    profit_factor = total_profit / total_loss
else:
    profit_factor = float('inf')
print("Global Profit Factor :",profit_factor)
print()

#to print the average return per trade
avg_return=(sum(list1)/len(list1) - account_size)/trades
avg_return_percent=((avg_return)/(account_size))*100
print("Average Return per Trade (Absolute) :",round(avg_return,2))
print("Average Return per Trade (%) :",str(round(avg_return_percent,4,))+'%')
print()


#sharpe, sortino, calmar ratios
for curve in all_equity_curves:
    sharpe_list.append(sharpe_ratio(curve))
    sortino_list.append(sortino_ratio(curve))
    calmar_list.append(calmar_ratio(curve))
    
print("Average Sharpe Ratio :",round(np.mean(sharpe_list),3))
print("Average Sortino Ratio :",round(np.mean(sortino_list),3))
print("Average Calmar Ratio :",round(np.mean(calmar_list),3))
print()

#to print total number of runs and trades
end_no_trades = (trades*n_people)
print('Total number of trades per run :',end_no_trades)
print('Total number of trades :',(end_no_trades*runs))
print(f'Total capital lost due to comission : {end_no_trades*runs*commission_per_trade}')
print()

#News Trades
print("Total Number of Trades taken on News :",count2)
print("News Trades that were flipped from a win :",count3)
print("News Trades that weren't flipped :", count2-count3)

#end of program
print('\n------------------------end-----------------------------------')

#time of end of program
end_time=datetime.now()
print(end_time)

#plotting RR distribution
counter = Counter(rr_distribution)
most_common_rr = counter.most_common(1)
for rr_val,count in most_common_rr:
        plt.text(rr_val,1.05,f'Most Common RR: {round(rr_val,2)}',horizontalalignment='center',color='black',
                 fontsize=8) #to print the most common RR on the 3rd graph
        
rr_distribution = np.array(rr_distribution).flatten()
        
mean_rr = np.mean(rr_distribution)
r0_curve = np.percentile(rr_distribution,0)
r5_curve = np.percentile(rr_distribution,5)
r95_curve = np.percentile(rr_distribution,95)
r100_curve = np.percentile(rr_distribution,100)

        
plt.figure(figsize=(12,6))

kde=gaussian_kde(rr_distribution)
x_val=np.linspace(rr_distribution.min(),rr_distribution.max(),1000)
y_val=kde(x_val)

plt.plot(x_val,y_val,color='black')
mask1=(x_val >= r0_curve) & (x_val <= r5_curve)
mask2=(x_val >= r5_curve) & (x_val <= r95_curve)
mask3=(x_val >= r95_curve) & (x_val <= r100_curve)

plt.fill_between(x_val[mask1],y_val[mask1],alpha=0.3,color='red')
plt.fill_between(x_val[mask2],y_val[mask2],alpha=0.3,color='green')
plt.fill_between(x_val[mask3],y_val[mask3],alpha=0.3,color='red')


'''sns.stripplot(x=rr_distribution,jitter=0.25,alpha=0.6,color='blue') #-- use to see a jitter graph and add news RR'''

plt.axvline(mean_rr,color='black',linestyle='--',label=f'Mean RR: {round(mean_rr,2)}')

plt.xlabel("Risk:Reward Ratio")
plt.title("RRR Distribution")
plt.legend()
plt.show()

#to display the graph
plt.xlabel("Trade Number")
plt.ylabel("Account Size")
plt.title("Monte Carlo Equity Curves with Percentiles")
plt.legend()
plt.show()