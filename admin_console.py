from api_classes.account_api import AccountAPI
from api_classes.transaction_api import TransactionAPI
import access_data as ad
import pyrebase


class AdminConsole:

    firebaseConfig = {
        'apiKey': "AIzaSyDb6XOMTUCqE0rxKXcNlLOAisfOrAMr_UM",
        'authDomain': "bank-account-system-228bb.firebaseapp.com",
        'databaseURL': "https://bank-account-system-228bb-default-rtdb.firebaseio.com/",
        'projectId': "bank-account-system-228bb",
        'storageBucket': "bank-account-system-228bb.firebasestorage.app",
        'messagingSenderId': "529265520944",
        'appId': "1:529265520944:web:71aa4d54e186bd8b2d18f5"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    @classmethod
    def delete_all_accounts(cls):
        AccountAPI.delete_all_accounts()

    @classmethod
    def clear_transactions(cls):
        TransactionAPI.delete_all_transactions()


if __name__ == "__main__":  
    AccountAPI.connect_db()
    TransactionAPI.connect_db()
    AdminConsole.clear_transactions()
    AdminConsole.delete_all_accounts()