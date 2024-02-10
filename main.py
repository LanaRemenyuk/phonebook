from app import phonebook


def main():
    while True:
        menu: str = input(
            "\nВыберите один из пунктов меню (введите необходимое число): \n"
            " 1. Прочитать весь справочник;\n"
            " 2. Добавить запись;\n"
            " 3. Редактировать запись;\n"
            " 4. Найти запись.\n\n"
            'Для выхода введите "выйти": '
        )
        if menu == "выйти":
            print("Вы вышли из справочника.")
            break
        elif menu not in ("1", "2", "3", "4"):
            print("\n!!! Некорректный номер, выберите номер из списка.")
        else:
            if menu == "1":
                phonebook.print_records(page_size=10)
            elif menu == "2":
                phonebook.add_record()
            elif menu == "3":
                phonebook.update_record()
            else:
                phonebook.search_records()


if __name__ == "__main__":
    main()