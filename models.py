import re
from objects import *
from state_control import save_data, load_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Incorrect input. Please enter: add [name] [phone]"
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
    return inner

''' 
for future Normalizes the phone number into a format +38XXXXXXXXXX.

def normalize_phone(number: str) -> str:
    cleaned = re.sub(r'\D', '', number)                          # Delete all non-numeric characters
    if len(cleaned) == 10:
        return f'+38{cleaned}'                                   # Add +38 if 10 digits are entered
    elif len(cleaned) == 12 and cleaned.startswith('38'):
        return f'+{cleaned}'                                     # If 12 digits are entered, leave +38
    elif len(cleaned) == 13 and cleaned.startswith('+38'):
        return cleaned                                           # Already in the correct format
    else:
        raise ValueError("Incorrect number format. Enter 10 digits (without +38) or the full number.")
'''

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args
    if not re.fullmatch(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ']+$", name):
        raise ValueError("Enter correct user name")
    if not re.fullmatch(r"^\d{10}$", phone):
        raise ValueError("Enter correct phone: must be 10 digits")

    name, phone, *_ = args
    record = book.find(name)
    try: 
        if record == None:
            new_record = Record(name)
            new_record.add_phone(phone)
            book.add_record(new_record)
        else:
            record.add_phone(phone)
        return "Contact added"
    except Exception as e:
        return e

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record == None:
        return "Contact not exist, add it"
    try:
        result = record.edit_phone(old_phone, new_phone)
    except Exception as e:
        return e
    output = "Contact changed" if result else "Not found number to change"
    return output

@input_error
def single_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record == None:
        return "No such contact"
    return str(record)

def all_phones(book: AddressBook):
    if not book.data:
        return ["Any contacts was saved."]
    result = []
    for record in book.data.values():
        result.append(str(record))
    return result

@input_error
def add_birthday(args, book: AddressBook):
    name, date, *_ = args
    record = book.find(name)
    if record == None:
        return "No such contact"
    if record.birthday != None:
        return "Birthday already added"
    try:
        record.add_birthday(date)
        return "Bidthday date added"
    except ValueError as e:
        return e
    
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record == None:
        return "No such contact"
    if record.birthday == None:
        return "No birthday info about contact"
    return "Birthday for " + record.name.value + " at: " + record.birthday.value.strftime("%d %B")

def birthdays(book: AddressBook):
    data = book.get_upcoming_birthdays()
    if not data:
        return "No one have birthdays this week"
    output = "You need to congratulate: "
    for index, row in enumerate(data):
        output += row['name'] + " on " + row["congratulation_date"]
        if index < len(data) - 1:
            output += ", "
    return output

def main():
    book = load_data()
    commands = [
        "close", 
        "exit", 
        "hello", 
        "add [username] [phone]", 
        "change [username] [old_phone] [new_phone]", 
        "phone [username]", 
        "all",
        "add-birthday [username] [birthday]",
        "show-birthday [username]",
        "birthdays"
    ]
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except Exception as e:
            print(f"Error: {e}")

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)  # Save the address book before exiting
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(single_phone(args, book))
        elif command == "all":
            print("\n".join(all_phones(book)))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command. Available commands:\n   ", "\n    ".join(commands))