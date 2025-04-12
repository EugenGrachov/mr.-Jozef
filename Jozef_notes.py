import re

# Класс для работы с контактами
class Record:
    def __init__(self, name, email=None, phone=None, birthday=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.birthday = birthday

    def __str__(self):
        return f"{self.name}, Email: {self.email}, Phone: {self.phone}, Birthday: {self.birthday}"

class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, email=None, phone=None, birthday=None):
        if not self.validate_email(email):
            print("Неверный формат email")
            return
        if not self.validate_phone(phone):
            print("Неверный формат телефона")
            return
        contact = Record(name, email, phone, birthday)
        self.contacts.append(contact)
        print(f"Контакт {name} добавлен")

    def edit_contact(self, name, email=None, phone=None, birthday=None):
        contact = self.find_contact(name)
        if contact:
            if email and not self.validate_email(email):
                print("Неверный формат email")
                return
            if phone and not self.validate_phone(phone):
                print("Неверный формат телефона")
                return
            contact.email = email if email else contact.email
            contact.phone = phone if phone else contact.phone
            contact.birthday = birthday if birthday else contact.birthday
            print(f"Контакт {name} обновлён")
        else:
            print("Контакт не найден")

    def delete_contact(self, name):
        contact = self.find_contact(name)
        if contact:
            self.contacts.remove(contact)
            print(f"Контакт {name} удалён")
        else:
            print("Контакт не найден")

    def search_contacts(self, query):
        found_contacts = [contact for contact in self.contacts if query.lower() in contact.name.lower() or (contact.email and query.lower() in contact.email.lower())]
        if found_contacts:
            for contact in found_contacts:
                print(contact)
        else:
            print("Контакты не найдены")

    def display_contacts(self):
        if self.contacts:
            for contact in self.contacts:
                print(contact)
        else:
            print("Нет сохранённых контактов")

    def validate_email(self, email):
        if email:
            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            return bool(re.match(pattern, email))
        return True

    def validate_phone(self, phone):
        if phone:
            pattern = r'^\+?[0-9]{1,3}?[-. ]?\(?\d{1,4}?\)?[-. ]?\d{1,4}[-. ]?\d{1,4}[-. ]?\d{1,9}$'
            return bool(re.match(pattern, phone))
        return True

    def find_contact(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

# Класс для работы с заметками
class Note:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return f"Заметка: {self.title}\n{self.text}"

class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, title, text):
        note = Note(title, text)
        self.notes.append(note)
        print(f"Заметка '{title}' добавлена")

    def edit_note(self, title, new_title=None, new_text=None):
        note = self.find_note_by_title(title)
        if note:
            note.title = new_title if new_title else note.title
            note.text = new_text if new_text else note.text
            print(f"Заметка '{title}' обновлена")
        else:
            print("Заметка не найдена")

    def delete_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            print(f"Заметка '{title}' удалена")
        else:
            print("Заметка не найдена")

    def search_notes(self, query):
        found_notes = [note for note in self.notes if query.lower() in note.title.lower() or query.lower() in note.text.lower()]
        if found_notes:
            for note in found_notes:
                print(note)
        else:
            print("Заметки не найдены")

    def display_notes(self):
        if self.notes:
            for note in self.notes:
                print(note)
        else:
            print("Нет сохранённых заметок")

    def find_note_by_title(self, title):
        for note in self.notes:
            if note.title == title:
                return note
        return None

# Пример использования
contact_book = ContactBook()
note_book = NoteBook()

# Добавление контактов
contact_book.add_contact("Иван Иванов", email="ivan@mail.com", phone="+123-456-7890", birthday="01.01.1990")
contact_book.add_contact("Мария Смирнова", email="maria@mail.com", phone="+321-654-0987", birthday="15.05.1985")

# Печать всех контактов
print("Все контакты:")
contact_book.display_contacts()

# Добавление заметок
note_book.add_note("Заметка 1", "Текст заметки 1")
note_book.add_note("Заметка 2", "Текст заметки 2")

# Печать всех заметок
print("\nВсе заметки:")
note_book.display_notes()

# Поиск заметки по названию или тексту
print("\nПоиск по запросу 'Текст':")
note_book.search_notes("Текст")

# Редактирование заметки
print("\nРедактирование заметки 'Заметка 1':")
note_book.edit_note("Заметка 1", new_text="Обновлённый текст заметки 1")

# Печать всех заметок после редактирования
print("\nВсе заметки после редактирования:")
note_book.display_notes()

# Удаление заметки
print("\nУдаление заметки 'Заметка 1':")
note_book.delete_note("Заметка 1")

# Печать всех заметок после удаления
print("\nВсе заметки после удаления:")
note_book.display_notes()
