from db_manager import DBManager

class AccountAPI:
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

    # Fetches all accounts from the DB table
    @classmethod
    def get_accounts(cls):
        cls.cursor.execute("SELECT * FROM accounts")
        bookings = cls.cursor.fetchall()
        return bookings
    
    # Fetches a particular account given the id
    @classmethod
    def fetch_account_by_id(cls, user_id):
        cls.cursor.execute(f"SELECT * FROM accounts WHERE \"ID\" = %s", (user_id, ))
        account = cls.cursor.fetchone()
        return account
    
    # Fetches a particular account given the account no
    @classmethod
    def fetch_account_by_acc_no(cls, acc_no):
        cls.cursor.execute(f"SELECT * FROM accounts WHERE account_no = %s", (acc_no, ))
        account = cls.cursor.fetchone()
        return account
    
    # Fetches a particular account id given the email
    @classmethod
    def fetch_account_by_email(cls, email):
        cls.cursor.execute(f"SELECT * FROM accounts WHERE email = %s", (email, ))
        account = cls.cursor.fetchone()
        return account

    # Adds a account record to the database
    @classmethod
    def add_account(cls, account_id, account_no, name, opening_balance, sort_code, PIN, attempts, blocked, email):
        cls.cursor.execute(
            """
            INSERT INTO accounts (
                "ID", account_no, name, balance, sort_code, \"PIN\", attempts, blocked, email
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (account_id, account_no, name, opening_balance, sort_code, PIN, attempts, blocked, email)
        )

        return True
    
    # Makes changes to a account record
    @classmethod
    def modify_account(cls, account_id, field, value):
        cls.cursor.execute(
            f"UPDATE accounts SET \"{field}\" = %s WHERE \"ID\" = %s", (value, account_id)
        )
    
    # Deletes the account record from the database
    @classmethod
    def delete_account(cls, account_id):
        cls.cursor.execute(
            f"DELETE FROM accounts WHERE \"ID\" = %s", account_id
        )

    # Deletes all accounts from the database
    @classmethod
    def delete_all_accounts(cls):
        cls.cursor.execute(
            f"DELETE FROM accounts"
        )
      