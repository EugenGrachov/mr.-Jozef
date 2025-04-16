import readline
from collections import UserDict
import re
from datetime import datetime
import datetime as dt
import pickle
from prettytable import PrettyTable
from mrjozef.notes import NoteBook, load_notes, save_notes, Note

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. It should be 10 digits.")
        super().__init__(value)

class Email(Field):
    def __init__(self, value):
        if not self.is_valid_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    @staticmethod
    def is_valid_email(email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

class Address(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Address must be a non-empty string.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                found = True
                break
        if not found:
            raise ValueError(f"Phone {old_phone} not found.")
        if not Phone.is_valid_phone(new_phone):
            raise ValueError("Invalid phone number format. It should be 10 digits.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}{email_str}{address_str}"

    def to_dict(self):
        return {
            "Name": self.name.value,
            "Phones": "; ".join(p.value for p in self.phones),
            "Birthday": str(self.birthday) if self.birthday else "N/A",
            "Email": str(getattr(self, 'email', 'N/A')) if getattr(self, 'email', 'N/A') != 'N/A' else "N/A",
            "Address": str(getattr(self, 'address', 'N/A')) if getattr(self, 'address', 'N/A') != 'N/A' else "N/A",
        }
    
    def to_dict(self):
        return {
            "Name": self.name.value,
            "Phones": "; ".join(p.value for p in self.phones),
            "Birthday": str(self.birthday) if self.birthday else "N/A",
            "Email": str(self.email) if self.email else "N/A",
            "Address": str(self.address) if self.address else "N/A",
        }

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

    def get_upcoming_birthdays(self, days=7):
        today = dt.datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                delta = birthday_this_year - today
                if delta.days < days:
                    upcoming_birthdays.append((record.name.value, birthday_this_year.strftime("%d.%m.%Y")))
        return upcoming_birthdays
    
    def to_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Birthday", "Email", "Address"]
        for record in self.data.values():
            table.add_row(record.to_dict().values())
        return table   

def parse_input(user_input):
    if not user_input.strip():
        return None, []
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except ValueError:
        return None, []

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid command format."
        except TypeError:
            return "Invalid input type."

    return inner

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    if not Phone.is_valid_phone(phone):
        raise ValueError("Invalid phone number format. It should be 10 digits.")
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def get_contact(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")

    table = PrettyTable()
    table.field_names = ["Name", "Phones", "Birthday", "Email", "Address"]
    table.add_row(record.to_dict().values())
    return table

@input_error
def delete_contact(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    book.delete(name)
    return f"Contact {name} deleted."

@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return "Birthday added."

def all_contacts(book):
    if not book.data:
        return "No contacts saved yet."
    else:
        return book.to_table()

@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    if record.birthday:
        return f"{name}'s birthday is on {record.birthday}"
    else:
        return f"No birthday set for {name}."


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

@input_error
def add_note(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me note text please.")
    text = " ".join(args)
    note = Note(text)
    notebook.add_note(note)
    return "Note added."

@input_error
def delete_note(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me note ID please.")
    note_id = int(args[0])
    notebook.delete_note(note_id)
    return f"Note {note_id} deleted."

@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        raise ValueError("Give me note ID and tag please.")
    note_id, tag = int(args[0]), args[1]
    if note_id not in notebook.data:
        raise KeyError(f"Note {note_id} not found.")
    notebook.data[note_id].add_tag(tag)
    return f"Tag '{tag}' added to note {note_id}."

@input_error
def delete_tag(args, notebook):
    if len(args) < 2:
        raise ValueError("Give me note ID and tag please.")
    note_id, tag = int(args[0]), args[1]
    if note_id not in notebook.data:
        raise KeyError(f"Note {note_id} not found.")
    notebook.data[note_id].remove_tag(tag)
    return f"Tag '{tag}' removed from note {note_id}."

@input_error
def find_by_tag(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me tag please.")
    tag = args[0]
    found_notes = notebook.find_by_tag(tag)
    if not found_notes:
        return f"No notes found with tag '{tag}'."
    table = PrettyTable()
    table.field_names = ["Note", "Tags", "Creation Date"]
    for note in found_notes:
        table.add_row(note.to_dict().values())
    return table

def show_notes(notebook):
    if not notebook.data:
        return "No notes saved yet."
    else:
        return notebook.to_table()

COMMANDS = [
    "hello",
    "add",
    "change",
    "phone",
    "all",
    "delete",
    "add-birthday",
    "birthdays",
    "show-birthday",
    "add-note",
    "delete-note",
    "add-tag",
    "delete-tag",
    "find-tag",
    "show-notes",
    "exit",
    "close",
    "add-email",
    "add-address"
]

def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def display_commands():
    table = PrettyTable()
    table.field_names = ["Command", "Description"]
    table.add_rows([
        ["hello", "Display a greeting message"],
        ["add", "Add a new contact"],
        ["change", "Change an existing contact's phone number"],
        ["phone", "Show a contact's phone number"],
        ["all", "Show all contacts"],
        ["delete", "Delete a contact"],
        ["add-birthday", "Add a birthday to a contact"],
        ["birthdays", "Show upcoming birthdays"],
        ["show-birthday", "Show a contact's birthday"],
        ["add-note", "Add a new note"],
        ["delete-note", "Delete a note"],
        ["add-tag", "Add a tag to a note"],
        ["delete-tag", "Delete a tag from a note"],
        ["find-tag", "Find notes by tag"],
        ["show-notes", "Show all notes"],
        ["exit/close", "Exit the program"],
        ["add-email", "Add an email to a contact"],
        ["add-address", "Add an address to a contact"]
    ])
    print(table)

@input_error
def add_email(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and email please.")
    name, email = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.add_email(email)
    return "Email added."

@input_error
def add_address(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and address please.")
    name, address = args[0], " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.add_address(address)
    return "Address added."

def main():
    book = load_data()
    notebook = load_notes()
    print("Welcome to the assistant bot!")
    display_commands()
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    command_handlers = {
        "hello": lambda args: (print("How can I help you?"), display_commands())[0],
        "add": lambda args: add_contact(args, book),
        "change": lambda args: change_contact(args, book),
        "phone": lambda args: print_result(get_contact(args, book)),
        "all": lambda args: print_result(all_contacts(book)),
        "delete": lambda args: delete_contact(args, book),
        "add-birthday": lambda args: add_birthday(args, book),
        "birthdays": lambda args: handle_birthdays(args, book),
        "show-birthday": lambda args: show_birthday(args, book),
        "add-note": lambda args: add_note(args, notebook),
        "delete-note": lambda args: delete_note(args, notebook),
        "add-tag": lambda args: add_tag(args, notebook),
        "delete-tag": lambda args: delete_tag(args, notebook),
        "find-tag": lambda args: print_result(find_by_tag(args, notebook)),
        "show-notes": lambda args: print_result(show_notes(notebook)),
        "exit": lambda args: exit_program(book, notebook),
        "close": lambda args: exit_program(book, notebook),
        "add-email": lambda args: add_email(args, book),
        "add-address": lambda args: add_address(args, book)
    }

    while True:
        user_input = input("Please input command: ").strip()
        if not user_input:
            print("Please enter a command.")
            continue

        command, args = parse_input(user_input)
        if command is None:
            print("Invalid input format.")
            continue

        if command in command_handlers:
            result = command_handlers[command](args)
            if result is not None:
                print(result)
        else:
            print("Command not found! Please try again")

def print_result(result):
    if isinstance(result, PrettyTable):
        print(result)
    else:
        print(result)

def handle_birthdays(args, book):
    if args:
        try:
            days = int(args[0])
            upcoming_birthdays = book.get_upcoming_birthdays(days)
        except ValueError:
            print("Invalid number of days. Please enter an integer.")
            return
    else:
        upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        table = PrettyTable()
        table.field_names = ["Name", "Birthday"]
        for name, birthday in upcoming_birthdays:
            table.add_row([name, birthday])
        print(f"Upcoming birthdays in the next {days if args else 7} days:")
        print(table)
    else:
        print("No upcoming birthdays in the next 7 days.")

def exit_program(book, notebook):
    save_data(book)
    save_notes(notebook)
    print("Goodbye!")
    exit()

if __name__ == "__main__":
    main()
