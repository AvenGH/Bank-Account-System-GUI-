import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import gui_classes.deposit_window
import gui_classes.withdraw_window
import gui_classes.transfer_window
import gui_classes.change_pin_window
from api_classes.transaction_api import TransactionAPI
import tkkbootstrap as tb
from ttkbootstrap.constants import *

TransactionAPI.connect_db()


class Dashboard:

    FIELDS = ("ID", "Type", "Amount", "Pending Balance", "Payee Acc No", "Reference")

    def __init__(self, root, user, dimensions="750x500"):
        self.root = root
        self.dimensions = dimensions
        self.user = user
        self.data=[]

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        self.bookings_image = ctk.CTkImage(dark_image = Image.open("images\\bookings_icon.png"), size=(35, 25))
        self.create_ui()
        self.dashboard.protocol("WM_DELETE_WINDOW", self.on_close)


    # Executed when close button is pressed on right hand corner
    def on_close(self):
        self.dashboard.destroy()
        self.root.deiconify()


    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        style = tb.Style(theme="darkly")
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.dashboard = ctk.CTkToplevel(self.root)
        self.dashboard.geometry(self.dimensions)
        self.dashboard.title("Dashboard")

        # Defines space within which elements may be positioned
        self.dashboard_frame = ctk.CTkFrame(master=self.dashboard)
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Creates a title positioned at the top of the screen
        self.dashboard_title = ctk.CTkLabel(master=self.dashboard_frame, text="Welcome! Please select an option:", font=("Arial", 24))
        self.dashboard_title.pack(pady=12, padx=10)

        self.logout_button = ctk.CTkButton(master=self.dashboard_frame, text="", image=self.logout_image, width=40, height=40, command=self.on_close)
        self.logout_button.place(x=50, y=50)

        self.bookings_button = ctk.CTkButton(master=self.dashboard_frame, text="", image=self.bookings_image, width=40, height=40, command=self.load_transactions)
        self.bookings_button.place(x=525, y=50)

        # Field that allows user to submit all their account registration details
        self.deposit_button = ctk.CTkButton(master=self.dashboard_frame, text="Deposit", command=self.load_deposit_window, fg_color="green",)
        self.deposit_button.pack(pady=12, padx=10)

        self.withdraw_button = ctk.CTkButton(master=self.dashboard_frame, text="Withdraw", command=self.load_withdraw_window, fg_color="red")
        self.withdraw_button.pack(pady=12, padx=10)

        self.balance_button = ctk.CTkButton(master=self.dashboard_frame, text="Check Balance", command=self.check_balance, fg_color="blue")
        self.balance_button.pack(pady=12)

        self.transfer_button = ctk.CTkButton(master=self.dashboard_frame, text="Transfer", command=self.load_transfer_window)
        self.transfer_button.pack(pady=12)

        self.change_pin_button = ctk.CTkButton(master=self.dashboard_frame, text="Change PIN", command=self.load_change_pin_window, fg_color="darkblue")
        self.change_pin_button.pack(pady=12)

        self.transactions_frame = ctk.CTkScrollableFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.transactions_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_transactions_window)
        self.back_button.place(x=1, y=1)

        self.title = ctk.CTkLabel(master=self.transactions_frame, text="Transaction History:", font=("Arial", 24))
        self.title.pack(pady=10)

        self.tree = ttk.Treeview(
            master=self.transactions_frame, 
            columns=Dashboard.FIELDS,
            show="headings", height=30,
            style="darkly", 
        )

        for field in Dashboard.FIELDS:
            self.tree.heading(field, text=field, anchor="center")
            self.tree.column(field, anchor="center", width=200)


    def load_transactions(self):
        # Hide the main dashboard
        self.dashboard_frame.pack_forget()
        # Show the bookings
        self.transactions_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.data.clear()
        self.fetch_transactions()

        for item in self.data:
            self.tree.insert("", "end", values=item)

        self.tree.pack()


    def fetch_transactions(self):
        seperator = []
        for _ in Dashboard.FIELDS:
            seperator.append("----------------------")
        self.data.append(tuple(seperator))

        transactions = TransactionAPI.fetch_transactions_by_acc_id(self.user["ID"])

        for transaction in transactions:
            self.data.append(
                (
                    ""
                )
            )
            self.data.append(
                (
                    transaction["ID"],
                    transaction["type"],
                    f"£{transaction["amount"]:.2f}",
                    f"£{transaction["pending_balance"]:.2f}",
                    transaction["payee_acc_no"],
                    transaction["reference"]
                )
            ) 


    def close_transactions_window(self):
        # Hide the bookings
        self.transactions_frame.pack_forget()
        # Bring the dashboard back
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)


    def load_deposit_window(self):
        self.dashboard_frame.pack_forget()
        self.deposit_window = gui_classes.deposit_window.DepositWindow(self.dashboard, self.dashboard_frame, self.user)


    def load_withdraw_window(self):
        self.dashboard_frame.pack_forget()
        self.withdraw_window = gui_classes.withdraw_window.WithdrawWindow(self.dashboard, self.dashboard_frame, self.user)


    def check_balance(self):
        tk.messagebox.showinfo("Current Balance", f"Your current balance is: £{self.user["balance"]:.2f}")

    
    def load_transfer_window(self):
        self.dashboard_frame.pack_forget()
        self.transfer_window = gui_classes.transfer_window.TransferWindow(self.dashboard, self.dashboard_frame, self.user)


    def load_change_pin_window(self):
        self.dashboard_frame.pack_forget()
        self.change_pin_window = gui_classes.change_pin_window.ChangePINWindow(self.dashboard, self.dashboard_frame, self.user)


# Allows file to be run independent of the main menu
if __name__ == '__main__':
    root = ctk.CTk()
    app = Dashboard(root, "user")
    root.mainloop()