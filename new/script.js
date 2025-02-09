document.addEventListener('DOMContentLoaded', () => {
    const accountNumber = prompt('Enter your account number:');
    const pin = prompt('Enter your PIN:');

    // Simulate backend verification
    if (accountNumber !== '123456' || pin !== '1234') {
        alert('Invalid account number or PIN');
        document.body.innerHTML = '<h1>Access Denied</h1>';
        return;
    }

    // Initial load
    showScreen('menu');
});

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.add('hidden');
    });
    document.getElementById(screenId).classList.remove('hidden');
}

function checkBalance() {
    // Simulate backend check
    const balance = 5000.0; // Replace with actual backend call
    document.getElementById('balance-amount').innerText = `Your balance is $${balance}`;
    showScreen('balance');
}

function withdraw() {
    const amount = parseFloat(document.getElementById('withdraw-amount').value);
    // Simulate backend withdraw
    alert(`Withdrew $${amount}`);
    showScreen('menu');
}

function deposit() {
    const amount = parseFloat(document.getElementById('deposit-amount').value);
    // Simulate backend deposit
    alert(`Deposited $${amount}`);
    showScreen('menu');
}

function viewStatements() {
    // Simulate backend fetch
    const statements = [
        { type: 'deposit', amount: 1000, date: '2025-01-01 12:00:00' },
        { type: 'withdraw', amount: 500, date: '2025-01-02 14:00:00' }
    ]; // Replace with actual backend call
    const statementsList = document.getElementById('statements-list');
    statementsList.innerHTML = '';
    statements.forEach(statement => {
        const li = document.createElement('li');
        li.innerText = `${statement.date}: ${statement.type} $${statement.amount}`;
        statementsList.appendChild(li);
    });
    showScreen('statements');
}

function transfer() {
    const amount = parseFloat(document.getElementById('transfer-amount').value);
    const toAccount = document.getElementById('transfer-to').value;
    // Simulate backend transfer
    alert(`Transferred $${amount} to account ${toAccount}`);
    showScreen('menu');
}

function exit() {
    alert('Thank you for using our ATM!');
    document.body.innerHTML = '<h1>Session Ended</h1>';
}