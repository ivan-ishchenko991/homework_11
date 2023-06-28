from collections.abc import Iterator
from re import compile, match, IGNORECASE
from collections import UserDict
import  re
from datetime import datetime
import json
from pathlib import Path


class IncorrectInput(Exception):
    pass

class Field:
    def __init__(self, value: str):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

class Name(Field):
    pass

class Email(Field):
    @property
    def value(self):
        return self.__value
    EMAIL_REGEX = re.compile(r"[a-zA-Z]{1,}[a-zA-Z0-9._]+@[a-z]+\.[a-z]{2,}")

    @value.setter
    def value(self, value):
        if value == None:
            self.__value = None
        else:
            if re.search(self.EMAIL_REGEX, str(value)):
                self.__value = value
            else:
                print(f"No e-mail found in {value}.")

class Phone(Field):

    @property
    def value(self):
        return self.__value
    
    PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")
    @value.setter
    def value(self, value: str):
        if value == None:
            self.__value = None
        else:
            value = value.replace(" ", "")
            search = re.search(self.PHONE_REGEX, value)
            try:
                country, operator, phone = search.group(1, 2, 3)
            except AttributeError:
                raise IncorrectInput(f"No phone number found in {value}.")

            if operator is None:
                raise IncorrectInput(f"Operator code not found in {value}.")

            self.country_code = country if country is not None else "38"
            self.operator_code = operator
            self.phone_number = phone
            self.__value = f"+{self.country_code}({self.operator_code}){self.phone_number}"

class Birthday(Field):
    BDAY_REGEX = compile(r"\d{2}\.\d{2}\.\d{4}")
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value == None:
            self.__value = None
        else:
            if re.search(self.BDAY_REGEX, value):
                self.__value = value
            else:
                print(f"No birthday found in {value}.")

class Record:
    def __init__(self, name: Name, phone: Phone = None, email: Email = None, bday: Birthday = None):
        self.name = name
        self.lst = []
        self.phones = None
        self.email = None
        self.bday = None
        if phone.value:
            self.phones = []
            self.lst.append(phone.value)
        if email.value:
            self.email = email.value
            self.lst.append(self.email)
        if bday.value:
            self.bday = bday.value
            self.lst.append(self.bday)
        # self.name = Name(name)

    def days_to_birthday(date):
        d, m, y = date.split('.')
        now = datetime.now()
        some_day = datetime(year=now.year, month=int(m), day=int(d))
        result = some_day - now
        if result.days >= 0:
            return result.days + 1
        else:
            some_date = some_day.replace(year=now.year + 1)
            result = some_date - now
            return result.days

class AddressBook(UserDict):
    dir_path = Path(__file__).parent
    filename = Path(fr'{dir_path}\addressbook.json')
    def unpackaging(self):
        with open(self.filename, 'r') as f:
            self.data.update(json.load(f))
    
    def packaging(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec.lst

    def iterator(self, seq, n):
        if type(seq) == dict:
            self.dict_lst = list(self.data.items())
        else:
            self.dict_lst = seq
        if n:
            n = n.group()
            self.count_loop = int(n)
        else:
            self.count_loop = 5
        self.loop = -1
        self.index = 0
        return self.__iter__()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # dict_lst = list(self.data.items())
        if self.index == len(self.dict_lst):
            raise StopIteration
        else:
            line = f"{self.dict_lst[self.index][0]}: {', '.join(self.dict_lst[self.index][1])}"
            self.index += 1
            self.loop += 1
            if self.loop == self.count_loop:
                print('-' * 20)
                self.loop = 0
            return line
    
    def searching(self, obj):
        result = []
        for k, v in self.data.items():
            if obj in k:
                result.append((k, v))
                continue
            for el in v:
                if obj in el:
                    result.append((k, v))
        return result

ab = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
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
days_to_bday_command = compile('days to birthday', flags=IGNORECASE)
search = compile('search', flags=IGNORECASE)

number_pattern = re.compile(r"\+?\(?(\d{2})?\)?\-?\(?(0\d{2})\)?\-?\d{3}\-?\d{2}\-?\d{2}")
b_day_pattern = r'\d{2}\.\d{2}\.\d{4}'

@input_error
def hello():
    print("\nHow can i help you?\n")

@input_error
def adding(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    b_day = re.search(Birthday.BDAY_REGEX, str(command))
    if b_day:
        bday = Birthday(b_day.group())
    else:
        bday = Birthday(None)
    number = re.search(number_pattern, str(command))
    if number:
        phone = Phone(number.group())
    else:
        phone = Phone(None)
    mail = re.search(Email.EMAIL_REGEX, str(command))
    if mail:
        email = Email(mail.group())
    else:
        email = Email(None)
    name = Name(arg_1)
    record = Record(name, phone, email, bday)
    ab.add_record(record)
    print('\nCompleted!\n')

@input_error
def changing(command):
    arguments = command.split(' ')
    arg_1 = arguments[1]
    b_day = re.search(Birthday.BDAY_REGEX, str(command))
    if b_day:
        bday = Birthday(b_day.group())
    else:
        bday = Birthday(None)
    number = re.search(number_pattern, str(command))
    if number:
        phone = Phone(number.group())
    else:
        phone = Phone(None)
    mail = re.search(Email.EMAIL_REGEX, str(command))
    if mail:
        email = Email(mail.group())
    else:
        email = Email(None)
    name = Name(arg_1)
    record = Record(name, phone, email, bday)
    ab.add_record(record)
    print('\nCompleted!\n')

@input_error
def show_phone(command):
        arguments = command.split(' ')
        arg_1 = arguments[1]
        for name, phones in ab.data.items():
            if name == arg_1:
                    print(f'{name}: {", ".join(phones)}')

@input_error
def deleting(command):
    arguments = command.split(' ')
    name = arguments[1]
    ab.pop(name)
    print('\nCompleted!\n')

@input_error
def show_all_phones(command):
    n = re.search(r"\d+", command)
    for line in ab.iterator(ab.data, n):
        print(line)

@input_error
def days_to_bday(command):
    args = command.split(' ')
    person = args[3]
    lst = ab.get(person)
    bday = None
    for date in lst:
        if re.search(Birthday.BDAY_REGEX, date):
            bday = date
            print(Record.days_to_birthday(bday))
            break
    if bday == None:
        print("Birthday date not found in contact.")

@input_error
def searching(command):
    n = re.search(r" \d+$", command)
    args = command.split(' ')
    searched_obj = args[1]
    result = ab.searching(searched_obj)
    for line in ab.iterator(result, n):
        print(line)

if __name__=='__main__':
    if Path(ab.filename).exists():
        ab.unpackaging()
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
            show_all_phones(user_command)
        elif match(delete, user_command):
            deleting(user_command)
        elif match(days_to_bday_command, user_command):
            days_to_bday(user_command)
        elif match(search, user_command):
            searching(user_command)
        elif match(goodbye, user_command):
            ab.packaging()
            print('Good bye!')
            break