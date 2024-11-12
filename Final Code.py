import pandas as pd
import os


def initialize_bill_number_file():
    bill_file = "bill_number.csv"
    if not os.path.exists(bill_file):
        #initial Bill ID as 1
        df = pd.DataFrame({'BillID': [1]})

        df.to_csv(bill_file, index=False)
        print(f"Bill Number file '{bill_file}' has been created with initial Bill ID 1.")
    else:
        print(f"Bill Number file '{bill_file}' already exists.")


# Function to display inventory
def inventory():
    print("\n" + "=" * 19 + " Inventory of products in stock " + "=" * 19 + "\n")
    inventory_file = "D:\\IKEA\\Furniture.csv"
    if os.path.exists(inventory_file):
        inventory_df = pd.read_csv(inventory_file)
        print(inventory_df.to_string(index=False))  # Prints without row indices
    else:
        print(f"Error: {inventory_file} not found!")


# Function to add data to the inventory
def add_data(file_path, new_data):
    print("\nAdding data to inventory...")
    try:
        df = pd.read_csv(file_path)
        df2 = pd.DataFrame([new_data])
        df = pd.concat([df, df2], ignore_index=True)
        df.to_csv(file_path, index=False)  # Save without index
        print("Data added successfully.")
    except Exception as e:
        print(f"Error while adding data: {e}")


# Function to update inventory quantity
def update_inventory(file_path, product_id, new_quantity):
    print("\nUpdating inventory quantity...")
    try:
        df = pd.read_csv(file_path)
        if product_id in df['Product_id'].values:
            df.loc[df['Product_id'] == product_id, 'Quantity'] = new_quantity
            df.to_csv(file_path, index=False)  # Save without index
            print("Quantity updated successfully.")
        else:
            print(f"Error: Product ID {product_id} not found!")
    except Exception as e:
        print(f"Error in updating quantity: {e}")


# Function for generating bills with GST and storing them incrementally
def bill_making():
    inventory_file = "D:\\IKEA\\Furniture.csv"
    bill_file = "bill_number.csv"
    all_bills_file = "all_bills.csv"  # Cumulative file to store all bills with incremental Bill IDs
    gst_rate = 18

    try:
        df3 = pd.read_csv(inventory_file)
        df4 = pd.read_csv(bill_file)
    except FileNotFoundError:
        print("File not found. Make sure all required files exist.")
        return

    # Initialize the final bill DataFrame with column structure
    final_bill = pd.DataFrame(
        columns=['Bill ID', 'Buyer name', 'Buyer contact', 'ProductID', 'ProductName', 'GST', 'Price', 'Quantity',
                 'Total'])
    bill_number = df4.loc[0, 'BillID']  # Read the current Bill ID

    # Collect buyer details
    buyer_name = input("Enter buyer name: ")
    buyer_contact = int(input("Enter Buyer contact number: "))

    while True:
        print("\nAvailable Products in inventory:")
        print(df3.to_string(index=False))  # Display inventory without indices
        sell_id = int(input("Enter the Product_id to sell: "))
        quantity_sold = int(input("Enter the quantity sold: "))

        if sell_id in df3['Product_id'].values:
            stock = df3.loc[df3['Product_id'] == sell_id, 'Quantity'].values[0]
            if quantity_sold <= stock:
                product_details = df3.loc[df3['Product_id'] == sell_id].iloc[0]
                product_price = product_details['Total Price']

                gst_amount = (product_price * gst_rate) / 100
                total_cost = quantity_sold * (product_price + gst_amount)

                # Update inventory quantity
                df3.loc[df3['Product_id'] == sell_id, 'Quantity'] -= quantity_sold

                # Append the new sale to the final bill DF(DataFrame)
                new_sale = {
                    'Bill ID': bill_number,
                    'Buyer name': buyer_name,
                    'Buyer contact': buyer_contact,
                    'ProductID': sell_id,
                    'ProductName': product_details['Furniture Entities'],
                    'GST': gst_amount,
                    'Price': product_price,
                    'Quantity': quantity_sold,
                    'Total': total_cost
                }
                final_bill = pd.concat([final_bill, pd.DataFrame([new_sale])], ignore_index=True)

                print('\n----Current purchase----')
                print(f"Product_id: {sell_id}")
                print(f"Furniture Entities: {product_details['Furniture Entities']}")
                print(f"Quantity: {quantity_sold}")
                print(f"Price per unit: INR {product_price}")
                print(f"GST per unit: INR {gst_amount}")
                print(f"Total cost (including GST): INR {total_cost}")

                purchase = input("Do you want to buy another product? (yes/no): ").lower()
                if purchase != 'yes':
                    break
            else:
                print("Not enough quantity in stock.")
        else:
            print("Product_id not found in inventory.")

    df4.loc[0, 'BillID'] = bill_number + 1 #incrementing
    df4.to_csv(bill_file, index=False)

    total = final_bill['Total'].sum()
    print("\n" + "=" * 29 + " HHJR FURNITURE SHOP " + "=" * 29)
    print("\n" + "=" * 34 + " Final Bill " + "=" * 34)
    print(f"\nBill ID of Final Bill is: {bill_number}")
    print(f"Buyer name: {buyer_name}")
    print(f"Buyer Contact Number: {buyer_contact}")
    print("\n", final_bill.to_string(index=False))
    print(f"\nFinal Total: INR {total}")

    # Append the current bill to the cumulative all_bills.csv file
    if os.path.exists(all_bills_file):
        all_bills = pd.read_csv(all_bills_file)
        all_bills = pd.concat([all_bills, final_bill], ignore_index=True)
    else:
        all_bills = final_bill  # If file doesn't exist, create it with the first bill

    all_bills.to_csv(all_bills_file, index=False)
    print(f"Bill data appended to '{all_bills_file}' successfully.")

    # Create a separate file for this bill
    output_folder = "Bill files"
    bill_folder = os.path.join(output_folder, f'Bill_{bill_number}_{buyer_name}')
    os.makedirs(bill_folder, exist_ok=True)
    final_bill.to_csv(os.path.join(bill_folder, f"bill_{bill_number}.csv"), index=False)

    print(f"Final bill saved to '{bill_folder}' successfully.")


def modification_inventory():
    inventory_file = "D:\\IKEA\\Furniture Price Prediction.csv"  # Update path as needed

    while True:
        print("\n1. Add data to inventory")
        print("2. Update quantity in inventory")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            print("Adding data to inventory:")
            product_id = int(input("Enter Product_id: "))
            product_name = input("Enter Furniture Entities: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per unit: "))

            new_data = {
                'Product_id': product_id,
                'Furniture Entities': product_name,
                'Quantity': quantity,
                'Total Price': price
            }

            add_data(inventory_file, new_data)

        elif choice == 2:
            print("Updating quantity in inventory:")
            product_id = int(input("Enter Product_id to update: "))
            new_quantity = int(input("Enter new quantity: "))

            update_inventory(inventory_file, product_id, new_quantity)

        elif choice == 3:
            print("Exiting the modification menu.")
            break
        else:
            print("Invalid choice. Please enter a valid option (1, 2, or 3).")


def main():
    # Initialize the Bill Number file first
    initialize_bill_number_file()

    while True:
        print("\nMenu:")
        print("1. View Inventory")
        print("2. Modify Inventory")
        print("3. Make a Bill")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            inventory()
        elif choice == 2:
            modification_inventory()
        elif choice == 3:
            bill_making()
        elif choice == 4:
            print("Exiting the program. Have a good day!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()