email = "pytrustbankltd619@gmail.com"

def write_account_details(account_no, name, pin, sort_code, balance):
    with open(f"Account Details\\account{account_no}.txt","w", encoding="utf-8") as myfile:
        myfile.write(
        f"""
    Dear {name},

    Your account has successfully been created.

    Your Default PIN Is: {pin}
    Your Account Number Is: {account_no}
    Your Sort Code Is: {sort_code}

    Your Opening Balance Is: £{balance:.02f}

    Any other queries, please contact us on {email}

        """)

def write_PIN_confirmation(account_no, name, pin):
    with open(f"PIN Confirmations\\account{account_no}.txt","w", encoding="utf-8") as myfile:
        myfile.write(
        f"""
    Dear {name}, [{account_no}]

    Your New PIN Is: {pin}

    Any other queries, please contact us on {email}

        """)