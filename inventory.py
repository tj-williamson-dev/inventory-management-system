import json

# Load inventory from file
try:
    with open("inventory.json", "r") as file:
        inventory = json.load(file)
except:
    inventory = []

while True:
    print("\n1. Add Item")
    print("2. View Items")
    print("3. Delete Item")
    print("4. Update Quantity")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        item_name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))

        item = {
            "name": item_name,
            "quantity": quantity
        }

        inventory.append(item)
        print(f"{item_name} added with quantity {quantity}!")

    elif choice == "2":
        print("\nInventory:")

        if len(inventory) == 0:
            print("No items in inventory.")
        else:
            for item in inventory:
                print(f"- {item['name']} | Quantity: {item['quantity']}")

    elif choice == "3":
        item_name = input("Enter item to delete: ")

        for item in inventory:
            if item["name"].lower() == item_name.lower():
                inventory.remove(item)
                print(f"{item['name']} deleted!")
                break
        else:
            print("Item not found.")

    elif choice == "4":
        item_name = input("Enter item to update: ")

        for item in inventory:
            if item["name"].lower() == item_name.lower():
                new_qty = int(input("Enter new quantity: "))
                item["quantity"] = new_qty
                print(f"{item['name']} updated to {new_qty}!")
                break
        else:
            print("Item not found.")

    elif choice == "5":
        # Save inventory before exiting
        with open("inventory.json", "w") as file:
            json.dump(inventory, file)

        print("Saved! Goodbye!")
        break

    else:
        print("Invalid option")