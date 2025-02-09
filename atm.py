import pandas as pd

# Load the database (CSV file) into a Pandas DataFrame
def load_database(file_name):
    """
    Loads the CSV file into a Pandas DataFrame.
    Replaces NaN values in the 'Transactions' column with an empty string.
    Ensures the 'Balance' column is numeric.
    """
    try:
        df = pd.read_csv(file_name)
        df['Transactions'] = df['Transactions'].fillna("")  # Replace NaN with empty strings
        
        # Ensure the 'Balance' column is numeric
        if not pd.api.types.is_numeric_dtype(df['Balance']):
            print("Warning: Converting 'Balance' column to numeric type.")
            df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')  # Convert to numeric, invalid values become NaN
            df['Balance'] = df['Balance'].fillna(0.0)  # Replace NaN with 0.0
        
        print("Database loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None

# Save the updated DataFrame back to the CSV file
def save_database(df, file_name):
    """
    Saves the updated DataFrame back to the CSV file.
    """
    try:
        df.to_csv(file_name, index=False)
        print("Database saved successfully.")
    except Exception as e:
        print(f"Error saving database: {e}")

# Find account details by account number
def find_account(df, account_number):
    """
    Finds the account index in the DataFrame based on the account number.
    Returns the row index if found, otherwise returns None.
    """
    account = df[df['Account Number'] == account_number]
    return None if account.empty else account.index[0]

# Display account balance
def display_balance(df, account_index):
    """
    Displays the current balance of the account.
    """
    balance = df.loc[account_index, 'Balance']
    print(f"Your current balance is: ${balance:.2f}")

# Withdraw money from the account
def withdraw(df, account_index, amount):
    """
    Withdraws money from the account if sufficient funds are available.
    Updates the balance and transaction history.
    """
    balance = df.loc[account_index, 'Balance']
    if amount > balance:
        print("Insufficient funds!")
        return False
    df.loc[account_index, 'Balance'] -= amount
    transactions = df.loc[account_index, 'Transactions'] or ""
    transactions += f"Withdrawal: -${amount:.2f}, "
    df.loc[account_index, 'Transactions'] = transactions
    print(f"${amount:.2f} withdrawn successfully.")
    return True

# Deposit money into the account
def deposit(df, account_index, amount):
    """
    Deposits money into the account.
    Updates the balance and transaction history.
    """
    df.loc[account_index, 'Balance'] += amount
    transactions = df.loc[account_index, 'Transactions'] or ""
    transactions += f"Deposit: +${amount:.2f}, "
    df.loc[account_index, 'Transactions'] = transactions
    print(f"${amount:.2f} deposited successfully.")

# View transaction history
def view_statements(df, account_index):
    """
    Displays the transaction history of the account.
    """
    transactions = df.loc[account_index, 'Transactions']
    if transactions:
        print("Transaction History:")
        print(transactions)
    else:
        print("No transactions recorded yet.")

# Transfer money to another account
def transfer_money(df, sender_index, receiver_account_number, amount):
    """
    Transfers money from one account to another if sufficient funds are available.
    Updates both accounts' balances and transaction histories.
    """
    # Check sender's balance
    sender_balance = df.loc[sender_index, 'Balance']
    if amount > sender_balance:
        print("Insufficient funds for transfer!")
        return False
    
    # Find the receiver's account
    receiver_index = find_account(df, receiver_account_number)
    if receiver_index is None:
        print("Receiver account not found!")
        return False
    
    # Update sender's account
    df.loc[sender_index, 'Balance'] -= amount  # Deduct amount from sender's balance
    sender_transactions = df.loc[sender_index, 'Transactions'] or ""
    sender_transactions += f"Transfer to Account {receiver_account_number}: -${amount:.2f}, "
    df.loc[sender_index, 'Transactions'] = sender_transactions
    
    # Update receiver's account
    df.loc[receiver_index, 'Balance'] += amount  # Add amount to receiver's balance
    receiver_transactions = df.loc[receiver_index, 'Transactions'] or ""
    receiver_transactions += f"Transfer from Account {df.loc[sender_index, 'Account Number']}: +${amount:.2f}, "
    df.loc[receiver_index, 'Transactions'] = receiver_transactions
    
    print(f"${amount:.2f} transferred successfully to Account {receiver_account_number}.")
    return True

# Main function to handle user interaction
def main():
    file_name = "bank_database.csv"  # Define the file name here
    df = load_database(file_name)
    if df is None:
        return
    
    # Input account number
    try:
        account_number = int(input("Enter your account number: "))
        account_index = find_account(df, account_number)
        if account_index is None:
            print("Account not found!")
            return
    except ValueError:
        print("Invalid account number. Please enter a numeric value.")
        return
    
    print("\nWelcome to the ATM!")
    while True:
        print("\nChoose an option:")
        print("1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. View Statements")
        print("5. Transfer Money to Another Account")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        
        # Dynamically retrieve the account index to ensure it's up-to-date
        account_index = find_account(df, account_number)
        
        if choice == "1":
            display_balance(df, account_index)
        elif choice == "2":
            try:
                amount = float(input("Enter the amount to withdraw: "))
                if amount <= 0:
                    print("Invalid amount! Please enter a positive number.")
                else:
                    withdraw(df, account_index, amount)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "3":
            try:
                amount = float(input("Enter the amount to deposit: "))
                if amount <= 0:
                    print("Invalid amount! Please enter a positive number.")
                else:
                    deposit(df, account_index, amount)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            view_statements(df, account_index)
        elif choice == "5":
            try:
                receiver_account_number = int(input("Enter the receiver's account number: "))
                amount = float(input("Enter the amount to transfer: "))
                if amount <= 0:
                    print("Invalid amount! Please enter a positive number.")
                else:
                    transfer_money(df, account_index, receiver_account_number, amount)
            except ValueError:
                print("Please enter valid numbers for the account and amount.")
        elif choice == "6":
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Save changes to the database before exiting
    save_database(df, file_name)

if __name__ == "__main__":
    main()


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.linear_model import LinearRegression

# # Load the database (CSV file) into a Pandas DataFrame
# def load_database(file_name):
#     """
#     Loads the CSV file into a Pandas DataFrame.
#     Replaces NaN values in the 'Transactions' column with an empty string.
#     """
#     try:
#         df = pd.read_csv(file_name)
#         df['Transactions'] = df['Transactions'].fillna("")  # Replace NaN with empty strings
#         print("Database loaded successfully.")
#         return df
#     except FileNotFoundError:
#         print(f"Error: File '{file_name}' not found.")
#         return None

# # Save the updated DataFrame back to the CSV file
# def save_database(df, file_name):
#     """
#     Saves the updated DataFrame back to the CSV file.
#     """
#     try:
#         df.to_csv(file_name, index=False)
#         print("Database saved successfully.")
#     except Exception as e:
#         print(f"Error saving database: {e}")

# # Find account details by account number
# def find_account(df, account_number):
#     """
#     Finds the account index in the DataFrame based on the account number.
#     Returns the row index if found, otherwise returns None.
#     """
#     account = df[df['Account Number'] == account_number]
#     return None if account.empty else account.index[0]

# # Display account balance
# def display_balance(df, account_index):
#     """
#     Displays the current balance of the account.
#     """
#     balance = df.loc[account_index, 'Balance']
#     print(f"Your current balance is: ${balance:.2f}")

# # Withdraw money from the account
# def withdraw(df, account_index, amount):
#     """
#     Withdraws money from the account if sufficient funds are available.
#     Updates the balance and transaction history.
#     """
#     balance = df.loc[account_index, 'Balance']
#     if amount > balance:
#         print("Insufficient funds!")
#         return False

#     df.loc[account_index, 'Balance'] -= amount
#     transactions = df.loc[account_index, 'Transactions'] or ""
#     transactions += f"Withdrawal: -${amount:.2f}, "
#     df.loc[account_index, 'Transactions'] = transactions
#     print(f"${amount:.2f} withdrawn successfully.")
#     return True

# # Deposit money into the account
# def deposit(df, account_index, amount):
#     """
#     Deposits money into the account.
#     Updates the balance and transaction history.
#     """
#     df.loc[account_index, 'Balance'] += amount
#     transactions = df.loc[account_index, 'Transactions'] or ""
#     transactions += f"Deposit: +${amount:.2f}, "
#     df.loc[account_index, 'Transactions'] = transactions
#     print(f"${amount:.2f} deposited successfully.")

# # View transaction history
# def view_statements(df, account_index):
#     """
#     Displays the transaction history of the account.
#     """
#     transactions = df.loc[account_index, 'Transactions']
#     if transactions:
#         print("Transaction History:")
#         print(transactions)
#     else:
#         print("No transactions recorded yet.")

# # Analyze and visualize transaction data
# def analyze_transactions(df, account_index):
#     """
#     Analyzes transaction data and provides statistics.
#     Visualizes the transaction amounts over time.
#     """
#     transactions = df.loc[account_index, 'Transactions']
#     if not transactions:
#         print("No transactions to analyze.")
#         return

#     # Extract transaction amounts
#     amounts = []
#     for entry in transactions.split(","):
#         if "Withdrawal" in entry:
#             amounts.append(-float(entry.split("-$")[1]))
#         elif "Deposit" in entry:
#             amounts.append(float(entry.split("+$")[1]))

#     amounts = np.array(amounts)

#     # Basic statistics
#     print(f"Total Transactions: {len(amounts)}")
#     print(f"Average Transaction Amount: ${np.mean(amounts):.2f}")
#     print(f"Maximum Transaction Amount: ${np.max(amounts):.2f}")
#     print(f"Minimum Transaction Amount: ${np.min(amounts):.2f}")

#     # Plot transaction history
#     plt.figure(figsize=(10, 5))
#     sns.lineplot(x=range(1, len(amounts) + 1), y=amounts, marker='o')
#     plt.title("Transaction History")
#     plt.xlabel("Transaction Index")
#     plt.ylabel("Amount ($)")
#     plt.grid()
#     plt.show()

# # Predict future balance using Scikit-learn
# def predict_future_balance(df, account_index):
#     """
#     Predicts the future balance using linear regression.
#     Visualizes actual vs. predicted balances.
#     """
#     transactions = df.loc[account_index, 'Transactions']
#     if not transactions:
#         print("No transactions to predict future balance.")
#         return

#     # Extract transaction amounts
#     amounts = []
#     for entry in transactions.split(","):
#         if "Withdrawal" in entry:
#             amounts.append(-float(entry.split("-$")[1]))
#         elif "Deposit" in entry:
#             amounts.append(float(entry.split("+$")[1]))

#     cumulative_balances = np.cumsum(amounts)

#     # Prepare data for regression
#     X = np.arange(len(cumulative_balances)).reshape(-1, 1)
#     y = cumulative_balances

#     # Train a linear regression model
#     model = LinearRegression()
#     model.fit(X, y)

#     # Predict future balance
#     future_steps = 5  # Predict next 5 transactions
#     future_X = np.arange(len(cumulative_balances), len(cumulative_balances) + future_steps).reshape(-1, 1)
#     future_y = model.predict(future_X)

#     # Plot predictions
#     plt.figure(figsize=(10, 5))
#     sns.lineplot(x=range(len(cumulative_balances)), y=cumulative_balances, label="Actual Balance", marker='o')
#     sns.lineplot(x=future_X.flatten(), y=future_y, label="Predicted Balance", linestyle="--", marker='x')
#     plt.title("Future Balance Prediction")
#     plt.xlabel("Transaction Index")
#     plt.ylabel("Balance ($)")
#     plt.legend()
#     plt.grid()
#     plt.show()

# # Main function to handle user interaction
# def main():
#     file_name = "bank_database.csv"  # Define the file name here
#     df = load_database(file_name)
#     if df is None:
#         return

#     # Input account number
#     try:
#         account_number = int(input("Enter your account number: "))
#         account_index = find_account(df, account_number)
#         if account_index is None:
#             print("Account not found!")
#             return
#     except ValueError:
#         print("Invalid account number. Please enter a numeric value.")
#         return

#     print("\nWelcome to the ATM!")
#     while True:
#         print("\nChoose an option:")
#         print("1. Check Balance")
#         print("2. Withdraw Money")
#         print("3. Deposit Money")
#         print("4. View Statements")
#         print("5. Analyze Transactions")
#         print("6. Predict Future Balance")
#         print("7. Exit")
#         choice = input("Enter your choice (1-7): ")

#         if choice == "1":
#             display_balance(df, account_index)
#         elif choice == "2":
#             try:
#                 amount = float(input("Enter the amount to withdraw: "))
#                 if amount <= 0:
#                     print("Invalid amount! Please enter a positive number.")
#                 else:
#                     withdraw(df, account_index, amount)
#             except ValueError:
#                 print("Please enter a valid number.")
#         elif choice == "3":
#             try:
#                 amount = float(input("Enter the amount to deposit: "))
#                 if amount <= 0:
#                     print("Invalid amount! Please enter a positive number.")
#                 else:
#                     deposit(df, account_index, amount)
#             except ValueError:
#                 print("Please enter a valid number.")
#         elif choice == "4":
#             view_statements(df, account_index)
#         elif choice == "5":
#             analyze_transactions(df, account_index)
#         elif choice == "6":
#             predict_future_balance(df, account_index)
#         elif choice == "7":
#             print("Thank you for using the ATM. Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")

#     # Save changes to the database before exiting
#     save_database(df, file_name)

# if __name__ == "__main__":
#     main()