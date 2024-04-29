import csv

def csvlog(self, other_pn, amount, s_r):
    filename = './userlogs/' + self.name + '.csv'
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [other_pn, amount, s_r]
        writer.writerow(row)
