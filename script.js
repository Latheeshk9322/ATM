document.addEventListener("DOMContentLoaded", function () {
    function login() {
        let accountNumber = document.getElementById("accountNumber").value;
        
        if (!accountNumber) {
            document.getElementById("loginMessage").innerText = "Please enter an account number.";
            return;
        }
        
        console.log("Attempting login with account number:", accountNumber);

        fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number: parseInt(accountNumber) })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Login response data:", data);
            if (data.message) {
                document.querySelector(".login-container").style.display = "none";
                document.querySelector(".dashboard").style.display = "block";
                document.getElementById("responseMessage").innerText = "Login successful!";
                sessionStorage.setItem("accountNumber", accountNumber);
            } else {
                document.getElementById("loginMessage").innerText = data.error;
            }
        })
        .catch(error => console.error("Error during login:", error));
    }
    
    function checkBalance() {
        let accountNumber = sessionStorage.getItem("accountNumber");
        fetch("http://127.0.0.1:5000/balance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number: parseInt(accountNumber) })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseMessage").innerText = "Balance: $" + data.balance;
        })
        .catch(error => console.error("Error fetching balance:", error));
    }
    
    function withdraw() {
        let accountNumber = sessionStorage.getItem("accountNumber");
        let amount = prompt("Enter withdrawal amount:");
        fetch("http://127.0.0.1:5000/withdraw", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number: parseInt(accountNumber), amount: parseFloat(amount) })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseMessage").innerText = data.message || data.error;
        })
        .catch(error => console.error("Error withdrawing money:", error));
    }
    
    function deposit() {
        let accountNumber = sessionStorage.getItem("accountNumber");
        let amount = prompt("Enter deposit amount:");
        fetch("http://127.0.0.1:5000/deposit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number: parseInt(accountNumber), amount: parseFloat(amount) })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseMessage").innerText = data.message || data.error;
        })
        .catch(error => console.error("Error depositing money:", error));
    }
    
    function viewTransactions() {
        let accountNumber = sessionStorage.getItem("accountNumber");
        fetch("http://127.0.0.1:5000/transactions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number: parseInt(accountNumber) })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("responseMessage").innerText = "Transactions: " + data.transactions;
        })
        .catch(error => console.error("Error fetching transactions:", error));
    }
    
    window.login = login;
    window.checkBalance = checkBalance;
    window.withdraw = withdraw;
    window.deposit = deposit;
    window.viewTransactions = viewTransactions;
});
