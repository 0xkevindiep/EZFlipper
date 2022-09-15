# EZ Flipper 

## Description
EZ Flipper is a program that scrapes a third party marketplace, 
[Grailed](https://www.grailed.com/), to find brand new items and compares the 
buying price to the average sale price of that same item on another reselling 
marketplace, [StockX](https://stockx.com/), to calculate the possible profit 
margins from flipping that item. The user gets to choose the minimum profit 
threshold by adjusting the variable 'min_profit' to determine which items are 
worth reselling. With millions of listings on Grailed, there's an abundance of 
hidden profitable items ready to be found and flipped. 

**DUE TO STOCKX BOT PROTECTION, THIS SCRIPT CAN ONLY BE RAN ONCE A DAY.**

## Requirements
You must have the latest verion of Google Chrome and 
Python 3.8.5 (or higher). 

When running for the first time, you may need to go to system preferences to 
allow chromedriver to run as a trusted executable.

## Instructions
1. Open up EZFlipper.py and adjust the variables 'brands', 'min_profit', 
'max_age', and 'transaction_fee' to your preference and save it. 

2. run the script: 
		python EZFlipper.py > items.txt

3. Open items.txt to find all of the profitable items with their corresponding 
links ordered by descending profit.
