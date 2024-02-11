import csv

from os import path
from typing import List

from inclusions import CHOICES


class PhoneBook:
    def __init__(self, filename: str) -> None:
        """
        Инициализация справочника.
        Если файл с данными существует, загружаем данные из него.
        Если файл не существует, мы его создаём
        """
        self._filename = filename
        if not self._file_exists():
            self._create_file()

    @staticmethod
    def _validate_data(key: int, value: str) -> bool:
        """Валидация входных данных."""

        if key in (1, 2, 3):
            if value.isalpha():
                return True
            return False
        elif key == 4:
            words = value.split()
            for word in words:
                if not word.isalpha():
                    return False
            return True
        elif key in (5, 6):
            if (value.isdigit() and len(value) >= 11) or (
                    value.startswith('+') and value[1:].isdigit() and len(value) >= 12):
                return True
            return False
        else:
            return True

    def _file_exists(self) -> bool:
        """
        Проверяет существование файла
        """
        return path.isfile(self._filename)

    def _create_file(self) -> None:
        """
        Создаёт новый файл
        """
        with open(self._filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Фамилия", "Имя", "Отчество", "Организация", "Телефон рабочий", "Телефон личный"])

    def _read_file(self) -> List[List[str]]:
        """
        Чтение из файла
        """
        with open(self._filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)

    def _write_file(self, data: List[List[str]]) -> None:
        """
        Запись в файл
        """
        with open(self._filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def print_records(self, page_size: int = 10) -> None:
        """
        Выводит записи из справочника с пагинацией
        """
        records = self._read_file()
        num_records = len(records) - 1
        num_pages = num_records // page_size + 1  # кроме заголовка

        for page in range(num_pages):
            start_index = page * page_size + 1  # кроме заголовка
            end_index = min(start_index + page_size, num_records + 1)
            page_records = records[start_index:end_index]

            for record in page_records:
                print(", ".join(record))

            if end_index < num_records + 1:
                input("Нажмите Enter для продолжения...")

    def add_record(self) -> None:
        """
        Добавляет новую запись в справочник
        """
        try:
            records = self._read_file()
            print("\n==Вы выбрали добавление новой записи==\n")
            values: list = []
            for key, val in CHOICES.items():
                while True:
                    choice: str = input(val)
                    if self._validate_data(key=key, value=choice):
                        values.append(choice)
                        break
                    print("Введите верные данные.")
            records.append(values)
            self._write_file(records)
        except Exception as e:
            print("Произошла ошибка при добавлении записи:", str(e))

    def update_record(self) -> None:
        """
        Обновляет существующую запись в справочнике
        """
        try:
            records = self._read_file()
            print("\n==Вы выбрали обновление записи==\n")

            search_key = input("Введите фамилию контакта для поиска записи: ")

            matching_records = []
            for record in records:
                if record[0] == search_key:
                    matching_records.append(record)

            if len(matching_records) > 1:
                print("Найдено несколько записей:")
                for i, record in enumerate(matching_records):
                    print(f"{i + 1}. {record}")

                choice = int(input("Введите номер записи для обновления: "))
                if choice < 1 or choice > len(matching_records):
                    print("Некорректный номер записи.")
                    return

                record_index = records.index(matching_records[choice - 1])
            elif len(matching_records) == 1:
                record_index = records.index(matching_records[0])
            else:
                print("Запись не найдена.")
                return

            new_values = []
            for key, val in CHOICES.items():
                while True:
                    choice = input(f"Введите новое значение для {val}: ")
                    if self._validate_data(key=key, value=choice):
                        new_values.append(choice)
                        break
                    print("Введите верные данные.")

            records[record_index] = new_values

            self._write_file(records)

            print("Запись успешно обновлена.")

        except Exception as e:
            print("Произошла ошибка при обновлении записи:", str(e))

    def search_records(self):
        """
        Добавляет функционал поиска по характеристикам
        """
        search_keys = input("Введите характеристики для поиска (через запятую): ")
        search_values = input("Введите значения для поиска (через запятую): ")

        search_keys = [key.strip().capitalize() for key in search_keys.split(",")]
        search_values = [value.strip() for value in search_values.split(",")]

        records = self._read_file()
        headers = records[0]
        key_indices = [headers.index(key) for key in search_keys]

        results = []

        for record in records[1:]:
            if all(record[index] == value for index, value in zip(key_indices, search_values)):
                results.append(record)

        if len(results) > 0:
            print("Найденные записи:\n")
            for value in results:
                print(" ".join(value))
        else:
            print("\nНичего не найдено!")


phonebook = PhoneBook('phonebook.csv')
