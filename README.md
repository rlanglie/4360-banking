User Guide:
    Run the program using
        python banking.py 
    or 
        python3 banking.py 
    depending on your python installation
    
    Generally, proceed by following the on-screen prompts
    The program starts with a login screen that will prompt you with a username and password
    After successfully logging in, you may view the balance of your main account

    You may choose to either, transfer, deposit, withdraw, logout, or quit depending 
        on which command you enter followed with a press of the enter key
    Again, following the on-screen prompts will allow you to perform any of the provided commands with ease
    All on-screen prompts must be followed by a press of the enter key to proceed and to input data 

    There are only 2 accounts
        Username: default
        Password: password

        and

        Username: justin
        Password: cox

    You may transfer money from one account to the other using the transfer command
    All users are referred to by their username for use in the transfer command
    A transaction history of either account may be viewed in the db.json database

Program Planning:   
    Functional Requirements:
        The system must handle user login
        The system must alllow the user the view their balance
        The system must allow users to transfer parts of their balance to other users
        The sytem must allow users to deposit and withdraw balance
        The system must allow for multiple consequitive user commands
    Non-Functional Requirements:
        The system must be easily understandable and foolproof
        The system must be resposnive
    Design Constraints:
        The system is limited security-wise by the database and user-access-terminal occuring on the same system
        The programmer is limited by the short development deadline