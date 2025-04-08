import pickle
from collections import UserDict
import re
from datetime import datetime, timedelta

# Decorator for error handling
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return f"Error: {e}"
    return wrapper

# Base class for different fields like Name, Phone, Birthday
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Class for Name field validation
class Name(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        super().__init__(value)

# Class for Phone field validation
class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must consist of 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return isinstance(phone, str) and re.match(r'^\d{10}$', phone) is not None

# Class for Birthday field validation
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Class to represent a contact record
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Add phone number to record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove phone number from record
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # Edit an existing phone number
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    # Add a birthday to the record
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # String representation of the record
    def __str__(self):
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {birthday_str}"

# Address book class to hold all records
class AddressBook(UserDict):
    # Add a new record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a record by name
    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    # Get upcoming birthdays within 7 days
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                
                # If the birthday has already passed, get the next year's birthday
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year
                    
                    # Check if the birthday is on a weekend (Saturday/Sunday), and shift to Monday
                    if congratulation_date.weekday() in [5, 6]:
                        shift_days = 7 - congratulation_date.weekday()
                        congratulation_date += timedelta(days=shift_days)
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })
        return upcoming_birthdays

# Function to save the address book to a file
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

# Function to load the address book from a file
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# Main function to interact with the user
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, *args = user_input.split()

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) < 2:
                print("Usage: add <name> <phone>")
                continue
            name, phone = args
            if book.find(name):
                book.find(name).add_phone(phone)
            else:
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
            print(f"Added {name} with phone {phone}")

        elif command == "change":
            if len(args) < 3:
                print("Usage: change <name> <old_phone> <new_phone>")
                continue
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                record.edit_phone(old_phone, new_phone)
                print("Phone updated.")
            else:
                print("Contact not found.")

        elif command == "phone":
            if not args:
                print("Usage: phone <name>")
                continue
            name = args[0]
            record = book.find(name)
            print(record if record else "Contact not found.")

        elif command == "all":
            for record in book.data.values():
                print(record)

        elif command == "add-birthday":
            if len(args) < 2:
                print("Usage: add-birthday <name> <DD.MM.YYYY>")
                continue
            name, birthday = args
            record = book.find(name)
            if record:
                record.add_birthday(birthday)
                print(f"Birthday for {name} set to {birthday}")
            else:
                print("Contact not found.")

        elif command == "show-birthday":
            if not args:
                print("Usage: show-birthday <name>")
                continue
            name = args[0]
            record = book.find(name)
            if record and record.birthday:
                print(f"{name}'s birthday is on {record.birthday.value}")
            else:
                print("Birthday not found for this contact.")

        elif command == "birthdays":
            birthdays = book.get_upcoming_birthdays()
            if birthdays:
                for b in birthdays:
                    print(f"{b['name']} - {b['congratulation_date']}")
            else:
                print("No upcoming birthdays.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()