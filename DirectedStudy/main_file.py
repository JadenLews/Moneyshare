from user import User

def valid_account(id):
    #WIP
    print()

def add_user(user):
    #if valid account:
    list_accounts.append(user)

def start(user):
    print(f"Hello {user.name}!")
    choices(user)

def choices(user):
    inp = input('What would you like to do?\nSEND, RECEIVE, CHECK BALANCE\n')
    if inp == 'check balance':
        check_balance(user)
    elif inp == 'reveive':
        receive(user)
    elif inp == 'send':
        send(user)


def check_balance(user):
    print(f"\nYour balance is {user.account_balance} {user.currency}\n\n")
    choices(user)

def send(user):
    #send to which user
    other_user = 1
    amount = input('How much money are you sending?\n')
    amount = int(amount)
    if not user.balance_check(amount):
        print('Insufficient Balance\n')
        choices(user)
    else:
        #input code 1
        input_code_1 = int(input('Input code 1\n'))
        if not user.validate(other_user, input_code_1):
            print('There has been an error, try again')
        else:
            #generate code 2
            code_two = user.generate_code
            print(f"Code 2 is {code_two}\n")
            user.make_transaction(amount, 'subtract')
            choices(user)


def receive(user):
    amount = int(input('How much money are you receiving?\n'))
    code_one = user.generate_code
    print(f"Code 1 is {code_one}\n")

def valid_code(user, code):
    #use code and user to ensure correctly generated code
    return True
    

list_accounts = []
jaden = User('Jaden', 123, 100, 'USD')
add_user(jaden)
start(jaden)