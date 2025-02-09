from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
FILE_NAME = "bank_database.csv"

def load_database():
    try:
        df = pd.read_csv(FILE_NAME)
        df['Transactions'] = df['Transactions'].fillna("")
        df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce').fillna(0.0)
        return df
    except FileNotFoundError:
        return None

def save_database(df):
    df.to_csv(FILE_NAME, index=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    account_number = data.get("account_number")
    df = load_database()
    if df is None:
        return jsonify({"error": "Database not found"}), 500
    account = df[df['Account Number'] == account_number]
    if account.empty:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": "Login successful"})

@app.route('/balance', methods=['POST'])
def get_balance():
    data = request.json
    account_number = data.get("account_number")
    df = load_database()
    account = df[df['Account Number'] == account_number]
    if account.empty:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"balance": account.iloc[0]['Balance']})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    account_number = data.get("account_number")
    amount = float(data.get("amount"))
    df = load_database()
    index = df[df['Account Number'] == account_number].index
    if index.empty:
        return jsonify({"error": "Account not found"}), 404
    if df.loc[index[0], 'Balance'] < amount:
        return jsonify({"error": "Insufficient funds"}), 400
    df.loc[index[0], 'Balance'] -= amount
    df.loc[index[0], 'Transactions'] += f"Withdrawal: -${amount:.2f}, "
    save_database(df)
    return jsonify({"message": "Withdrawal successful", "balance": df.loc[index[0], 'Balance']})

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    account_number = data.get("account_number")
    amount = float(data.get("amount"))
    df = load_database()
    index = df[df['Account Number'] == account_number].index
    if index.empty:
        return jsonify({"error": "Account not found"}), 404
    df.loc[index[0], 'Balance'] += amount
    df.loc[index[0], 'Transactions'] += f"Deposit: +${amount:.2f}, "
    save_database(df)
    return jsonify({"message": "Deposit successful", "balance": df.loc[index[0], 'Balance']})

@app.route('/transactions', methods=['POST'])
def transactions():
    data = request.json
    account_number = data.get("account_number")
    df = load_database()
    account = df[df['Account Number'] == account_number]
    if account.empty:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"transactions": account.iloc[0]['Transactions']})

if __name__ == '__main__':
    app.run(debug=True)
