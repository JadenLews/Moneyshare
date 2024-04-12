from hashlib import sha256
from savecsv import csvlog
import random 
import csv
import os


class User:
    def __init__(self, p_name, p_number, p_input_balance, currency):
        self.name = p_name
        #scramble the unique indentifier to not be tracable
        self.unique_identifier = p_number
        self.currency = currency
        self.transaction_log = {}
        filename = self.name + '.csv'
        path = './userlogs/' + filename
        check_file = os.path.isfile(path)
        if check_file:
            self.load_user(filename)
        else:
            self.account_balance = p_input_balance
            filename = './userlogs/' + self.name + '.csv'
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                row = [p_input_balance]
                writer.writerow(row)
        #user identifier has to be unique
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
        return result[0:6], test

    def validate_code_1(self, phone_numberr, amountt, code):
        other = self.unique_identifier
        amount = str(amountt)
        phone_number = str(phone_numberr)
        previous_transactions = self.transaction_log.get(other, [])

        # put the transaction data into a simple string format. The exact format doesn't
        # really matter (as long as it splits numbers up in a non-ambiguous way),
        # since all it's going to be hashed later.
        all_transaction_data = ", ".join(amount for (_, amount, hmm) in previous_transactions)

        # make a bytes object all of the data, and then hash it.
        # again, the exact format of the data doesn't really matter as long
        # as it's unambiguous
        test = f"{other}: {amount}\n{all_transaction_data}", "utf8"
        all_data = bytes(f"{other}: {amount}\n{all_transaction_data}", "utf8")
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

        ans =result[0:6]
        #return ans, test
        return str(ans) == str(code)
        return str(self.generate_code_1(amount, phone_number)) == str(code)
    
    def generate_code_2(self, amount, phone_number, code_1):
        ia = int(amount)
        ipn = int(phone_number)
        ic1 = int(code_1)
        iui = int(self.unique_identifier)
        #test = f"\nvalues are {ia} {ipn} {ic1} {iui}"

        if phone_number in self.transaction_log:
            #do later
            #test += "\nfdfsfsdfsdfsdf"
            seed = ia
            seed *= (iui//ia) + (ic1 * ia) - (ipn//(ia + 88))
            #test += f" is seed same {seed}\n"
            counter = 100
            for log in self.transaction_log[phone_number]:
                #test += str(log)
                #test += "\n"
                #test += f"before{seed}\n"
                #test += f"this is logs {ipn} {log[1]}\n"
                seed -= (int(log[0])//int(log[1]))
                #test += f"after{seed}\n"
                seed += counter
                counter += 1
        else:
            seed = ia
            seed *= (ipn//ia) + (ic1 * ia) - (iui//(ia + 88))
        #test += f"\n {seed}"
        random.seed(seed)
        #return test
        self.make_transaction(amount, 'subtract')
        csvlog(self, phone_number, amount, 'S')
        self.log_transaction(phone_number, amount, 'S')
        return random.randint(1,99999999)

    def validate_code_2(self, amount, phone_number, code_2, code_1):
        ia = int(amount)
        ipn = int(phone_number)
        ic1 = int(code_1)
        iui = int(self.unique_identifier)
        #test = f"values are {ia} {ipn} {ic1} {iui}"

        if phone_number in self.transaction_log:
            #do later
            #test += "\nfdfsfsdfsdfsdf"
            seed = ia
            seed *= (ipn//ia) + (ic1 * ia) - (iui//(ia + 88))
            #test += f" is seed same {seed}\n"
            counter = 100
            for log in self.transaction_log[phone_number]:
                #test += str(log)
                #test += f"before{seed}\n"
                #test += f"this is logs {ipn} {log[1]}\n"
                seed -= (iui//int(log[1]))
                #test += f"after{seed}\n"
                seed += counter
                counter += 1
        else:
            seed = ia
            seed *= (iui//ia) + (ic1 * ia) - (ipn//(amount + 88))
        #test += f"\n {seed}"
        random.seed(seed)
        #return test
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
            for row in csvreader:
                if len(row) == 1:
                    inputamount = int(row[0])
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
                        self.transaction_log[phone] = [(str(phone), str(amoun))]
            self.account_balance = inputamount


