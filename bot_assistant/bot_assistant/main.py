import sys
from bot_assistant.contacts import AddressBook, Record, Name, Phone, Birthday, Email
from bot_assistant.notebook import Note, NoteBook
from bot_assistant.file_sorter import FileSorter
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class SingleUseCompleter(Completer):
    def __init__(self, words):
        self.words = words
        self.used = False  # Флаг, указывающий на то, использовались ли подсказки

    def get_completions(self, document: Document, complete_event):
        # Проверяем, были ли уже использованы подсказки
        if not self.used:
            text = document.text_before_cursor
            for word in self.words:
                if word.startswith(text):
                    yield Completion(word, start_position=-len(text))
            self.used = True  # Помечаем подсказки как использованные

    def reset(self):
        # Сброс флага для следующего ввода
        self.used = False


# Список команд для автодополнения
COMMANDS = [
    "help",
    "exit",
    "add_contact",
    "change_contact_phone",
    "show_all_contacts",
    "search_by_bd",
    "add_birthday",
    "add_email",
    "add_phone",
    "add_note",
    "search_note",
    "edit_note",
    "remove_note",
    "show_note",
    "help_note",
    "delete_contact",
    "search_contacts",
    "sort_files",
]
command_completer = SingleUseCompleter(COMMANDS)

# Создание сессии с автодополнением
session = PromptSession(completer=command_completer)


