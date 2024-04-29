from hashlib import sha256
from savecsv import csvlog
import random 
import csv
import os
from datetime import datetime


class User:
    def __init__(self, p_name, p_number, p_input_balance, currency):
        self.name = p_name
        self.transaction_log = {}
        self.currency = currency
        filename = self.name + '.csv'
        path = './userlogs/' + filename
        check_file = os.path.isfile(path)
        if check_file:
            self.load_user(filename)
        else:
            self.unique_identifier = p_number
            self.account_balance = p_input_balance
            filename = './userlogs/' + self.name + '.csv'
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                row = [p_input_balance, p_number]
                writer.writerow(row)

    def balance_check(self, amount):
        if self.account_balance < amount:
            return False
        elif self.account_balance > amount:
            return True
        
    def make_transaction(self, amount, action):
        if action == 'add':
            self.account_balance = self.account_balance + amount
        elif action == 'subtract':
            self.account_balance = self.account_balance - amount
    
    def generate_code_1(self, amountt, phone_numberr):
        amount = str(amountt)
        phone_number = str(phone_numberr)
        previous_transactions = self.transaction_log.get(phone_number, [])

        # put the transaction data into a simple string format. The exact format doesn't
        # really matter (as long as it splits numbers up in a non-ambiguous way),
        # since all it's going to be hashed later.
        all_transaction_data = ", ".join(amount for (_, amount, hmm) in previous_transactions)

        # make a bytes object all of the data, and then hash it.
        # again, the exact format of the data doesn't really matter as long
        # as it's unambiguous
        test = f"{phone_number}: {amount}\n{all_transaction_data}", "utf8"
        all_data = bytes(f"{phone_number}: {amount}\n{all_transaction_data}", "utf8")
        hash = sha256(all_data).digest()

        result = ""

        # convert the hash's first few bytes into decimal digits.
        # this method has an issue where multiple byte sequences can
        # encode to the same digit sequence (e.g. "11" can be 2 bytes "1, 1" 
        # or 1 byte "11"). I don't think that's a huge issue, but if someone can
        # think of a way to fix that then please do!
        for byte in hash:
            # exit as soon as the result is six digits
            if len(result) >= 6:
                break
            result += str(byte)
        #return all_data
            
    
        # Get the current date and time
        #save this code in backup
        now = datetime.now()
        time_and_day = now.strftime("%A, %H:%M:%S")  
        filename = './userbackup/' + self.name + '.csv'
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            row = [phone_number, amount, 'R\n', 'Code 1', result[0:6], '\n', time_and_day]
            writer.writerow(row)

        return result[0:6], test

    def validate_code_1(self, phone_numberr, amountt, code):
        other = self.unique_identifier
        amount = str(amountt)
        phone_number = str(phone_numberr)
        previous_transactions = self.transaction_log.get(other, [])
        all_transaction_data = ", ".join(amount for (_, amount, hmm) in previous_transactions)
        test = f"{other}: {amount}\n{all_transaction_data}", "utf8"
        all_data = bytes(f"{other}: {amount}\n{all_transaction_data}", "utf8")
        hash = sha256(all_data).digest()
        result = ""
        for byte in hash:
            # exit as soon as the result is six digits
            if len(result) >= 6:
                break
            result += str(byte)

        ans =result[0:6]
        #return ans, test
        if str(ans) == str(code):
            now = datetime.now()
            time_and_day = now.strftime("%A, %H:%M:%S")  
            filename = './userbackup/' + self.name + '.csv'
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                row = [phone_number, amount, 'S\n', 'Code 1 given', ans, '\n', time_and_day]
                writer.writerow(row)
        return (str(ans) == str(code), str(ans))
    
    def generate_code_2(self, amount, phone_number, code_1):
        ia = int(amount)
        ipn = int(phone_number)
        ic1 = int(code_1)
        iui = int(self.unique_identifier)

        if phone_number in self.transaction_log:
            seed = ia
            seed *= (iui//ia) + (ic1 * ia) - (ipn//(ia + 88))
            counter = 100
            for log in self.transaction_log[phone_number]:
                seed -= (int(log[0])//int(log[1]))
                seed += counter
                counter += 1
        else:
            seed = ia
            seed *= (ipn//ia) + (ic1 * ia) - (iui//(ia + 88))
        random.seed(seed)
        self.make_transaction(amount, 'subtract')
        csvlog(self, phone_number, amount, 'S')
        self.log_transaction(phone_number, amount, 'S')
        code = random.randint(1,99999999)
        now = datetime.now()
        time_and_day = now.strftime("%A, %H:%M:%S")  
        filename = './userbackup/' + self.name + '.csv'
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            row = [phone_number, amount, 'S\n', 'Code 2', code, '\n', time_and_day]
            writer.writerow(row)
        return code

    def validate_code_2(self, amount, phone_number, code_2, code_1):
        ia = int(amount)
        ipn = int(phone_number)
        ic1 = int(code_1)
        iui = int(self.unique_identifier)
        if phone_number in self.transaction_log:
            seed = ia
            seed *= (ipn//ia) + (ic1 * ia) - (iui//(ia + 88))
            counter = 100
            for log in self.transaction_log[phone_number]:
                seed -= (iui//int(log[1]))
                seed += counter
                counter += 1
        else:
            seed = ia
            seed *= (iui//ia) + (ic1 * ia) - (ipn//(amount + 88))
        random.seed(seed)
        expected = random.randint(1,99999999)
        if expected == int(code_2):
            self.make_transaction(amount, 'add')
            csvlog(self, phone_number, amount, 'R')
            self.log_transaction(phone_number, amount, 'R')
            return True
        else:
            return False
    
    def log_transaction(self, p_number, amount, s_r):
        #self.transaction log is a dictionary that we should have phone numbers link 
        #to a list of transactions in the order they were done, a transaction
        #should contain the amount and the action being done, this log will be used
        #to generate codes for future transactions
        if p_number in self.transaction_log:
            self.transaction_log[p_number].append((str(p_number), str(amount), s_r))
        else:
            #no history create item in dictionary
            self.transaction_log[p_number] = [(str(p_number), str(amount), s_r)]

    def load_user(self, filename):
        with open('./userlogs/' + filename, 'r') as file:
            csvreader = csv.reader(file)
            first_row = next(csvreader)
            self.unique_identifier = first_row[1]
            inputamount = int(first_row[0])
            counter = 0
            for row in csvreader:
                if counter == -1:
                    pass
                else:
                    phone = row[0]
                    amoun = row[1]
                    s_r = row[2]
                    if s_r == 'R':
                        inputamount+= int(amoun)
                    else:
                        inputamount -= int(amoun)
                    if phone in self.transaction_log:
                        self.transaction_log[phone].append((str(phone), str(amoun), s_r))
                    else:
                        #no history create item in dictionary
                        self.transaction_log[phone] = [(str(phone), str(amoun), s_r)]
            self.account_balance = inputamount

    def log_reset(self, phone_num):
        important = 0
        same_lines = []
        payments = []
        filename = self.name + '.csv'
        path = './userlogs/' + filename
        check_file = os.path.isfile(path)
        if check_file:
            with open(path, 'r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    if len(row) == 2:
                        important = row
                    else:
                        if str(row[0]) == str(phone_num):
                            payments.append((row[1], row[2]))
                        else:
                            same_lines.append(row)
            #rewrite the log
            with open(path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(important)
                for write in same_lines:
                    row = write
                    writer.writerow(row)
                for write in payments:
                    writer.writerow((900, write[0], write[1]))



    


#recovery failure: finishing a transaction if shutoff happens in middle of one
#sync recovery: if csv logs get messed up for users, putting them back in an agreeing state
#log codes: being able to see previous codes 1, codes 2...
#qr code check on phone: our computers cant scan qr codes atm but maybe we have them generate qr anyway and check on our phones
#qr code and code backup: add function for the use to choose if they want to use a qr code to make process quicker or use codes
#phone pay feature: iphone style apple pay feature?
#camera feature: Check if we can get a quick and simple camera function working so we can mess around with qr codes.
#qr path: adding qr codes could simplify the whole process not just the enter code aspect, maybe we could create an optional path.