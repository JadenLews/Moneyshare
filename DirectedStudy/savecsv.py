import csv

def csvlog(self, other_pn, amount):
    filename = './userlogs/' + self.name + '.csv'
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [other_pn, amount]
        writer.writerow(row)
