# Write code that analyzes data to take date as input and return the price for past and future estiamtes

#------------------------OVERVIEW------------------------#
'''
Here is the background information on your task
You are a quantitative researcher working with a commodity trading desk. 
Alex, a VP on the desk, wants to start trading natural gas storage contracts. 
However, the available market data must be of higher quality to enable the instrument to be priced accurately. 
They have sent you an email asking you to help extrapolate the data available from external feeds to provide more granularity, 
considering seasonal trends in the price as it relates to months in the year. 
To price the contract, we will need historical data and an estimate of the future gas price at any date.

Commodity storage contracts represent deals between warehouse (storage) owners and participants in the supply chain (refineries, transporters, distributors, etc.). 
The deal is typically an agreement to store an agreed quantity of any physical commodity (oil, natural gas, agriculture) in a warehouse for a specified amount of time. 
The key terms of such contracts (e.g., periodic fees for storage, limits on withdrawals/injections of a commodity) are agreed upon inception of the contract 
between the warehouse owner and the client. The injection date is when the commodity is purchased and stored, 
and the withdrawal date is when the commodity is withdrawn from storage and sold. 

A client could be anyone who would fall within the commodities supply chain, such as producers, refiners, transporters, and distributors. 
This group would also include firms (commodities trading, hedge funds, etc.) whose primary aim is to take advantage of seasonal or intra-day price 
differentials in physical commodities. For example, if a firm is looking to buy physical natural gas during summer and sell it in winter, 
it would take advantage of the seasonal price differential mentioned above. The firm would need to leverage the services of an underground storage facility 
to store the purchased inventory to realize any profits from this strategy.
'''

#----------website and information-----------#
'''
https://www.cmegroup.com/education/courses/introduction-to-energy/introduction-to-crude-oil/understanding-commodity-storage

Importance of Storage:
Balances supply and demand across the commodity supply chain.
Collects products before distribution (midstream).
Provides backup supply during disruptions (downstream).
Allows producers/traders to store commodities when prices are low and sell later at higher prices.

Crude Oil Storage:
Stored mainly in vertical cylindrical tanks.
Tank size:
Diameter: 10–400 ft
Capacity: Hundreds of barrels to 1.5 million barrels
VLCCs/ULCCs (supertankers) can store 2+ million barrels.
Floating storage is more expensive and used when supply exceeds demand.
U.S. crude inventories (2015–2024): ~400–530 million barrels.
U.S. working storage capacity: 680 million barrels (about 30% higher than 2014).

Storage Utilization & Prices:
High storage utilization:

Indicates oversupply.
Usually linked to low prices.
Often associated with contango.

Low storage utilization
Indicates tighter supply.
Usually linked to higher prices.
Often associated with backwardation.

Natural Gas Storage
Stored underground in:
Depleted reservoirs (most common)
Salt caverns
Aquifers
Mines
Hard-rock caverns
Depleted reservoirs are most cost-effective because existing infrastructure can be reused.
Base gas: Permanent gas kept in storage.
Working gas: Usable gas available for consumers.
Seasonal pattern:
Summer: Storage builds.
Winter: Storage is withdrawn to meet heating demand.
Winter prices tend to be higher, encouraging summer storage.

Electricity Storage
Large-scale storage is currently too expensive.
Electricity cannot be economically stored like oil or gas.
Prices are highly volatile due to immediate supply-demand balance.
Price swings can reach 600% in a single day.

Why Storage Matters
Reduces the impact of supply disruptions.
Ensures continuous operations for downstream users.
Helps stabilize markets.
Creates profit opportunities by storing during low-price periods and selling when prices recover.

EIA Inventory Reports
The Energy Information Administration (EIA) publishes weekly U.S. energy inventory data.
Traders closely monitor these reports because they influence energy prices.

Bullish signals:
Inventories below average.
Faster-than-normal inventory draws.

Bearish signals:
Inventories above average.
Faster-than-normal inventory builds.
Slower-than-normal inventory draws.

Report Schedule
Crude oil & petroleum inventories: Wednesday, 9:30 a.m. Central Time
Working natural gas inventories: Thursday, 9:30 a.m. Central Time
'''
#----------Data----------#
'''
Nat_Gas.csv
'''
#--------------------------Code--------------------------#

