import pickle
from datetime import datetime
from collections import UserDict
from prettytable import PrettyTable

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Tag(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Tag must be a non-empty string")
        super().__init__(value)

    def __str__(self):
        return str(self.value)

class Note:
    def __init__(self, text):
        self.text = text
        self.tags = []
        self.creation_date = datetime.now()

    def __str__(self):
        return f"Note: {self.text}\n{self.tags}"

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

    def to_table(self):
        table = PrettyTable()
        table.field_names = ["ID", "Note", "Tags", "Creation Date"]
        for note_id, note in self.data.items():
            table.add_row([note_id, note.to_dict()["Note"], note.to_dict()["Tags"], note.to_dict()["Creation Date"]])
        return table

def save_notes(notebook, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)

def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()
