import tkinter as tk
import customtkinter as ctk
from PIL import Image
import util.account_file_handler as afh
import datacomp as dc
from api_classes.account_api import AccountAPI


class ChangePINWindow:
    def __init__(self, dashboard, dashboard_frame, user):
        self.dashboard = dashboard
        self.dashboard_frame = dashboard_frame
        self.user = user
        self.width = 630
        self.height = 460

        self.logout_image = ctk.CTkImage(dark_image = Image.open("images\\logout2.jpg"), size=(25, 25))
        
        self.create_ui()


    def create_ui(self):   
        self.change_pin_frame = ctk.CTkFrame(master=self.dashboard, width=630, height=460) 

        self.back_button = ctk.CTkButton(master=self.change_pin_frame, text="", image=self.logout_image, width=40, height=40, command=self.close_change_pin_window)
        self.back_button.place(x=1, y=1)

        self.change_pin_title = ctk.CTkLabel(master=self.change_pin_frame, text="Please enter your details:", font=("Arial", 24))
        self.change_pin_title.pack(pady=10)

        self.change_pin_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.current_pin_label = ctk.CTkLabel(master=self.change_pin_frame, text="Current PIN", font=("Arial", 18))
        self.current_pin_label.place(x=100, y=105)

        self.current_pin = ctk.CTkEntry(master=self.change_pin_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter current PIN...", show="*")
        self.current_pin.place(x=275, y=100)

        self.new_pin_label = ctk.CTkLabel(master=self.change_pin_frame, text="New PIN", font=("Arial", 18))
        self.new_pin_label.place(x=100, y=180)

        self.new_pin = ctk.CTkEntry(master=self.change_pin_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Enter new PIN...", show="*")
        self.new_pin.place(x=275, y=175)

        self.conf_pin_label = ctk.CTkLabel(master=self.change_pin_frame, text="Confirm New PIN", font=("Arial", 18))
        self.conf_pin_label.place(x=100, y=255)

        self.conf_pin = ctk.CTkEntry(master=self.change_pin_frame, width=240, height=32, font=("Arial", 16), placeholder_text="Confirm new PIN...", show="*")
        self.conf_pin.place(x=275, y=250)

        self.display_button = ctk.CTkButton(master=self.change_pin_frame, fg_color="dark blue", text="Confirm Change of PIN", command=self.change_pin, width=200)
        self.display_button.place(x=225, y=325)

    
    def change_pin(self):
        if self.current_pin.get() == "" or self.new_pin.get() == "" or self.conf_pin.get() == "":
            tk.messagebox.showerror("Error", "All fields are required.")
            return
        
        if self.current_pin.get() != self.user["PIN"]:
            tk.messagebox.showerror("Error", "Incorrect PIN")
            return
        
        if (len(self.new_pin.get()) != 4) or (len(self.conf_pin.get()) != 4):
            tk.messagebox.showerror("Error", "PIN must be exactly 4 digits long")
            return
        
        if not(dc.is_positive_int(self.new_pin.get(), True)) or not(dc.is_positive_int(self.conf_pin.get(), True)):
            tk.messagebox.showerror("Error", "PIN must be exactly 4 digits long")
            return
        
        if self.new_pin.get() != self.conf_pin.get():
            tk.messagebox.showerror("Error", "PINs do not match.")
            return
        
        AccountAPI.modify_account(self.user["ID"], "PIN", self.conf_pin.get())
        self.user["PIN"] = self.conf_pin.get()

        tk.messagebox.showinfo("Change of PIN Successful", f"Your banking PIN has successfully been changed!")
        
        self.close_change_pin_window()

        afh.write_PIN_confirmation(
            account_no=self.user["account_no"],
            name=self.user["name"],
            pin=self.user["PIN"]
        )


    def close_change_pin_window(self):
        self.change_pin_frame.pack_forget()
        self.dashboard_frame.pack(pady=20, padx=60, fill="both", expand=True)

