import json, sys
from datetime import datetime

def update_database(new_db):
    with open('db.json', 'w') as file:
        json.dump(new_db, file, indent=4)

def log_transaction(db, amt, sender, receiver):
    transaction = {
        "amount": amt,
        "sender": sender,
        "receiver": receiver,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Fetch sender's and receiver's accounts
    sender_accounts = db["users"].get(sender, {}).get("accounts", {})
    receiver_accounts = db["users"].get(receiver, {}).get("accounts", {})

    # Assuming you want to pick the first account available
    sender_first_account = next(iter(sender_accounts.values()), None)
    receiver_first_account = next(iter(receiver_accounts.values()), None)

    # Check if both accounts are available
    if sender_first_account is None:
        print(f"Error: Sender {sender} has no accounts.")
        return db
    if receiver_first_account is None:
        print(f"Error: Receiver {receiver} has no accounts.")
        return db

   # Generate a unique transaction ID using the current timestamp
    transaction_id = f"tx_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    # Append the transaction to both sender's and receiver's history
    sender_first_account.setdefault("history", {})[transaction_id] = transaction
    receiver_first_account.setdefault("history", {})[transaction_id] = transaction

    return db

def transferBetweenAccounts(amt, tx, rx):
    """Transfer amount between two accounts."""
    try:
        amt = float(amt)  # Convert amount to float
    except ValueError:
        print("Invalid amount. Please enter a numerical value.")
        return
    
    if amt <= 0:
        print("Amount must be greater than zero.")
        return

    db = load_database()  # Load the database
    if tx not in db["users"] or rx not in db["users"]:
        print("Invalid sender or receiver.")
        return
    
    user_tx = db["users"][tx]
    user_rx = db["users"][rx]

    # Assuming there's only one account per user for simplicity
    tx_account = list(user_tx["accounts"].values())[0]
    rx_account = list(user_rx["accounts"].values())[0]

    if tx_account["balance"] < amt:
        print("Insufficient funds.")
        return

    # Perform the transfer
    tx_account["balance"] -= amt
    rx_account["balance"] += amt

    db = log_transaction(db, amt, tx, rx)

    # Save the updated database
    update_database(db)

    print(f"Transferred ${amt} from {tx} to {rx} successfully.")

quit_state = -1
run_state = 0
user_state = 1

def action_menu(user):
    option = input("Which action would you like to perform?\n")
    if option == "quit":
        return quit_state  

    if option == "logout":
        return run_state   

    if option == "transfer":
        amt = input("How mouch would you like to transfer?\n")
        rx = input("Who do you want to send it to?\n")
        transferBetweenAccounts(amt, user['username'], rx)
    return user_state
    
def display_user(user):
    """Display user information."""
    print(f"User: {user['username']}")

    print("Accounts:")
    for (accountName, accountData) in get_user_elev(user['username'])['accounts'].items():
        print(f"\t{accountName}")
        print(f"\t\tBalance: {accountData['balance']}\n")


def load_database(filename='db.json'):
    """Load the user database from a file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Database file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error decoding the database file.")
        sys.exit(1)

def get_user_elev(user):
    users = load_database()["users"]
    if user not in users:
        print("DB ERROR")
        return -1
    return users[user]

def log_failed_attempt(user):
    db = load_database()
    
    user_data = db["users"].setdefault(user.get('username') , {})

    login_attempts = user_data.setdefault("login_attempts", {})
    
    attempt_key = len(login_attempts)
    
    login_attempts[attempt_key] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    update_database(db)                                                                                                                                                                                                                                                                                                   

def get_user(username, password):
    users = load_database()["users"]
    # check if user exists
    if username not in users:
        return -1
    
    user = users[username]
    login_attempts = user.get("login_attempts", [])

    # check user login attempts
    if len(login_attempts) >= 3:
        # Convert the dictionary values to datetime objects
        attempt_times = [datetime.strptime(attempt, "%Y-%m-%d %H:%M:%S") for attempt in login_attempts.values()]
        
        # Get the latest attempt time
        last_attempt_time = attempt_times[-1]
        current_time = datetime.now()
        
        # Check if a minute has passed since the last attempt
        if (current_time - last_attempt_time).total_seconds() < 20 * max(3, len(login_attempts)):
            return -2
        

    # check if password is correct
    if password != user["password"]:
        log_failed_attempt(user)
        return -1
    return user

def login_handling():
    """Handle user login."""
    while True:
        usrnm_attempt = input("What is your username?\n>")
        passwd_attempt = input("What is your password?\n>")

        if not usrnm_attempt or not passwd_attempt:
            print("Please enter text for both username and password\n")
            continue

        user = get_user(usrnm_attempt, passwd_attempt)

        if (type(user) is not int):
            print("Login successful!\n")
            return user
        else:
            if user == -1:
                print("Username or password is incorrect!\n")
            if user == -2:
                print("Too many attempts try again later\n")


            

def main():
    state = run_state

    while state == run_state:
        print("Welcome to BSU-PAY: Bemidji State University's unofficial banking app!!!1!\n\n")
        input("Press enter to proceed...\n")

        # Handle user login
        current_user = login_handling()

        state = user_state

        while state == user_state:
            # Display user information
            display_user(current_user)
            # Prompt for next action
            state = action_menu(current_user)

if __name__ == "__main__":
    main()
