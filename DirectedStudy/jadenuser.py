import random 

class User:
    def __init__(self, p_name, p_number, p_input_balance, currency):
        self.name = p_name
        #scramble the unique indentifier to not be tracable
        self.unique_identifier = p_number
        self.account_balance = p_input_balance
        self.currency = currency
        self.transaction_log = {}
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
    
    def generate_code_1(self, amount, phone_number):
        #generate code_1 and validate_code_1 should use the same method to create
        #the code and so it'll be the same on the other device when they run
        #validate_code_1

        #this method should use the amount, phone number and transaction log to 
        #create a code that cant be predicted by an outside party but is recreatable
        #for the other device 
        return 123456789

    def validate_code_1(self, phone_number, code):
        #check generate_code_1 comment
        return True
    
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
            return True
        else:
            return False
    
    def log_transaction(self, p_number, amount):
        #self.transaction log is a dictionary that we should have phone numbers link 
        #to a list of transactions in the order they were done, a transaction
        #should contain the amount and the action being done, this log will be used
        #to generate codes for future transactions
        if p_number in self.transaction_log:
            self.transaction_log[p_number].append((p_number, amount))
        else:
            #no history create item in dictionary
            self.transaction_log[p_number] = [(p_number, amount)]


#jaden = User('Jaden', 2076102112, 100, 'USD')
#two = User('Jaden', 2076109219, 100, 'USD')
#code = jaden.generate_code_2(50, 2076109219, 123456)