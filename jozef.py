import readline
from collections import UserDict
import re
from datetime import datetime, timedelta
import datetime as dt
import pickle
from prettytable import PrettyTable


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
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. It should be 10 digits.")
        super().__init__(value)

    # Static method to validate phone number format
def is_valid_phone(phone):

        # old validation:
        #return re.fullmatch(r"\d{10}", phone) is not None

        if not phone or not isinstance(phone, str):
            return False
        phone_international = r'^\+?[0-9]{1,3}?[-. ]?\(?\d{1,4}?\)?[-. ]?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,9}$'
        phone_local = r'^\d{10}$'
        return bool(re.match(phone_international, phone)) or bool(re.fullmatch(phone_local, phone))


class Email(Field):
    def __init__(self, value):
        if not self.is_valid_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    # Static method to validate email format
    @staticmethod
    def is_valid_email(email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None


class Address(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Address must be a non-empty string.")
        super().__init__(value)


# Class for Birthday field validation
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dt.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Note:
    def __init__(self, text):
        self.text = text
        self.title = title if title else text[:30]
        self.tags = []
        self.creation_date = dt.now()

    def str(self):
        return f"Заметка: {self.title}\n{self.text}"

    def add_tag(self, tag):
        self.tags.append(Tag(tag))

    def remove_tag(self, tag):
        for t in self.tags:
            if t.value == tag:
                self.tags.remove(t)
                return
        raise ValueError(f"Tag {tag} not found.")

    def __str__(self):
        tags_str = f", tags: {'; '.join(t.value for t in self.tags)}" if self.tags else ""
        date_str = self.creation_date.strftime("%d.%m.%Y %H:%M:%S")
        return f"Note: {self.text}, created at: {date_str}{tags_str}"

    # Convert note to dictionary for PrettyTable
    def to_dict(self):
        return {
            "Note": self.text,
            "Tags": "; ".join(t.value for t in self.tags),
            "Creation Date": self.creation_date.strftime("%d.%m.%Y %H:%M:%S")
        }


class NoteBook(UserDict):

    def add_note(self, note):
        self.data[len(self.data) + 1] = note

    def delete_note(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError(f"Note {note_id} not found.")

    def find_by_tag(self, tag):
        found_notes = []
        for note in self.data.values():
            for t in note.tags:
                if t.value == tag:
                    found_notes.append(note)
                    break
        return found_notes

    # Convert notebook to PrettyTable format
    def to_table(self):
        table = PrettyTable()
        table.field_names = ["ID", "Note", "Tags", "Creation Date"]
        for note_id, note in self.data.items():
            table.add_row([note_id, note.to_dict()["Note"], note.to_dict()["Tags"], note.to_dict()["Creation Date"]])
        return table


class Tag(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Tag must be a non-empty string")
        super().__init__(value)

    def __str__(self):
        return str(self.value)


# Class to represent a contact record
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    # Add a phone number to the record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove a phone number from the record
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone {phone} not found.")

    # Edit an existing phone number with a new one
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
        
    # Search for an existing phone number in records
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    # Add an email to the record
    def add_email(self, email):
        if self.email:
            raise ValueError("Email already exists. Use edit_email to change it.")
        self.email = Email(email)

    # Edit the existing email
    def edit_email(self, new_email):
        if not self.email:
            raise ValueError("No email to edit. Use add_email to add one.")
        self.email = Email(new_email)

    # Remove the email
    def remove_email(self):
        if not self.email:
            raise ValueError("No email to remove.")
        self.email = None

    # Search for an email
    def find_email(self):
        return self.email
    
    # Add an address to the record
    def add_address(self, address):
        if self.address:
            raise ValueError("Address already exists. Use edit_address to change it.")
        self.address = Address(address)

    # Edit the existing address
    def edit_address(self, new_address):
        if not self.address:
            raise ValueError("No address to edit. Use add_address to add one.")
        self.address = Address(new_address)

    # Remove the address
    def remove_address(self):
        if not self.address:
            raise ValueError("No address to remove.")
        self.address = None

    # Search for an address
    def find_address(self):
        return self.address

    # Add a birthday to the record
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # String representation of the record
    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}, E-mail: {email_str}, address: {address_str}"

    # Convert record to dictionary for PrettyTable
    def to_dict(self):
        return {
            "Name": self.name.value,
            "Phones": "; ".join(p.value for p in self.phones),
            "Birthday": str(self.birthday) if self.birthday else "N/A",
            "Email": str(self.email) if self.email else "N/A",
            "Address": str(self.address) if self.address else "N/A",
        }

# Address book class to hold all records
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a contact by name at the address book
    def find(self, name):
        return self.data.get(name)

    # Delete a contact from the address book by name 
    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

    # Get upcoming birthdays within 7 days
    def get_upcoming_birthdays(self):
        today = datetime.datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                delta = birthday_this_year - today
                if delta.days < 7:
                    upcoming_birthdays.append((record.name.value, birthday_this_year.strftime("%d.%m.%Y")))
        return upcoming_birthdays

    # Convert address book to PrettyTable format for display
    def to_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Birthday", "Email"]
        for record in self.data.values():
            table.add_row(record.to_dict().values())
        return table

# Function to parse user input and separate command from arguments
def parse_input(user_input):
    if not user_input.strip():
        return None, []
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args
    except ValueError:
        return None, []

# Decorator for error handling
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


# Add a new contact to the address book
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


# Change an existing contact's phone number
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


# Search for a contact by name and show his details
@input_error
def get_contact(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    
    table = PrettyTable()
    table.field_names = ["Name", "Phones", "Birthday"]
    table.add_row(record.to_dict().values())
    return table


# Delete a contact by name
@input_error
def delete_contact(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    book.delete(name)
    return f"Contact {name} deleted."


# Add a birthday to a contact
@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args[0], args[1]
    try:
        dt.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return "Birthday added."


# Show all contacts in the address book
def all_contacts(book):
    if not book.data:
        return "No contacts saved yet."
    else:
        return book.to_table()


# Show birthday by name
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
    return "Tag added."


@input_error
def delete_tag(args, notebook):
    if len(args) < 2:
        raise ValueError("Give me note ID and tag please.")
    note_id, tag = int(args[0]), args[1]
    if note_id not in notebook.data:
        raise KeyError(f"Note {note_id} not found.")
    notebook.data[note_id].remove_tag(tag)
    return "Tag deleted."


# Function to find notes by tag
@input_error
def find_by_tag(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me tag please.")
    tag = args[0]
    found_notes = notebook.find_by_tag(tag)
    if not found_notes:
        return f"No notes found with tag {tag}."
    table = PrettyTable()
    table.field_names = ["Note", "Tags"]
    for note in found_notes:
        table.add_row([note.to_dict()["Note"], note.to_dict()["Tags"]])
    return table


# Shows all notes in the notebook
def show_notes(notebook):
    if not notebook.data:
        return "No notes saved yet."
    else:
        return notebook.to_table()


def save_notes(notebook, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


@input_error
def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()


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
def change_email(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and new email please.")
    name, new_email = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.edit_email(new_email)
    return "Email updated."


@input_error
def delete_email(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.remove_email()
    return "Email deleted."


@input_error
def get_email(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    if record.email:
        return f"{name}'s email is {record.email}"
    else:
        return f"No email set for {name}."


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


@input_error
def change_address(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and new address please.")
    name, new_address = args[0], " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.edit_address(new_address)
    return "Address updated."


@input_error
def delete_address(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    record.remove_address()
    return "Address deleted."


@input_error
def get_address(args, book):
    if len(args) < 1:
        raise ValueError("Give me name please.")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    if record.address:
        return f"{name}'s address is {record.address}"
    else:
        return f"No address set for {name}."


# Function to save the address book to a file
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


# Function to load the address book from a file
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except ( FileNotFoundError,
            EOFError,
            pickle.UnpicklingError ):
        return AddressBook()


COMMANDS = [
    "hello",
    "add",
    "change",
    "phone",
    "add-email",
    "change-email",
    "delete-email",
    "get-email",
    "add-address",
	"change-address",
	"delete-address",
	"get-address",
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
]


# Function to handle tab completion for commands
def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

# Function to display available commands in a table format
def display_commands():
    table = PrettyTable()
    table.field_names = ["Command", "Description"]
    table.add_rows([
        ["hello", "Display a greeting message"],
        ["add", "Add a new contact"],
        ["change", "Change an existing contact's phone number"],
        ["phone", "Show a contact's phone number"],
        ["add-email", "Add an email to a contact"],
        ["change-email", "Change a contact's email"],
        ["delete-email", "Delete a contact's email"],
        ["get-email", "Show a contact's email"],
        ["add-address", "Add an address to a contact"],
        ["change-address", "Change a contact's address"],
        ["delete-address", "Delete a contact's address"],
        ["get-address", "Show a contact's address"],
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
    ])
    print(table)


def main():
    book = load_data()
    notebook = load_notes()
    print("Welcome to the assistant bot!")
    display_commands()
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    while True:
        user_input = input("Please input command: ").strip()
        if not user_input:
            print("Please enter a command.")
            continue

        command, args = parse_input(user_input)

        if command is None:
            print("Invalid input format.")
            continue
        if command == "hello":
            print("How can I help you?")
            display_commands()
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            result = get_contact(args, book)
            if isinstance(result, PrettyTable):
                print(result)
            else:
                print(result)
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        elif command == "delete-email":
            print(delete_email(args, book))
        elif command == "get-email":
            print(get_email(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command == "delete-address":
            print(delete_address(args, book))
        elif command == "get-address":
            print(get_address(args, book))
        elif command == "all":
            result = all_contacts(book)
            if isinstance(result, PrettyTable):
                print(result)
            else:
                print(result)
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "birthdays":
            if args:
                try:
                    days = int(args[0])
                    upcoming_birthdays = book.get_upcoming_birthdays(days)
                except ValueError:
                    print("Invalid number of days. Please enter an integer.")
                    continue
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
                print(f"No upcoming birthdays in the next {days if args else 7} days.")
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "add-note":
            print(add_note(args, notebook))
        elif command == "delete-note":
            print(delete_note(args, notebook))
        elif command == "add-tag":
            print(add_tag(args, notebook))
        elif command == "delete-tag":
            print(delete_tag(args, notebook))
        elif command == "find-tag":
            result = find_by_tag(args, notebook)
            if isinstance(result, PrettyTable):
                print(result)
            else:
                print(result)
        elif command == "show-notes":
            result = show_notes(notebook)
            if isinstance(result, PrettyTable):
                print(result)
            else:
                print(result)
        elif command in ["exit", "close"]:
            save_data(book)
            save_notes(notebook)
            print("Goodbye!")
            break
        else:
            print("Command not found! Please try again")


if __name__ == "__main__":
    main()
