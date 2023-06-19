from re import compile, match, IGNORECASE
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone):
        self.phone = phone if phone else []

class Record(Field):
    def __init__(self, name, phone):
        self.name = name.value
        # if phone.phone:
        self.phones = phone.phone

class AddressBook(UserDict, Field):
    def add_record(self, rec):
        self.name = rec.name
        self.phones = rec.phones
        self.data[self.name] = self.phones

numbers = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError):
            print('\nCommand was entered incorrectly, please try again.\n') 
    return inner

greeting = compile('hello', flags=IGNORECASE)
add = compile('add', flags=IGNORECASE)
change = compile('change', flags=IGNORECASE)
phone = compile('phone', flags=IGNORECASE)
show_all = compile('show all', flags=IGNORECASE)
delete = compile('delete', flags=IGNORECASE)
goodbye = compile(r'(good bye|close|exit)', flags=IGNORECASE)

# name_pattern = re.compile(r'[a-zA-Z]+')
# number_pattern = re.compile(r"(?:\+380\(\d{2}\)\d{3}-\d{1}-\d{3}|\+380\(\d{2}\)\d{3}-\d{2}-\d{2})")

@input_error
def hello():
    print("\nHow can i help you?\n")

@input_error
def adding(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    if len(arguments) > 2:
        phone = Phone(arguments[2:])
    name = Field(arg_1)
    record = Record(name, phone)
    numbers.add_record(record)
    print('\nCompleted!\n')

@input_error
def changing(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    if len(arguments) > 2:
        phone = Phone(arguments[2:])
    name = Field(arg_1)
    record = Record(name, phone)
    numbers.add_record(record)
    print('\nCompleted!\n')

@input_error
def show_phone(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    name = Field(arg_1)
    record = Record(name)
    for k in numbers.keys():
        if k == arg_1:
            print(f'\n{record.name.value}: {", ".join(numbers.get(record.name.value))}\n')

@input_error
def deleting(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    name = Field(arg_1)
    record = Record(name)
    numbers.pop(record.name.value)
    print('\nCompleted!\n')

@input_error
def show_all_phones():
    for k, v in numbers.items():
        print(f'{k}: {", ".join(v)}')

if __name__=='__main__':
    while True:
        user_command = input('Write a command: ')

        if match(greeting, user_command):
            hello()
        elif match(add, user_command):
            adding(user_command)
        elif match(change, user_command):
            changing(user_command)
        elif match(phone, user_command):
            show_phone(user_command)
        elif match(show_all, user_command):
            show_all_phones()
        elif match(delete, user_command):
            deleting(user_command)
        elif match(goodbye, user_command):
            print('Good bye!')
            break