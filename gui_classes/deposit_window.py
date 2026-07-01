import tkinter as tk
import customtkinter as ctk
from PIL import Image
from api_classes.account_api import AccountAPI
from api_classes.transaction_api import TransactionAPI
import datacomp as dc
from util import generate_random_id


class DepositWindow:
    def __init__(self, dashboard, dashboard_frame, user):
        self.dashboard = dashboard
        self.dashboard_frame = dashboard_frame
        self.user = user
        self.width = 630
        self.height = 460

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        
        self.create_ui()


    def create_ui(self):   
        self.deposit_frame = ctk.CTkFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.deposit_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_deposit_window)
        self.back_button.place(x=1, y=1)

        self.deposit_title = ctk.CTkLabel(master=self.deposit_frame, text="Please enter your details:", font=("Arial", 24))
        self.deposit_title.pack(pady=10)

        self.deposit_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.amount_label = ctk.CTkLabel(master=self.deposit_frame, text="Amount", font=("Arial", 18))
        self.amount_label.place(x=100, y=105)

        self.amount = ctk.CTkEntry(master=self.deposit_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter amount...")
        self.amount.place(x=275, y=100)

        self.display_button = ctk.CTkButton(master=self.deposit_frame, fg_color="dark blue", text="Confirm Deposit", command=self.deposit, width=200)
        self.display_button.place(x=225, y=175)

    
    def deposit(self):
        if self.amount.get() == "":
            tk.messagebox.showerror("Error", "Amount must not be blank.")
            return

        if not dc.is_positive(self.amount.get()):
            tk.messagebox.showerror("Error", "Amount must be a positive numerical value.")
            return
        
        new_amount = self.user["balance"] + int(self.amount.get())
        print("New balance is:",new_amount)

        AccountAPI.modify_account(self.user["ID"], "balance", new_amount)
        self.user["balance"] = new_amount
        transid = generate_random_id.generate_transaction_id()

        TransactionAPI.add_transaction(
            transaction_id=transid, 
            acc_id=self.user["ID"], 
            type="Deposit", 
            amount=int(self.amount.get()), 
            pending_balance=new_amount
        )
        tk.messagebox.showinfo("Deposit Successful", f"£{float(self.amount.get()):.2f} has successfully been deposited into your account!\nNew Balance: £{new_amount:.2f}")
        self.close_deposit_window()


    def close_deposit_window(self):
        self.deposit_frame.pack_forget()
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

