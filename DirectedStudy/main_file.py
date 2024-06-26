from user import User
import time
from arguments import get_cli_arguments

#currently the phone number is the identifying number for an account
#this us under the assumption that all phone numbers for sim technology 
#are unique and cannot be modified by users


def start(user):
    print(f"Hello {user.name}!")
    choices(user)

def choices(user):
    inp = input('What would you like to do?\nSEND, RECEIVE, CHECK BALANCE\n')
    if inp == 'check balance':
        check_balance(user)
    elif inp == 'receive':
        receive(user)
    elif inp == 'send':
        send(user)


def check_balance(user):
    print(f"\nYour balance is {user.account_balance} {user.currency}\n\n")
    time.sleep(3)
    choices(user)

def send(user):
    #send to which user
    amount = int(input('How much money are you sending?\n'))
    if amount > user.account_balance:
        print('You do not have the funds for that')
    else:
        p_number = int(input('What is the phone number of who you are sending money to\n'))
        code_1 = int(input('Enter Code 1\n'))
        code_1_check = user.validate_code_1(p_number, amount, code_1)
        #Check
        if code_1_check:
            #True
            #generate code 2
            code_two = user.generate_code_2(amount, p_number, code_1)
            print(f"Code 2 is {code_two}\n")
            print(f"Balance is now {user.account_balance}\n")
        else:
            #error False
            print('There has been an error, try again')
    time.sleep(3)
    choices(user)


def receive(user):
    amount = int(input('How much money are you receiving?\n'))
    p_number = int(input('What is the phone number of who is sending money?\n'))
    code_one = user.generate_code_1(amount, p_number)
    print(f"Code 1 is {code_one[0]}\n")
    time.sleep(3)
    code_2 = int(input('Enter Code 2\n'))
    code_2_check = user.validate_code_2(amount, p_number, code_2, code_one[0])
    #Check
    if code_2_check:
        print(f"{amount} has been added to your wallet\nYour balance is now {user.account_balance}\n")
    else:
        print('error')
    time.sleep(3)
    choices(user)



list_accounts = []
args = get_cli_arguments()

user = User(
    args.username,
    args.phone_number,
    args.initial_balance,
    args.currency,
)

start(user)