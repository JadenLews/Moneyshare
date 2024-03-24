#### Can rewrite as a function to initialize a transaction log
#### and a separate function to add rows to a transaction log after it has been created

import csv

# Define some sample data as a list of dictionaries
# Each dictionary contains phone, transaction_amt, and date as keys
data = [
    {'phone': '1234', 'transaction_amt': 10, 'date': '2024-01-01'},
]

# Specify the filename
filename = 'Bob_transactions.csv'

# Open the file in write mode ('w', newline='') for compatibility across different platforms
with open(filename, 'w', newline='') as file:
    # Specify the fieldnames based on the dictionary keys
    fieldnames = ['phone', 'transaction_amt', 'date']
    
    # Create a writer object, specifying the fieldnames and the file
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data rows
    for row in data:
        writer.writerow(row)

print(f'File {filename} created successfully.')
