import readline
from collections import UserDict
import re
from datetime import datetime, timedelta
import datetime as dt
import pickle
from prettytable import PrettyTable                # HERE IS A QUESTION WITH IMPORTING "prettytable"


# Base class for different fields like Name, Phone, Birthday
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Class for Name field validation
class Name(Field):
# Currently no validation in the constructor, but it can be added if needed in the future
    # def __init__(self, value):
    #     if not value or not isinstance(value, str):
    #         raise ValueError("Name must be a non-empty string")
    #     super().__init__(value)
    pass


# Class for Phone field validation
class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. It should be 10 digits.")
        super().__init__(value)

    # Static method to validate phone number format
    @staticmethod
    def is_valid_phone(phone):
        return re.fullmatch(r"\d{10}", phone) is not None
    

# Class for Birthday field validation
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


# Class to represent a contact record
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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

    # Add a birthday to the record
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # String representation of the record
    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"

    # Convert record to dictionary for PrettyTable
    def to_dict(self):
        return {
            "Name": self.name.value,
            "Phones": "; ".join(p.value for p in self.phones),
            "Birthday": str(self.birthday) if self.birthday else "N/A",
        }

# Address book class to hold all records
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a contact by name at the address book
    def find_contact(self, name):                      # HERE IS A QUESTION WITH NAMING "find"
        return self.data.get(name)

    # Delete a contact from the address book by name 
    def delete_contact(self, name):                      # HERE IS A QUESTION WITH NAMING "delete"
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found.")

    # Get upcoming birthdays within 7 days
    def get_upcoming_birthdays(self):
        today = dt.datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)

                # If the birthday has already passed, get the next year's birthday
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                delta = birthday_this_year - today

                # Check if the birthday is on a weekend (Saturday/Sunday), and shift to Monday
                if delta.days < 7:
                    upcoming_birthdays.append((record.name.value, birthday_this_year.strftime("%d.%m.%Y")))
        return upcoming_birthdays

    # Convert address book to PrettyTable format for display
    def to_table(self):
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Birthday"]
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
    record = book.find_contact(name)
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
    record = book.find_contact(name)
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
    record = book.find_contact(name)
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
    book.delete_contact(name)
    return f"Contact {name} deleted."


# Add a birthday to a contact
@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args[0], args[1]
    record = book.find_contact(name)
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
    record = book.find_contact(name)
    if not record:
        raise KeyError(f"Contact {name} not found.")
    if record.birthday:
        return f"{name}'s birthday is on {record.birthday}"
    else:
        return f"No birthday set for {name}."


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

# Class for Tag field validation
class Tag(Field):
    pass

# Class to represent a note
class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []
        self.creation_date = datetime.now()

    # Add a tag to the note
    def add_tag(self, tag):
        self.tags.append(Tag(tag))

    # Remove a tag from the note
    def remove_tag(self, tag):
        for t in self.tags:
            if t.value == tag:
                self.tags.remove(t)
                return
        raise ValueError(f"Tag {tag} not found.")

    # String representation of the note
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


# Class to represent a notebook
class NoteBook(UserDict):
    
    # Add a new note to the notebook
    def add_note(self, note):
        self.data[len(self.data) + 1] = note

    # Delete a note by ID
    def delete_note(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError(f"Note {note_id} not found.")

    # Search for notes by tag
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

# Function to handle tab completion for notes
#def note_completer(text, state):
#	options = [str(note) for note in notebook.data.values() if str(note).startswith(text)]
#	if state < len(options):
#		return options[state]
#	else:
#		return None

# Add a new note to the notebook                        Am I right?
@input_error
def add_note(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me note text please.")
    text = " ".join(args)
    note = Note(text)
    notebook.add_note(note)
    return "Note added."


# Delete a note by ID
@input_error
def delete_note(args, notebook):
    if len(args) < 1:
        raise ValueError("Give me note ID please.")
    note_id = int(args[0])
    notebook.delete_note(note_id)
    return f"Note {note_id} deleted."


# Add a tag to a note
@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        raise ValueError("Give me note ID and tag please.")
    note_id, tag = int(args[0]), args[1]
    if note_id not in notebook.data:
        raise KeyError(f"Note {note_id} not found.")
    notebook.data[note_id].add_tag(tag)
    return "Tag added."


# Delete a tag from a note
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


# Add the notes to a file
def save_notes(notebook, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


# Loads the notes from a file
def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()



# Main function to interact with the user
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
            upcoming_birthdays = book.get_upcoming_birthdays()
            if upcoming_birthdays:
                table = PrettyTable()
                table.field_names = ["Name", "Birthday"]
                for name, birthday in upcoming_birthdays:
                    table.add_row([name, birthday])
                print("Upcoming birthdays in the next 7 days:")
                print(table)
            else:
                print("No upcoming birthdays in the next 7 days.")
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