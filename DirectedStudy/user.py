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
        return 123456789

    def validate_code_1(self, phone_number, code):
        return True
    
    def generate_code_2(self, amount, phone_number):
        return 123456789

    def validate_code_2(self, phone_number, code):
        return True
    
    def log_transaction(self, p_number, amount):
        #if user does not exist in current dictionary log then make new dictionary item
        #if user does exist, add log to the list of transactions with user
        print()