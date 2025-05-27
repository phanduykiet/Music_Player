import tkinter as tk
import random

def generate_random_list():
    items = [f"Item {i}" for i in range(1, 11)]  # Replace this with your actual data
    random.shuffle(items)
    return items

def update_listbox():
    items = generate_random_list()
    listbox.delete(0, tk.END)  # Clear existing items
    for item in items:
        listbox.insert(tk.END, item)

# Create the main window
root = tk.Tk()
root.title("Random Listbox Example")

# Create a Listbox
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack(padx=10, pady=10)

# Create a button to generate random items
generate_button = tk.Button(root, text="Generate Random Items", command=update_listbox)
generate_button.pack(pady=10)

# Initial population of the Listbox
update_listbox()

# Start the Tkinter event loop
root.mainloop()
