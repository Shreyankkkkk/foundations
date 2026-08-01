# Project 2 - Build a Budget App 
'''
Build a Budget App
In this lab, you will build a simple budget app that tracks spending in different categories and can show the relative spending percentage on a graph.

Objective: Fulfill the user stories below and get all the tests to pass to complete the lab.

User Stories:

You should have a Category class that accepts a name as the argument.

The Category class should have an instance attribute ledger that is a list, and contains the list of transactions.

The Category class should have the following methods:

A deposit method that accepts an amount and an optional description. If no description is given, it should default to an empty string. The method should append an object to the ledger list in the form of {'amount': amount, 'description': description}.
A withdraw method that accepts an amount and an optional description (default to an empty string). The method should store in ledger the amount passed in as a negative number, and should return True if the withdrawal succeeded and False otherwise.
A get_balance method that returns the current category balance based on ledger.
A transfer method that accepts an amount and another Category instance, withdraws the amount with description Transfer to [Destination], deposits it into the other category with description Transfer from [Source], where [Destination] and [Source] should be replaced by the name of destination and source categories. The method should return True when the transfer is successful, and False otherwise.
A check_funds method that accepts an amount and returns False if it exceeds the balance or True otherwise. This method must be used by both the withdraw and transfer methods.
When a Category object is printed, it should:

Display a title line of 30 characters with the category name centered between * characters.
List each ledger entry with up to 23 characters of its description left-aligned and the amount right-aligned (two decimal places, max 7 characters).
Show a final line Total: [balance], where [balance] should be replaced by the category total.
Here is an example usage:

food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)
And here is an example of the output:

*************Food*************
initial deposit        1000.00
groceries               -10.15
restaurant and more foo -15.89
Transfer to Clothing    -50.00
Total: 923.96
You should have a function outside the Category class named create_spend_chart(categories) that takes a list of categories and returns a bar-chart string. To build the chart:

Start with the title Percentage spent by category.
Calculate percentages from withdrawals only and not from deposits. The percentage should be the percentage of the amount spent for each category to the total spent for all categories (rounded down to the nearest 10).
Label the y-axis from 100 down to 0 in steps of 10.
Use o characters for the bars.
Include a horizontal line two spaces past the last bar.
Write category names vertically below the bar.
This function will be tested with up to four categories.

Make sure to match the spacing of the example output exactly:

Percentage spent by category
100|          
 90|          
 80|          
 70|          
 60| o        
 50| o        
 40| o        
 30| o        
 20| o  o     
 10| o  o  o  
  0| o  o  o  
    ----------
     F  C  A  
     o  l  u  
     o  o  t  
     d  t  o  
        h     
        i     
        n     
        g     
NOTE: open the browser console with F12 to see a more verbose output of the tests.
'''

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description = ''):
        transaction = {
            'amount' : amount,
            'description' : description
        }
        self.ledger.append(transaction)

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            transaction = {
                'amount' : -amount,
                'description' : description
            }
            self.ledger.append(transaction)
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for value in self.ledger:
            balance += value['amount']
        return balance
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            if self.withdraw(amount, f"Transfer to {category.name}"):
                category.deposit(amount, f"Transfer from {self.name}")
                return True
        return False
    
    def check_funds(self, amount):
        if self.get_balance() - amount >= 0:
            return True
        else:
            return False
        
    def __str__(self):
        temp_number = 0
        output = ''
        if (30 - len(self.name)) % 2 == 0:
            temp_number = int((30 - len(self.name)) / 2)
            string_start = "*" * temp_number
            string_end = "*" * temp_number
            output += string_start + self.name + string_end + "\n"
        else:
            temp_number = int((30 - len(self.name)) / 2)
            string_start = "*" * (temp_number)
            string_end = "*" * (temp_number + 1)
            output += string_start + self.name + string_end + "\n"

        for transaction in self.ledger:
            description = transaction['description'][:23]
            amount = f"{transaction['amount']:.2f}"
            amount = amount[:7]
            space = 30 - len(description) - len(amount)
            output += description + ' ' * space + amount + "\n"
            
        output += f"Total: {self.get_balance():.2f}"
        return output

categories = []

food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
#print(food)
categories.append(food)
categories.append(clothing)

def create_spend_chart(categories : list):
    output = "Percentage spent by category\n"

    spent = []
    total_spent = 0
    for category in categories:
        category_spent = 0
        for transaction in category.ledger:
            if transaction['amount'] < 0:
                category_spent += abs(transaction['amount'])
        spent.append(category_spent)
        total_spent += category_spent
    
    if total_spent == 0:
        raise ZeroDivisionError("The total spendings were 0.")
    
    percentages = []
    for amount in spent:
        percentage = int((amount / total_spent) * 100)
        percentage = percentage - (percentage % 10)
        percentages.append(percentage)

    for number in range(100, -1, -10):
        output += f"{number:>3}|"
        for percentage in percentages:
            if percentage >= number:
                output += ' o '
            else:
                output += '   '
        output += ' \n'
    
    output += "    " + "-" * (len(categories) * 3 + 1) + "\n" 
    
    max_length = 0
    for value in categories:
        if len(value.name) > max_length:
            max_length = len(value.name)
    for index in range(max_length):
        output += '     '
        for category in categories:
            if index < len(category.name):
                output += category.name[index] + '  '
            else:
                output += '   '
        output += '\n'
    
    return output.rstrip("\n")

#print(create_spend_chart(categories))
