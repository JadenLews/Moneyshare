#### Can rewrite as a function to initialize a transaction log
#### and a separate function to add rows to a transaction log after it has been created

import csv

# Define some sample data as a list of dictionaries
# Each dictionary contains phone and amt
data_dictionary = {
    2345 : [10, 2],
    1234 : [-15]
    }

# Specify the filename
filename = '123_log.csv'

# Open the file in write mode ('w', newline='') for compatibility across different platforms
with open(filename, 'w', newline='') as file:

    # Create a writer object, specifying the fieldnames and the file
    writer = csv.writer(file)
    
    # Write the data rows
    for phone_number, transaction_amts in data_dictionary.items():
        row = [phone_number]
        row.extend(transaction_amts)
        writer.writerow(row)

print(f'File {filename} created successfully.')
