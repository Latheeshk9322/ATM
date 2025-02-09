import pandas as pd

# Load the database (CSV file) into a Pandas DataFrame
def load_database(file_name):
    """
    Loads the CSV file into a Pandas DataFrame.
    Ensures the 'Balance' column is numeric and replaces NaN values.
    """
    try:
        df = pd.read_csv(file_name)
        df['Transactions'] = df['Transactions'].fillna("")  # Replace NaN with empty strings
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce').fillna(0.0)  # Ensure numeric balance
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
    """
    balance = df.loc[account_index, 'Balance']
    if amount > balance:
        print("Insufficient funds!")
        return False
    df.loc[account_index, 'Balance'] -= amount
    df.loc[account_index, 'Transactions'] += f"Withdrawal: -${amount:.2f}, "
    print(f"${amount:.2f} withdrawn successfully.")
    return True

# Deposit money into the account
def deposit(df, account_index, amount):
    """
    Deposits money into the account.
    """
    df.loc[account_index, 'Balance'] += amount
    df.loc[account_index, 'Transactions'] += f"Deposit: +${amount:.2f}, "
    print(f"${amount:.2f} deposited successfully.")

# View transaction history
def view_statements(df, account_index):
    """
    Displays the transaction history of the account.
    """
    transactions = df.loc[account_index, 'Transactions']
    print("Transaction History:" if transactions else "No transactions recorded yet.")
    print(transactions)

# Transfer money to another account
def transfer_money(df, sender_index, receiver_account_number, amount):
    """
    Transfers money from one account to another if sufficient funds are available.
    """
    df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce').fillna(0.0)  # Ensure numeric balances
    
    sender_balance = df.loc[sender_index, 'Balance']
    if amount > sender_balance:
        print("Insufficient funds for transfer!")
        return False
    
    receiver_index = find_account(df, receiver_account_number)
    if receiver_index is None:
        print("Receiver account not found!")
        return False
    
    df.loc[sender_index, 'Balance'] -= amount  # Deduct from sender
    df.loc[sender_index, 'Transactions'] += f"Transfer to {receiver_account_number}: -${amount:.2f}, "
    
    df.loc[receiver_index, 'Balance'] += amount  # Add to receiver
    df.loc[receiver_index, 'Transactions'] += f"Transfer from {df.loc[sender_index, 'Account Number']}: +${amount:.2f}, "
    
    print(f"${amount:.2f} transferred successfully to Account {receiver_account_number}.")
    return True

# Main function to handle user interaction
def main():
    file_name = "bank_database.csv"
    df = load_database(file_name)
    if df is None:
        return
    
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
        print("5. Transfer Money")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        
        account_index = find_account(df, account_number)
        
        if choice == "1":
            display_balance(df, account_index)
        elif choice == "2":
            amount = float(input("Enter the amount to withdraw: "))
            withdraw(df, account_index, amount)
        elif choice == "3":
            amount = float(input("Enter the amount to deposit: "))
            deposit(df, account_index, amount)
        elif choice == "4":
            view_statements(df, account_index)
        elif choice == "5":
            receiver_account_number = int(input("Enter receiver's account number: "))
            amount = float(input("Enter amount to transfer: "))
            transfer_money(df, account_index, receiver_account_number, amount)
        elif choice == "6":
            print("Thank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
    save_database(df, file_name)

if __name__ == "__main__":
    main()
