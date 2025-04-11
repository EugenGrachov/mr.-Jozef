# mr.-Jozef
Project created as part of training from [GOIT] (https ://goit.global) * * Oldies Project Team * *

# 🤖 mr.Jozef — your personal assistant in the terminal

Hi, I am **mr.Jozef** — a smart CLI bot that will help you manage contacts and notes right from the terminal!

---

## 🚀 Implemented Features
📇 Contacts
 - Adding contacts: name, address, phone number, email, birthday
 - Searching contacts by various criteria (e.g., by name)
 - Editing and deleting contacts
 - Validating phone numbers and email addresses during adding or editing
 - Displaying a list of contacts who have a birthday in a specified number of days

📝 Notes
  -  Adding text notes
  -  Editing and deleting notes
  -  Searching notes by content
 📌 Adding tags to notes
 🔎 Searching and sorting notes by tags

💾 Data Storage
  -  All data is stored on the user's hard drive
  -  The assistant can be restarted without data loss

🧠 Intelligent Features
  -  Recognizing user input and guessing the intended command
  -  Suggesting the closest command when input is unclear

---

## 🧑‍💻 User Guide

### How to run the program:

1. Clone the repository to your local machine.
2. Make sure you have Python 3.10 or later installed.
3. Open your terminal and navigate to the project folder.
4. Run the program using the following command:

```bash
python jozef.py
```

5. The program will start in the Command-Line Interface (CLI). You will see the available commands and functions.

### Main commands:
- **Hello**
  ```
  hello
  ``` 

- **Add contact:**
  ```
  add contact <name> <address> <phone> <email> <birthday>
  ```
- **Change contact's phone number**
  ```
  change contact <name> <old_phone> <new_phone>
  ```
- **Show contact's phone number:**
  ```
  phone <name>
  ```
  - **Show all contacts:**
  ```
  all
  ```
- **Display contacts with upcoming birthdays within a specified number of days:**
  ```
  upcoming_birthdays <number_of_days>
  ```
- **Add a note:**
  ```
  add_note <note_text>
  ```
- **Search for notes:**
  ```
  search_note <topic or tag>
  ```

### How the data is stored:

- All contacts and notes are saved in the `storage.pkl` file, which allows data persistence across program sessions.
- You can edit, add, or delete contacts and notes without losing data, even after restarting the program.

---

---

## 🛠️ Technologies

- Python 3.9+
- Standard Libraries: `pickle`, `datetime`, `difflib`, `re`
- Object-Oriented Programming: classes `Contact`, `Note`, `Phone`, `Email`, `Birthday`, `Address`
- Data persistence with file storage
- CLI interaction

---

## 🛠️ Installation and launch

```bash
git clone https://github.com/EugenGrachov/mr.-Jozef.git
cd mr.-Jozef
python jozef.py
```

## 📂 Project structure

```
├── assistant.py #        Main CLI interface
├── models.py #           Classes Contact, Note, etc.
├── storage.pkl #         Data storage file
├── README.md #           Project documentation
```

---

## 👥 Authors

Project created as part of training from [GOIT] (https ://goit.global)
* * Oldies Project Team * *

| Name                | Role         |
|---------------------|--------------|
| Hrachov Yevhenii    | Teamlead     |
| Vorobyov Kirill     | Scrummaster  |
| Chuntu Artem        | Developer    |
| Polovinkin Oleksii  | Developer    |
---

## 💡 License

[MIT License](LICENSE)
