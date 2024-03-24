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

    def validate_code_1(self, phone_number, amount, code):
        return self.generate_code_1(amount, phone_number) == code
    
    def generate_code_2(self, amount, phone_number, code_1):
        #generate code_2 and validate_code_2 should use the same method to create
        #the code and so it'll be the same on the other device when they run
        #validate_code_2

        #this method should use the amount, phone number, transaction log, and maybe code1
        #to create a code that cant be predicted by an outside party but is recreatable
        #for the other device 
        return 123456789

    def validate_code_2(self, phone_number, code_2, code_1):
        #check generate_code_2
        return True
    
    def log_transaction(self, p_number, amount):
        #self.transaction log is a dictionary that we should have phone numbers link 
        #to a list of transactions in the order they were done, a transaction
        #should contain the amount and the action being done, this log will be used
        #to generate codes for future transactions
        if p_number in self.transaction_log:
            #has history, add to it
            print()
        else:
            #no history create item in dictionary
            print()