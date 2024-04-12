import random
from user import User

#testing for the project
num_trials = 1
transaction_per_trial = 20
people = 6

def print_people(list_user):
    all = ''
    for user in list_user:
        all += f"{user.name}, {user.unique_identifier}, {user.account_balance} {user.transaction_log}\n"
    return all
allcorrect = 0
allfalse = 0
for trial in range(num_trials):
    list_people = []
    list_pn = []
    for person in range(people):
        #use while loop to ensure we have the amount of people we want
        while True:
            rand_phone_num = random.randint(1, 9999999999)
            rand_account_bal = random.randint(15, 1000)
            if rand_phone_num in list_pn:
                pass
            else:
                made = User(str(person), rand_phone_num, rand_account_bal, 'USD')
                list_people.append(made)
                list_pn.append(rand_phone_num)
                break
    #print out all people
    #print_people(list_people)
    false = 0
    correct = 0
    for transaction in range(transaction_per_trial):
        #use while loop to ensure we get the wanted amount of valid transactions
        transaction_amount = 0
        peoples = []
        sender = 0
        while True:
            transaction_amount = random.randint(1, 100)
            indexuser1 = random.randint(0, len(list_people) - 1)
            indexuser2 = random.randint(0, len(list_people) - 1)
            potential = [list_people[indexuser1], list_people[indexuser2]]
            #dont want transaction between you and yourslef
            if int(potential[0].unique_identifier) == int(potential[1].unique_identifier):
                pass
            else:
                sender = random.choice([0,1])
                #dont want to go into negative balance
                if potential[sender].account_balance < transaction_amount:
                    pass
                else:
                    peoples = potential
                    break

        print(f"transaction amount:{transaction_amount}, Who sends: {peoples[sender].name}, Who receives: {peoples[1-sender].name}\n people:\n{print_people(peoples)}")
        
        #we have the two people doing the transaction, we know the transaction should be 
        #valid, now we have to test and ensure it runs correctly

        #if sender is 1, 1-1 is 0, finds the receiver
        code_one = peoples[1-sender].generate_code_1(transaction_amount, peoples[sender].unique_identifier)
        answer1 = peoples[sender].validate_code_1(peoples[1-sender].unique_identifier, transaction_amount, code_one[0])
        code_two = peoples[sender].generate_code_2(transaction_amount, peoples[1-sender].unique_identifier, code_one[0])
        answer2 = peoples[1-sender].validate_code_2(transaction_amount, peoples[sender].unique_identifier, code_two, code_one[0])
        #peoples[1 - sender].log_transaction(peoples[sender].unique_identifier, transaction_amount, 'R')
        #peoples[sender].log_transaction(peoples[1 - sender].unique_identifier, transaction_amount, 'S')
        if answer1 and answer2:
            correct += 1
        else:
            false += 1
    #need to better send down user variable
    list_people[indexuser1] = peoples[0]
    list_people[indexuser2] = peoples[1]

    #list_people[indexuser1] = per
    allcorrect += correct
    allfalse += false
print(f"Correct trials: {allcorrect}, False trials: {allfalse}")

        #print(code_one[0])
        #print(code_two)
