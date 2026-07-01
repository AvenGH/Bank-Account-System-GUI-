import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import gui_classes.deposit_window
import gui_classes.withdraw_window
import gui_classes.transfer_window
import gui_classes.change_pin_window
from api_classes.transaction_api import TransactionAPI

TransactionAPI.connect_db()


class Dashboard:
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

        self.bookings_button = ctk.CTkButton(master=self.dashboard_frame, text="", image=self.bookings_image, width=40, height=40)
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