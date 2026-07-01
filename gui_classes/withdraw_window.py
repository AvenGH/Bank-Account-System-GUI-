import tkinter as tk
import customtkinter as ctk
from PIL import Image
from api_classes.account_api import AccountAPI
from api_classes.transaction_api import TransactionAPI
import datacomp as dc
from util import generate_random_id


class WithdrawWindow:
    def __init__(self, dashboard, dashboard_frame, user):
        self.dashboard = dashboard
        self.dashboard_frame = dashboard_frame
        self.user=user
        self.width = 630
        self.height = 460

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        
        self.create_ui()


    def create_ui(self):   
        self.withdraw_frame = ctk.CTkFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.withdraw_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_withdraw_window)
        self.back_button.place(x=1, y=1)

        self.withdraw_title = ctk.CTkLabel(master=self.withdraw_frame, text="Please enter your details:", font=("Arial", 24))
        self.withdraw_title.pack(pady=10)

        self.withdraw_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.amount_label = ctk.CTkLabel(master=self.withdraw_frame, text="Amount", font=("Arial", 18))
        self.amount_label.place(x=100, y=105)

        self.amount = ctk.CTkEntry(master=self.withdraw_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter amount...")
        self.amount.place(x=275, y=100)

        self.display_button = ctk.CTkButton(master=self.withdraw_frame, fg_color="dark blue", text="Confirm Withdraw", command=self.withdraw, width=200)
        self.display_button.place(x=225, y=175)

    
    def withdraw(self):
        if self.amount.get() == "":
            tk.messagebox.showerror("Error", "Amount must not be blank.")
            return
        
        if not dc.is_positive(self.amount.get()):
            tk.messagebox.showerror("Error", "Amount must be a positive numerical value.")
            return
        
        if int(self.amount.get()) > self.user["balance"]:
            tk.messagebox.showerror("Error", "Insufficient balance. Please enter a lower amount.")
            return
        
        new_amount = self.user["balance"] - int(self.amount.get())
        print("New balance is:",new_amount)

        AccountAPI.modify_account(self.user["ID"], "balance", self.user["balance"] - int(self.amount.get()))
        self.user["balance"] = new_amount
        transid = generate_random_id.generate_transaction_id()
        
        TransactionAPI.add_transaction(
            transaction_id=transid, 
            acc_id=self.user["ID"], 
            type="Withdraw", 
            amount=int(self.amount.get()), 
            pending_balance=AccountAPI.fetch_account_by_id(self.user["ID"])["balance"]
        )
        tk.messagebox.showinfo("Withdraw Successful", f"£{float(self.amount.get()):.2f} has successfully been withdrawn from your account!\nNew Balance: £{new_amount:.2f}")
        self.close_withdraw_window()


    def close_withdraw_window(self):
        self.withdraw_frame.pack_forget()
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

