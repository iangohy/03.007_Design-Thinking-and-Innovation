import csv

while True:
    with open('data.csv', 'a') as data:
        barcode = input("Enter barcode (enter q to quit): ")
        if barcode.lower() == "q":
            print("Thank you for your hard work!")
            print("Quitting...")
            quit()
        description = input("Enter product description: ")
        classification = input("Enter category (waste/paper/plastic/can): ")
        while classification != "waste" and classification != "paper" and classification != "plastic" and classification != "can":
            classification = input("Enter category (waste/paper/plastic/can): ")
        writer = csv.writer(data)
        writer.writerow([barcode, description, classification])

