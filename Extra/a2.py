import tkinter as tk
from tkinter import simpledialog, messagebox, Checkbutton, IntVar, Toplevel, Button

class TravelApp:
    def __init__(self):
        self.places_data = {'Mumbai': {}, 'Delhi': {}, 'Bangalore': {}, 'Kolkata': {}}
        self.places_customization = []

    def show_customization_dialog(self, root):
        dialog = Toplevel(root)
        dialog.title("Select Places")
        dialog.geometry('400x300')  # Set the dimensions of the dialog

        vars = {}

        # Create a Checkbutton for each place in places_data and map it to an IntVar
        for place in self.places_data:
            var = IntVar()
            chk = Checkbutton(dialog, text=place, variable=var, anchor='w', width=20, pady=5)
            chk.pack()  # This will pack checkboxes vertically
            vars[place] = var  # Store the IntVar associated with this place

        def confirm():
            self.places_customization = [place for place, var in vars.items() if var.get() == 1]
            dialog.destroy()
            root.destroy()  # This will close the main window as well

        Button(dialog, text="Confirm", command=confirm).pack(pady=10)

        dialog.transient(root)  # Set to be a transient window of the root window
        dialog.grab_set()  # Make the window modal
        dialog.wait_window()  # Wait here until the dialog is closed

    def gui_input(self):
        root = tk.Tk()
        root.title("Main Window")
        root.geometry('600x400')  # Configure main window size

        # Gather user inputs via simple dialog
        starting_city = simpledialog.askstring("Input", "Enter the starting city:", parent=root)
        max_time = simpledialog.askfloat("Input", "Enter the maximum allowable time in hours:", parent=root)
        max_cost = simpledialog.askfloat("Input", "Enter the maximum allowable cost in Rs:", parent=root)

        while True:
            value = simpledialog.askstring("Input", "Enter 1 for all places and 2 for customization:", parent=root)
            if value not in ['1', '2']:  # Validate input
                tk.messagebox.showerror("Invalid Input", "Please enter 1 or 2")
                continue
            else:
                break
        match value:
            case 1:
                self.places_customization=list(self.places_data.index)
            case 2:
                # return "Two"
                p=list(self.places_data.index)
                root.title("Main Window")
                self.places_customization=p
                Button(root, text="Open Dialog", command=lambda: self.show_customization_dialog(root)).pack(pady=20)
                print("starting city : ",starting_city)
                print("max_time : ",max_time)
                print("max_cost : ",max_cost)

# Usage
app = TravelApp()
app.gui_input()
