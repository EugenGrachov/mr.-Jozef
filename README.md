
# mr.-Jozef

Project created as part of training from [GOIT](https://goit.global) — **Oldies Project Team**

---

## 📌 Table of Contents

- [🤖 About mr.Jozef](#-mrjozef--your-personal-assistant-in-the-terminal)
- [🚀 Implemented Features](#-implemented-features)
- [🛠️ Installation and Launch](#️-installation-and-launch)
- [🧑‍💻 User Guide](#-user-guide)
- [🧾 Commands](#-commands)
- [🔄 Autocompletion](#-autocompletion)
- [✅ Testing](#-testing)
- [📂 Project Structure](#-project-structure)
- [👥 Authors](#-authors)
- [💡 License](#-license)

---

# 🤖 mr.Jozef — your personal assistant in the terminal

Hi, I am **mr.Jozef** — a smart CLI bot that will help you manage contacts and notes right from the terminal!  
This project is designed as a part of the GOIT training course to practice building Python-based command-line applications with data persistence and intelligent interaction.

---

## 🚀 Implemented Features

📇 **Contacts**
- Adding contacts: name, address, phone number, email, birthday
- Searching contacts by various criteria (e.g., by name)
- Editing and deleting contacts
- Validating phone numbers and email addresses during adding or editing
- Displaying a list of contacts who have a birthday in a specified number of days

📝 **Notes**
- Adding text notes
- Editing and deleting notes
- Searching notes by content
- Adding tags to notes
- Searching and sorting notes by tags

💾 **Data Storage**
- All data is stored on the user's hard drive
- The assistant can be restarted without data loss

🧠 **Intelligent Features**
- Recognizing user input and guessing the intended command
- Suggesting the closest command when input is unclear

---

## 🛠️ Installation and launch

1. Clone the repository:
   ```bash
   git clone https://github.com/EugenGrachov/mr.-Jozef.git
   cd mr.-Jozef
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package:
   ```bash
   pip install .
   ```

4. After installation, you can run the assistant from anywhere in the terminal:
   ```bash
   mrjozef
   ```

> **Note:** Make sure that Python 3.9+ is installed and all dependencies from `requirements.txt` are satisfied.

---

## 🧑‍💻 User Guide

How to run the program:

1. Clone the repository to your local machine.
2. Make sure you have Python 3.10 or later installed.
3. Open your terminal and navigate to the project folder.
4. Run the program using the following command:
   ```bash
   python jozef.py
   ```
5. The program will start in the Command-Line Interface (CLI). You will see the available commands and functions.

Main commands:

- **Hello**
  ```bash
  hello
  ```

- **Add contact:**
  ```bash
  add contact <name> <address> <phone> <email> <birthday>
  ```

- **Change contact's phone number:**
  ```bash
  change contact <name> <old_phone> <new_phone>
  ```

- **Show contact's phone number:**
  ```bash
  phone <name>
  ```

- **Show all contacts:**
  ```bash
  all
  ```

- **Display contacts with upcoming birthdays within a specified number of days:**
  ```bash
  upcoming_birthdays <number_of_days>
  ```

- **Add a note:**
  ```bash
  add_note <note_text>
  ```

- **Search for notes:**
  ```bash
  search_note <topic or tag>
  ```

How the data is stored:

All contacts and notes are saved in the `storage.pkl` file, which allows data persistence across program sessions.  
You can edit, add, or delete contacts and notes without losing data, even after restarting the program.

---

## 🧾 Commands

- **Add a contact**  
  Add a new contact with name, phone, email, address, and birthday.  
  Example:  
  ```bash
  add John +123456789 john@example.com "123 Main St" 01.01.1990
  ```

- **Search contacts**  
  Search for a contact by name or phone.  
  Example:  
  ```bash
  search John
  ```

- **Add a note**  
  Add a new note with optional tags.  
  Example:  
  ```bash
  add_note "Buy groceries" #shopping
  ```

- **Search notes**  
  Search notes by content or tags.  
  Example:  
  ```bash
  search_note groceries
  ```

- **Exit the assistant**  
  Exit the program.  
  Example:  
  ```bash
  exit
  ```

---

## 🔄 Autocompletion

The assistant supports autocompletion for commands and arguments.

To use this feature:
1. Start typing a command in the terminal.
2. Press the `Tab` key to see suggestions or complete the command automatically.
3. If multiple options are available, press `Tab` twice to see all possible completions.

> **Note:** Autocompletion works only if the terminal supports it and the feature is enabled in your environment.

---

## ✅ Testing

To run unit tests:

```bash
python -m unittest discover
```

> This will automatically discover and run all tests in the project.

---

## 📂 Project Structure

```
mr.-Jozef/
├── mrjozef/
│   ├── __init__.py
│   ├── main.py
│   ├── notes.py
├── setup.py
├── README.md
├── LICENSE
└── requirements.txt
```

🛠️ Technologies used:
- Python 3.9+
- Standard Libraries: `pickle`, `datetime`, `difflib`, `re`
- Object-Oriented Programming: classes `Contact`, `Note`, `Phone`, `Email`, `Birthday`, `Address`
- Data persistence with file storage
- CLI interaction

---

## 👥 Authors

Project created as part of training from [GOIT](https://goit.global)  
**Oldies Project Team**

| Name                | Role         |
|---------------------|--------------|
| Hrachov Yevhenii    | Teamlead     |
| Vorobyov Kirill     | Scrummaster  |
| Chuntu Artem        | Developer    |
| Polovinkin Oleksii  | Developer    |

---

## 💡 License

[MIT License](LICENSE)
