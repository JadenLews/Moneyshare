class User:
    def __init__(self, p_name, p_unique, p_input_balance, currency):
        self.name = p_name
        #scramble the unique indentifier to not be tracable
        self.unique_identifier = p_unique
        self.account_balance = p_input_balance
        self.currency = currency
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

    def generate_code(self):
        return 123456789

    def validate(self, other, code):
        return True