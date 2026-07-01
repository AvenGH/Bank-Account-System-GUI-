from api_classes.transaction_api import TransactionAPI
from api_classes.account_api import AccountAPI

import random

def generate_transaction_id():
    existing_transaction_ids = [transaction["ID"] for transaction in TransactionAPI.get_transactions()]
    if existing_transaction_ids:
        top_id = existing_transaction_ids[-1]
        if top_id != "#9999":
            new_id = f'#{int(top_id[1:])+1: 05}'.replace(" ", "")
            return new_id
    return "#0001"

def generate_account_id():
    existing_account_ids = [account["ID"] for account in AccountAPI.get_accounts()]
    new_id = f'#{random.randint(1, 9999): 05}'.replace(" ", "")
    if new_id in existing_account_ids:
        generate_account_id()
    return new_id

def generate_account_no():
    existing_account_numbers = [account['account_no'] for account in AccountAPI.get_accounts()]
    while True:
        acc_no = str(random.randrange(10000000, 100000000))
        if acc_no not in existing_account_numbers:
            return acc_no
    

if __name__ == "__main__":
    TransactionAPI.connect_db()
    test_id = generate_transaction_id()
    print(test_id)