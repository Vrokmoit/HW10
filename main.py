from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value=None):
        if value is not None:
            if self.validate_phone(value):
                self.value = value
            else:
                raise ValueError("Phone number must be 10 digits")
        else:
            self.value = None
    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if phone is not None:
            if Phone.validate_phone(phone):
                self.phones.append(Phone(phone))
            else:
                raise ValueError("Phone number must be 10 digits")
            
    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                return

    def edit_phone(self, name, new_phone):
        found_contact = None
        for contact in self.phones:
            if contact.value == name:
                found_contact = contact
                break

        if found_contact is None:
            raise ValueError(f"Contact '{name}' not found")

        if new_phone is not None and not Phone.validate_phone(new_phone):
            raise ValueError("Phone number must be 10 digits")

        found_contact.value = new_phone

        if found_contact is None:
            raise ValueError(f"Contact '{name}' not found")


    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None



    def __str__(self):
        phones_str = ", ".join([phone.value for phone in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        if name in self.data:
            return self.data[name]

# Декоратор для обработки ошибок
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError as e:
            return str(e)
        except IndexError as e:
            if "unpack" in str(e):
                return "Give me name and phone please"
            else:
                return "Invalid input"
        except Exception as e:
            return str(e)
    return wrapper


@input_error
def add_contact(name, phone):
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added successfully"

@input_error
def change_phone(name, phone):
    if name in address_book.data:
        if not phone:
            raise ValueError("Phone is missing")
        record = address_book[name]
        record.edit_phone(record.phones[0].value, phone)
        return "Phone number updated"
    else:
        raise ValueError(f"Contact '{name}' not found")

@input_error
def find_phone(name):
    if name in address_book.data:
        record = address_book[name]
        phones = record.find_phone(name)
        if phones:
            return phones
        else:
            return f"No phones found for contact '{name}'"
    else:
        raise ValueError(f"Contact '{name}' not found")

# Вывод всех контактов
def show_all_contacts():
    data = address_book.data
    if not data:
        return "No contacts found"
    else:
        result = "\n".join([str(record) for record in data.values()])
        return result

# Главная функция для обработки команд пользователя
def main():
    print("How can I help you?")
    
    while True:
        command = input("Enter a command: ").lower()
        
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add "):
            _, name, phone, *rest = command.split()
            if not name or not phone:
                print("Enter a name and phone")
                continue
            response = add_contact(name, phone)
            print(response)
        elif command.startswith("change "):
            _, name, *phone = command.split()
            phone = " ".join(phone)
            response = change_phone(name, phone)
            print(response)
        elif command.startswith("phone "):
            _, name = command.split()
            try:
                response = find_phone(name)
                print(response)
            except Exception as e:
                print(e)
        elif command.startswith("delete "):
            _, name = command.split()
            try:
                address_book.delete(name)
                print(f"Contact '{name}' deleted successfully")
            except KeyError:
                print(f"Contact '{name}' not found")
        elif command == "show all":
            result = show_all_contacts()
            print(result)
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again")

if __name__ == "__main__":
    address_book = AddressBook()  # Создание новой адресной книги
    main()