class ContactBot:
    def __init__(self, address_book, note_book):
        self.address_book = address_book
        self.note_book = note_book
        self.sorter = FileSorter() # обьєкт сорьувальник

    @staticmethod
    def hello():
        return "How can I help you?"

    # додавання контакту
    def add_contact(self, data):
        try:
            name, phone = data.rsplit(maxsplit=1)
            record = Record(name)
            record.add_phone(Phone(phone))
            self.address_book.add_record(record)
            return f"Contact {name} added with phone {phone}"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    # зміна номера телефону контакту
    def change_contact_phone(self, data):
        try:
            name, phone = data.rsplit(maxsplit=1)
            record = self.address_book.find(name)
            if record:
                record.phones.clear()
                record.add_phone(Phone(phone))
                return f"Phone number updated for {name}"
            else:
                return "Contact not found"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    def add_phone(self, data):
        try:
            name, phone = data.rsplit(maxsplit=1)
            if name and phone:  # Ensure both name and phone are provided
                record = self.address_book.find(name)
                if record:
                    record.add_phone(Phone(phone))
                    self.address_book.save_to_json()  # Save changes to JSON file
                    return f"Phone number {phone} added for {name}"
                else:
                    return f"Contact '{name}' not found"
            else:
                return "Invalid data format. Please provide both name and phone number."
        except ValueError as e:
            return f"Error: {e}"

    # вивід всіх контактів
    def show_all_contacts(self):
        if not self.address_book.data:
            return "No contacts available"
        else:
            result = ""
            for record in self.address_book.data.values():
                contact_info = f"Contact name: {record.name.value}, Phones: {', '.join(record.phones)}"
                if record.birthday.value:
                    contact_info += f", Birthday: {record.birthday}"
                if record.email.value:
                    contact_info += f", Email: {record.email}"
                result += contact_info + "\n"
            return result

    # пошук контактів з днем народження в межах 14 днів
    def search_by_bd(self):
        upcoming_birthday_contacts = []
        today = datetime.today()
        for contact in self.address_book.data.values():
            if contact.birthday.value_as_datetime():
                next_birthday = datetime(
                    today.year,
                    contact.birthday.value_as_datetime().month,
                    contact.birthday.value_as_datetime().day,
                )
                if next_birthday < today:
                    next_birthday = datetime(
                        today.year + 1,
                        contact.birthday.value_as_datetime().month,
                        contact.birthday.value_as_datetime().day,
                    )
                days_to_birthday = (next_birthday - today).days
                if 0 <= days_to_birthday <= 14:
                    upcoming_birthday_contacts.append((contact, days_to_birthday))
        if not upcoming_birthday_contacts:
            return "No contacts with upcoming birthdays."
        else:
            result = ""
            for contact, days_left in upcoming_birthday_contacts:
                result += f"Contact: {contact.name.value.capitalize()}, Days until birthday: {days_left} ({contact.birthday})\n"  # Змінено
            return result

    # додавання дня народження контакту
    def add_birthday(self, data):
        try:
            name, birthday = data.rsplit(maxsplit=1)
            if name in self.address_book:
                self.address_book[name].birthday = Birthday(birthday)
                return f"Birthday added for {name}"
            else:
                return f"Contact with name {name} does not exist."
        except ValueError:
            return "Invalid data format. Please provide both name and birthday."

    # додавання електронної адреси контакту
    def add_email(self, data):
        try:
            name, email = data.rsplit(maxsplit=1)
            if name and email:
                if name in self.address_book:
                    self.address_book[name].email = Email(email)
                    return f"Email added for {name}"
                else:
                    return f"Contact with name {name} does not exist."
            else:
                return "Invalid data format. Please provide both name and email."
        except ValueError:
            return "Invalid data format. Please provide both name and email."

    def add_note(self):
        title = input("Enter the title of the note:  ")
        text = input("Enter the content of the note: ")
        tags = input("Enter tags, separated by commas: ")
        new_note = Note(
            title, text, tags
        )  # Створення нової нотатки з усіма необхідними аргументами
        self.note_book.add_note(new_note)  # Додавання нової нотатки до нотатника
        return "Note added"

    def edit_note(
        self, note_title, new_content
    ):  # Пошук та редагування нотатки за назвою
        for note in self.note_book.data:
            if note.title == note_title:  # Порівнюємо назву нотатки з вказаною
                note.text = new_content  # Оновлюємо текст нотатки на новий зміст
                return "Note updated successfully."
        return "Note not found."

    def show_note(self):
        if not self.note_book.data:
            return "No notes available"
        else:
            return "\n".join(str(note) for note in self.note_book.data)

    # надання користувачу довідки щодо доступних команд для роботи з нотатками

    def help(self):
        commands_help = {
            "hello": "Displays a greeting message and offers assistance.",
            "add_contact": "<name> <phone>: Adds a new contact.",
            "change_contact_phone": "<name> <new phone>: Updates the phone number of a contact.",
            "add_phone": "<name> <phone>: Adds an additional phone number to an existing contact.",
            "show_all_contacts": "Displays all contacts.",
            "search_by_bd": "Searches for contacts whose birthday is within the next 14 days.",
            "add_birthday": "<name> <birthday>: Adds a birthday to a contact.",
            "add_email": "<name> <email>: Adds an email to a contact.",
            "add_note": "Adds a new note.",
            "search_note": "<keyword>: Searches for notes by keyword.",
            "edit_note": "<note title> <new content>: Edits the content of a note.",
            "remove_note": "<note title>: Removes a note.",
            "show_note": "Displays all notes.",
            "help_note": "Displays help message for note commands.",
            "delete_contact": "<name>: Deletes a contact.",
            "search_contacts": "<name or phone>: Searches contacts by name or phone.",
        }
  
        max_command_length = max(len(command) for command in commands_help.keys())
        formatted_help = [f"{command.ljust(max_command_length)} : {description}" for command, description in commands_help.items()]
        # Выводим отформатированный список команд
        for line in formatted_help:
            return "\n".join([f"{cmd}: {desc}" for cmd, desc in commands_help.items()])

    def help_note(self):
        commands = {
            "add_note": "Add a new note. Usage: add_note your note here",
            "search_note": "Search notes by keyword. Usage: search_note keyword",
            "edit_note": "Edit an existing note. Usage: edit_note id new content",
            "remove_note": "Remove a note. Usage: remove_note id",
            "show_note": "Show all notes.",
            "help_note": "Show this help message.",
        }
        return "\n".join([f"{cmd}: {desc}" for cmd, desc in commands.items()])

    # Видалення контакту
    def delete_contact(self, name):
        try: 
            self.address_book.delete(name)
            return f"Contact {name} deletetion fuction finished"
        except ValueError:
            return "Invalid data format. Please provide both name and phone."

    # Пошук контакту
    def search_contacts(self, name):
        found_records = [
            record
            for record in self.address_book.data.values()
            if name.lower() in record.name.value.lower()
            or any(name.lower() in phone.lower() for phone in record.phones)
        ]
        if found_records:
            return "\n".join(str(record) for record in found_records)
        else:
            return f"No contacts found matching '{name}'"

    def main_in_bot(self):
        while True:
            command_completer.reset()
            user_input_original = session.prompt("Enter command:  ")
            user_input = user_input_original.lower()
            if user_input in ["good bye", "close", "exit", "."]:
                self.address_book.save_to_json()
                self.note_book.save_to_json()
                return exit_bot()
            elif user_input.startswith("sort_files"):
                folder_path = user_input_original[len("sort_files") + 1:].strip()
                self.sorter.go(folder_path)
                return "Files sorted successfully."
            elif user_input.startswith("add_birthday"):
                data = user_input_original[len("add_birthday") + 1 :]
                return self.add_birthday(data)
            elif user_input.startswith("add_email"):
                data = user_input_original[len("add_email") + 1 :]
                return self.add_email(data)
            elif user_input == "hello":
                return self.hello()
            elif user_input.startswith("add_contact"):
                data = user_input_original[len("add_contact") + 1 :]
                return self.add_contact(data)
            elif user_input.startswith(
                "add_phone"
            ):  # додає телефон до списку телефонів контакту. Як працюєЖ пишемо add_phone name
                data = user_input_original[len("add_phone") + 1 :]
                return self.add_phone(data)
            
            elif user_input.startswith("add_note"):  # + Додає нотатку до нотатника.
                if len(user_input.split()) > 1:
                    return "Invalid command format. Usage: add_note"
                else:
                    return self.add_note()
                
            elif user_input.startswith(
                "search_note"
            ):  # + Шукає нотатки за певними ключовими словами і сортує від новішого до старішого до даті.
                search_query = user_input[len("search_note"):].strip()  # Отримуємо пошуковий запит, видаляючи команду та пробіли на початку та в кінці
                if len(search_query) < 1:
                    print('Invalid command format.')
                else:
                    found_notes = self.note_book.search_note(search_query)
                    for note in found_notes:
                        return note  # Виводимо інформацію про кожну знайдену нотатку  
            elif user_input.startswith(
                "edit_note"
            ):  # + Редагує існуючу нотатку. edit_note "назва рецепту" "новий зміст рецепту"
                command, *args = (
                    user_input.split()
                )  # Розділяємо введену команду на частини
                if (
                    len(args) >= 2
                ):  # Переконуємося, що користувач ввів ідентифікатор та новий зміст
                    note_id = args[
                        0
                    ]  # Перше слово після команди - ідентифікатор нотатки
                    new_content = " ".join(args[1:])  # Все інше - новий зміст нотатки
                    return self.edit_note(note_id, new_content)
                else:
                    return "Please, provide both an ID and new content for the note."
            elif user_input.startswith("remove_note"):  # + Видаляє нотаток.
                note_title = user_input[
                    11:
                ].strip()  # Витягуємо назву нотатки і видаляємо зайві пробіли
                if self.note_book.remove_note_by_title(note_title):
                    return "Note removed successfully."
                else:
                    return "Note not found."
            elif user_input.startswith("show_note"):  # + Виводить список всіх нотаток.
                if len(user_input.split()) > 1:
                    return "Invalid command format. Usage: show_note"
                else:
                    return self.show_note()
            elif user_input.startswith("help_note"):  # + Виводить список доступних команд для нотатника.
                if len(user_input.split()) > 1:
                    return "Invalid command format. Usage: help_note"
                else:
                    return self.help_note()
            elif user_input.startswith("help"):  # + Виводить список доступних всех команд.
                if len(user_input.split()) > 1:
                    return "Invalid command format. Usage: help"
                else:
                    return self.help()            
            elif user_input.startswith("change_contact_phone"):
                data = user_input_original[len("change_contact_phone") + 1 :]
                return self.change_contact_phone(data)
            elif user_input == "show_all_contacts":
                return self.show_all_contacts()
            elif user_input.startswith("delete_contact"):
                name = user_input_original[len("delete_contact") + 1 :]
                return self.delete_contact(name)
            elif user_input.startswith("search_contacts"):
                name = user_input[len("search_contacts") + 1 :]
                return self.search_contacts(name)
            elif user_input == "search_by_bd":
                return self.search_by_bd()
            else:
                return "Invalid command. Try again."
            
def main():
    print("Hello my name is Otto. How can I help you?")
    address_book = AddressBook("address_book.json")
    note_book = NoteBook("notes.json")
    bot = ContactBot(address_book, note_book)
    while True:
        print(bot.main_in_bot())


def exit_bot() -> None:
    print("Good bye!")
    sys.exit()


if __name__ == "__main__":
    main()
