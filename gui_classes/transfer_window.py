import tkinter as tk
import customtkinter as ctk
from PIL import Image
from api_classes.account_api import AccountAPI
from api_classes.transaction_api import TransactionAPI
import datacomp as dc
from util import generate_random_id


class TransferWindow:
    def __init__(self, dashboard, dashboard_frame, user):
        self.dashboard = dashboard
        self.dashboard_frame = dashboard_frame
        self.user = user
        self.width = 630
        self.height = 460

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        
        self.create_ui()


    def create_ui(self):   
        self.transfer_frame = ctk.CTkFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.transfer_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_transfer_window)
        self.back_button.place(x=1, y=1)

        self.transfer_title = ctk.CTkLabel(master=self.transfer_frame, text="Please enter your details:", font=("Arial", 24))
        self.transfer_title.pack(pady=10)

        self.transfer_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.payee_label = ctk.CTkLabel(master=self.transfer_frame, text="Payee Acc No", font=("Arial", 18))
        self.payee_label.place(x=100, y=105)

        self.payee_acc_no = ctk.CTkEntry(master=self.transfer_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter payee acc no...")
        self.payee_acc_no.place(x=275, y=100)

        self.amount_label = ctk.CTkLabel(master=self.transfer_frame, text="Amount", font=("Arial", 18))
        self.amount_label.place(x=100, y=180)

        self.amount = ctk.CTkEntry(master=self.transfer_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter amount...")
        self.amount.place(x=275, y=175)

        self.ref_label = ctk.CTkLabel(master=self.transfer_frame, text="Reference", font=("Arial", 18))
        self.ref_label.place(x=100, y=255)

        self.ref = ctk.CTkEntry(master=self.transfer_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter reference...")
        self.ref.place(x=275, y=250)

        self.display_button = ctk.CTkButton(master=self.transfer_frame, fg_color="dark blue", text="Confirm Transfer", command=self.transfer, width=200)
        self.display_button.place(x=225, y=325)

    
    def transfer(self):
        if self.amount.get() == "" or self.payee_acc_no.get() == "" or self.ref.get() == "":
            tk.messagebox.showerror("Error", "All fields are required.")
            return
        
        if not dc.is_positive(self.amount.get()):
            tk.messagebox.showerror("Error", "Amount must be a positive numerical value.")
            return
        
        if int(self.amount.get()) > self.user["balance"]:
            tk.messagebox.showerror("Error", "Insufficient balance. Please enter a lower amount.")
            return

        payee_account = AccountAPI.fetch_account_by_acc_no(self.payee_acc_no.get())
        if not payee_account:
            tk.messagebox.showerror("Error", "Account not found.")
            return
        
        new_amount = self.user["balance"] - int(self.amount.get())
        print("New balance is:",new_amount)

        AccountAPI.modify_account(
            account_id=self.user["ID"], 
            field="balance", 
            value=self.user["balance"] - int(self.amount.get())
        )
        AccountAPI.modify_account(
            account_id=payee_account["ID"],
            field="balance",
            value=payee_account["balance"] + int(self.amount.get())
        )
        self.user["balance"] = new_amount
        payee_account["balance"] = payee_account["balance"] + int(self.amount.get())

        transid = generate_random_id.generate_transaction_id()
        TransactionAPI.add_transaction(
            transaction_id=transid, 
            acc_id=self.user["ID"], 
            type="Transfer", 
            amount=int(self.amount.get()), 
            pending_balance=AccountAPI.fetch_account_by_id(self.user["ID"])["balance"],
            payee_acc_no=self.payee_acc_no.get(),
            reference = self.ref.get()
        )
        tk.messagebox.showinfo("Transfer Successful", f"{float(self.amount.get()):.2f} has successfully been transferred to account no [{self.payee_acc_no.get()}]!\nNew Balance: £{new_amount:.2f}")
        self.close_transfer_window()


    def close_transfer_window(self):
        self.transfer_frame.pack_forget()
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

