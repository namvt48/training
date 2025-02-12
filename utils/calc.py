# Input information
account_balance = 500  # Account balance (USD)
risk_percentage = 0.02  # Maximum risk percentage (2%)
leverage = 10  # Leverage (x10)
entry_price = 100000  # Entry price (USD)
stoploss_price = 95000  # Stoploss price (USD)
take_profit_price = 110000  # Take Profit price (USD)

# Step 1: Calculate the risk amount per trade
risk_amount = account_balance * risk_percentage
print(risk_amount)

# Step 2: Calculate the stoploss distance
stoploss_distance = abs(entry_price - stoploss_price)

# Step 3: Calculate the position size in contracts (units)
position_size_contracts = risk_amount / stoploss_distance

# Step 4: Calculate expected profit if Take Profit is reached
expected_profit = position_size_contracts * (take_profit_price - entry_price)

# Step 5: Calculate the loss amount if Stoploss is hit
loss_amount = position_size_contracts * (entry_price - stoploss_price)

# Output results
print(f"Position Size (Contracts): {position_size_contracts:.2f}")
print(f"Expected Profit (if TP is reached): {expected_profit:.2f} USD")
print(f"Loss Amount (if SL is hit): {loss_amount:.2f} USD")