# Goal = use this monthly snapshot to produce a varying picture of the existing price data, as well as an extrapolation for an extra year

# ATTEMPT 1 - Before Pandas, MATPLOTLIB, NumPY and DateTime
# Approach: 
    # Calculate n-2 years average, predict n-1th year price
    # Calculate the error and take the average of the error
    # Predict nth year price and account for the error
    # Now get the errors and take average error, predict missing months price
    # Predict 2025 price for all months
        # Percentage erros are filtered twice for precision
import csv
try:
    with open("Nat_Gas.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

    #---------- Estimation of the price one year into the future and day prediction ----------#
        data = {}
        # Sort the data by years
        for date, price in reader:
            month, day, year = map(int, date.split("/")) # assigns each element to each split element
            price = float(price)

            if year not in data:
                data[year] = {}
            data[year][month] = price # creates a nested dictionary where {year : {month : price}}
        year = sorted(data.keys())

        # To calculate average of n-2 years and error
        def predict_year(training_years):
            prediction = {}
            for month in range(1, 13): 
                values = []
                for years in training_years:        # this block adds the value of each month into a list if the number is greater than 2
                    if month in data[years]:
                        values.append(data[years][month])
                if len(values) < 2:
                    continue
                growth = []
                for i in range(1, len(values)):
                    growth.append(values[i] / values[i - 1]) # calculates the growth of each month and adds it to a list
                avg_growth = sum(growth) / len(growth)
                prediction[month] = values[-1] * avg_growth
            return prediction
        
        # to calculate the error of the prediction
        def calculate_error(prediction, actual_year):
            errors = []
            for month in prediction:
                if month in data[actual_year]:      # checks it the month data is present in the data dict of that year
                    actual = data[actual_year][month]
                    predicted = prediction[month]
                    error = abs(actual - predicted) / actual
                    errors.append(error)
            if len(errors) == 0:
                return 0
            return sum(errors) / len(errors) # returns average error of the prediction
        
        # Estimate the price at any date in the past 
        def predict_price(date):
            month, day, year = map(int, date.split("/"))
            # to check if the input date is correct
            if month < 1 or month > 12 or day < 1 or day > 31 or year not in data:
                return None

            # to calculate the price of a day
            if month == 1:
                start = data[year - 1][12]
            else:
                start = data[year][month - 1]
            
            end = data[year][month]

            if month in [1, 3, 5, 7, 8, 10, 12]:
                days_in_month = 31
            elif month in [4, 6, 9, 11]:
                days_in_month = 30
            else:
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    days_in_month = 29
                else:
                    days_in_month = 28
            
            price = start + (end - start) * (day / days_in_month)
            return price
        
    #---------- To predict the day price of past and the future price of whole year ----------#
        # Get user input for a date and predict price of that date 
        while True:
            date = input("Enter a date (MM/DD/YYYY) to predict the price of that day : ")
            price_of_date = predict_price(date)
            if price_of_date is None:
                print("Invalid date. Please enter a valid date in the format MM/DD/YYYY.")
                continue
            else:
                print(f"Predicted price of Natural Gas on {date} is: ${price_of_date:.2f}")
                break

        # Future price prediction for 2025
        train_2023 = year[:-2]
        prediction_2023 = predict_year(train_2023)
        error_2023 = calculate_error(prediction_2023, year[-2])

        # prediction of n-1 using 0 to n-2 years
        train_2024 = year[:-1]
        prediction_2024 = predict_year(train_2024)
        error_2024 = calculate_error(prediction_2024, year[-1])

        # average errors of n-2 and n-1 prediction
        avg_error = (error_2023 + error_2024) / 2
        
        # Prediction of n+1 yearr
        prediction_n1 = predict_year(year)
        print("\n 2025 Prediction of Natural Gas Prices: \n")
        for month in range(1, 13):
            if month in prediction_n1:
                predicted_price = prediction_n1[month]
                low = predicted_price * (1 - avg_error)
                high = predicted_price * (1 + avg_error)
                print(f"Month : {month:2d} / Predicted Prices : ${predicted_price:.2f}")
                print(f" - Low Estimate : ${low:.2f} / High Estimate : ${high:.2f}\n")
        print("\nAverage Error:", round(avg_error * 100, 2), "%")

except FileNotFoundError:
    print("Error: The file 'Nat_Gas.csv' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    file.close()
