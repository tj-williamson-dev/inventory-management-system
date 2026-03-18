import json
import os
import csv
import tkinter as tk
from tkinter import messagebox

FILE_NAME = "inventory.json"
EXPORT_FILE = "inventory_export.csv"


def load_inventory():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_inventory():
    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file)


def get_filtered_inventory():
    search_text = search_entry.get().strip().lower()
    if not search_text:
        return inventory

    return [item for item in inventory if search_text in item["name"].lower()]


def refresh_listbox():
    listbox.delete(0, tk.END)

    filtered_inventory = get_filtered_inventory()

    for item in filtered_inventory:
        total_value = item["quantity"] * item["price"]
        listbox.insert(
            tk.END,
            f"{item['name']} | {item['category']} | Qty: {item['quantity']} | Price: ${item['price']:.2f} | Value: ${total_value:.2f}"
        )

    total_items_label.config(text=f"Total Unique Items: {len(filtered_inventory)}")

    total_quantity = sum(item["quantity"] for item in filtered_inventory)
    total_value = sum(item["quantity"] * item["price"] for item in filtered_inventory)

    total_quantity_label.config(text=f"Total Quantity: {total_quantity}")
    total_value_label.config(text=f"Total Inventory Value: ${total_value:.2f}")


def add_item():
    name = name_entry.get().strip()
    qty = quantity_entry.get().strip()
    price = price_entry.get().strip()
    category = category_entry.get().strip()

    if not name or not category:
        messagebox.showerror("Error", "Name and Category required.")
        return

    if not qty.isdigit():
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    try:
        price = float(price)
    except:
        messagebox.showerror("Error", "Price must be a number.")
        return

    for item in inventory:
        if item["name"].lower() == name.lower():
            item["quantity"] += int(qty)
            item["price"] = price
            item["category"] = category
            save_inventory()
            refresh_listbox()
            clear_entries()
            return

    inventory.append({
        "name": name,
        "quantity": int(qty),
        "price": price,
        "category": category
    })

    save_inventory()
    refresh_listbox()
    clear_entries()


def delete_item():
    selected = listbox.curselection()
    if not selected:
        return

    filtered = get_filtered_inventory()
    selected_item = filtered[selected[0]]

    inventory.remove(selected_item)

    save_inventory()
    refresh_listbox()
    clear_entries()


def update_item():
    selected = listbox.curselection()
    if not selected:
        return

    name = name_entry.get().strip()
    qty = int(quantity_entry.get())
    price = float(price_entry.get())
    category = category_entry.get().strip()

    filtered = get_filtered_inventory()
    selected_item = filtered[selected[0]]

    for i, item in enumerate(inventory):
        if item == selected_item:
            inventory[i] = {
                "name": name,
                "quantity": qty,
                "price": price,
                "category": category
            }

    save_inventory()
    refresh_listbox()
    clear_entries()


def export_to_csv():
    with open(EXPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Category", "Quantity", "Price", "Value"])

        for item in inventory:
            value = item["quantity"] * item["price"]
            writer.writerow([
                item["name"],
                item["category"],
                item["quantity"],
                item["price"],
                value
            ])

    messagebox.showinfo("Exported", "CSV file created!")


def load_selected_item(event):
    selected = listbox.curselection()
    if not selected:
        return

    item = get_filtered_inventory()[selected[0]]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, item["name"])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, str(item["quantity"]))

    price_entry.delete(0, tk.END)
    price_entry.insert(0, str(item["price"]))

    category_entry.delete(0, tk.END)
    category_entry.insert(0, item["category"])


def clear_entries():
    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)


inventory = load_inventory()

for item in inventory:
    if "category" not in item:
        item["category"] = "General"
    if "price" not in item:
        item["price"] = 0.0

root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1000x720")
root.configure(bg="#f4f6f8")

tk.Label(root, text="Inventory Management System",
         font=("Segoe UI", 22, "bold"),
         bg="#f4f6f8").pack(pady=15)

search_entry = tk.Entry(root, width=30)
search_entry.pack()
search_entry.bind("<KeyRelease>", lambda e: refresh_listbox())

form = tk.Frame(root, bg="#f4f6f8")
form.pack(pady=10)

name_entry = tk.Entry(form)
name_entry.grid(row=1, column=0, padx=5)
tk.Label(form, text="Name", bg="#f4f6f8").grid(row=0, column=0)

quantity_entry = tk.Entry(form)
quantity_entry.grid(row=1, column=1, padx=5)
tk.Label(form, text="Quantity", bg="#f4f6f8").grid(row=0, column=1)

price_entry = tk.Entry(form)
price_entry.grid(row=1, column=2, padx=5)
tk.Label(form, text="Price", bg="#f4f6f8").grid(row=0, column=2)

category_entry = tk.Entry(form)
category_entry.grid(row=1, column=3, padx=5)
tk.Label(form, text="Category", bg="#f4f6f8").grid(row=0, column=3)

buttons = tk.Frame(root, bg="#f4f6f8")
buttons.pack(pady=10)

tk.Button(buttons, text="Add", command=add_item).grid(row=0, column=0, padx=5)
tk.Button(buttons, text="Update", command=update_item).grid(row=0, column=1, padx=5)
tk.Button(buttons, text="Delete", command=delete_item).grid(row=0, column=2, padx=5)
tk.Button(buttons, text="Export", command=export_to_csv).grid(row=0, column=3, padx=5)

stats = tk.Frame(root, bg="#f4f6f8")
stats.pack()

total_items_label = tk.Label(stats, text="")
total_items_label.grid(row=0, column=0, padx=10)

total_quantity_label = tk.Label(stats, text="")
total_quantity_label.grid(row=0, column=1, padx=10)

total_value_label = tk.Label(stats, text="")
total_value_label.grid(row=0, column=2, padx=10)

listbox = tk.Listbox(root, width=120, height=20)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", load_selected_item)

refresh_listbox()

root.mainloop()