import tkinter as tk
from tkinter import simpledialog, messagebox, Checkbutton, IntVar, Toplevel, Button

class TravelApp:
    def __init__(self):
        self.places_data = {'Mumbai': {}, 'Delhi': {}, 'Bangalore': {}, 'Kolkata': {}}
        self.places_customization = []

    def show_customization_dialog(self, root):
        dialog = Toplevel(root)
        dialog.title("Select Places")
        dialog.geometry('400x300')
        vars = {}
        for place in self.places_data:
            var = IntVar()
            chk = Checkbutton(dialog, text=place, variable=var, anchor='w', width=20, pady=5)
            chk.pack()
            vars[place] = var
        def confirm():
            self.places_customization = [place for place, var in vars.items() if var.get() == 1]
            dialog.destroy()
            root.destroy()

        Button(dialog, text="Confirm", command=confirm).pack(pady=10)

        dialog.transient(root)
        dialog.grab_set()
        dialog.wait_window()

    def gui_input(self):
        root = tk.Tk()
        root.title("Main Window")
        root.geometry('600x400')
        starting_city = simpledialog.askstring("Input", "Enter the starting city:", parent=root)
        max_time = simpledialog.askfloat("Input", "Enter the maximum allowable time in hours:", parent=root)
        max_cost = simpledialog.askfloat("Input", "Enter the maximum allowable cost in Rs:", parent=root)

        while True:
            value = simpledialog.askstring("Input", "Enter 1 for all places and 2 for customization:", parent=root)
            if value not in ['1', '2']:
                tk.messagebox.showerror("Invalid Input", "Please enter 1 or 2")
                continue
            else:
                break
        if value == '1':
            self.places_customization = list(self.places_data.keys())
            root.destroy()
        elif value == '2':
            self.show_customization_dialog(root)
            
        else:
            messagebox.showerror("Invalid Input", "Please enter 1 or 2")
        
        print("Selected Places:", self.places_customization)
        
# Usage
app = TravelApp()
app.gui_input()
