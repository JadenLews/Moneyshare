import hashlib
import random

# Setting a random seed for reproducibility
random.seed(42)

class DigiTallyTransaction:
    def __init__(self, payer, payee, amount):
        self.payer = payer
        self.payee = payee
        self.amount = amount
        self.nonce_payer = random.randint(1000, 9999)
        self.nonce_payee = random.randint(1000, 9999)
        self.code1 = None
        self.code2 = None

    def generate_code1(self):
        # Simulating previous transaction log with a simple concatenation
        previous_transactions = f"{self.payer}{self.payee}{self.amount}"
        # print("self.payer", self.payer)
        # print("self.payer", self.payee)
        # print("self.payer", self.amount)
        
        # Hashing details to generate MAC
        mac = hashlib.sha256(f"{self.payer}{self.payee}{self.nonce_payee}{self.amount}{previous_transactions}".encode()).hexdigest()[:4]
        self.code1 = f"{self.nonce_payee}{mac}"
        return self.code1

    def validate_code1(self, code1_input):
        return code1_input == self.code1

    def generate_code2(self):
        if not self.code1:
            raise Exception("Code1 must be generated and validated first.")
        mac = hashlib.sha256(f"{self.payer}{self.payee}{self.amount}{self.nonce_payee}".encode()).hexdigest()[:4]
        self.code2 = f"{self.nonce_payer}{mac}"
        return self.code2

    def validate_code2(self, code2_input):
        if code2_input == self.code2:
            self.payee.balance += self.amount
            self.payer.balance -= self.amount
            return True
        return False

class User:
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

# Example usage
alice = User("Alice", 100)
bob = User("Bob", 50)

transaction = DigiTallyTransaction(alice, bob, 10)
code1 = transaction.generate_code1()
print(f"Code1 generated: {code1}")

# Alice enters Code1 into her phone (simulated here by passing code1 directly)
if transaction.validate_code1(code1):
    print("Code1 validated successfully.")
    code2 = transaction.generate_code2()
    print(f"Code2 generated: {code2}")
    
    # Bob enters Code2 into his phone
    if transaction.validate_code2(code2):
        print("Transaction completed successfully.")
        print(f"Alice's new balance: {alice.balance}")
        print(f"Bob's new balance: {bob.balance}")
    else:
        print("Error: Invalid Code2.")
else:
    print("Error: Invalid Code1.")
