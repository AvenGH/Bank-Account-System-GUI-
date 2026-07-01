from db_manager import DBManager
import datacomp as dc
import datetime
import tkinter as tk
import customtkinter as ctk

today = datetime.date.today()

# API for managing transaction records

class TransactionAPI:
    db = None
    cursor = None

    # Attempts to connect to database and returns error if connection is unsuccessful
    @classmethod
    def connect_db(cls):
        try:
            cls.db = DBManager("BankingManagementSystem")
            cls.cursor = cls.db.get_cursor()
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    # Fetches all transactions from the DB table
    @classmethod
    def get_transactions(cls):
        cls.cursor.execute("SELECT * FROM transactions")
        transactions = cls.cursor.fetchall()
        return transactions
    
    # Fetches a particular transaction given the id
    @classmethod
    def fetch_transaction_by_id(cls, transaction_id):
        cls.cursor.execute(f"SELECT * FROM transactions WHERE \"ID\" = %s", (transaction_id, ))
        transaction = cls.cursor.fetchone()
        return transaction
    
    # Fetches all transactions given a specific account id
    @classmethod
    def fetch_transactions_by_acc_id(cls, acc_id):
        cls.cursor.execute(f"SELECT * FROM transactions WHERE acc_id = %s", (str(acc_id), ))
        transactions = cls.cursor.fetchall()
        return transactions
    
    # Adds a transaction record to the database
    @classmethod
    def add_transaction(cls, transaction_id, acc_id, type, amount, pending_balance, payee_acc_no=None, reference=None):
        cls.cursor.execute(
            """
            INSERT INTO transactions (
                "ID", acc_id, type, amount, pending_balance, payee_acc_no, reference
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (transaction_id, acc_id, type, amount, pending_balance, payee_acc_no, reference)
        )

        return True
    
    # Makes changes to a transaction record
    @classmethod
    def modify_transaction(cls, transaction_id, field, value):
        cls.cursor.execute(
            f"UPDATE transactions SET {field} = %s WHERE \"ID\" = %s", (value, transaction_id)
        )
    
    # Deletes the transaction record from the database
    @classmethod
    def delete_transaction(cls, transaction_id):
        cls.cursor.execute(
            f"DELETE FROM transactions WHERE \"ID\" = %s", transaction_id
        )

    # Deletes all transactions from the database
    @classmethod
    def delete_all_transactions(cls):
        cls.cursor.execute(
            f"DELETE FROM transactions"
        )
        

if __name__ == "__main__":
    TransactionAPI.connect_db()
    print(TransactionAPI.get_transactions())
