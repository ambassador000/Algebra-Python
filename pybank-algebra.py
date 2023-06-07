import os
import datetime

companies = {}
transactions = {}
ordinal_number = 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def line_of_stars_print():
    terminal_width = os.get_terminal_size().columns
    print('*' * terminal_width)

def header_text_centered_print(text):
    terminal_size = os.get_terminal_size().columns
    print(text.center(terminal_size))

def line_of_underscores_print():
    terminal_width = os.get_terminal_size().columns
    print('_' * terminal_width)


def create_account():
    global ordinal_number
    line_of_stars_print()
    header_text_centered_print("PyBANK ALGEBRA")
    print("\n" * 2)
    header_text_centered_print("KREIRANJE RACUNA")
    print("")
    header_text_centered_print("Podaci o vlasniku računa")

    while True:
        company_name = input('Naziv Tvrtke:\t\t\t\t')
        if any(company[0] == company_name for company in companies.values()):
            print("Tvrtka s unesenim nazivom već postoji. Molimo unesite neki drugi naziv tvrtke.")
        else:
            break

    street_and_number = input('Ulica i broj sjedista Tvrtke:\t\t')
    postal_code = input('Postanski broj sjedista Tvrtke:\t\t')
    city = input('Grad u kojem je sjediste Tvrtke:\t')

    while True:
        oib = input('OIB Tvrtke:\t\t\t\t')
        while not (len(oib) == 11 and oib.isdigit()):
            print("Pogrešan unos. Molimo unesite točno 11 brojeva.")
            oib = input("OIB Tvrtke:\t\t\t\t")

        if any(company[4] == oib for company in companies.values()):
            print("Tvrtka s ovim OIB-om već ima račun.")
        else:
            break
        
    responsible_person = input('Ime i prezime odgovorne osobe Tvrtke:\t')

    account_currency = input('\nUpišite naziv valute računa (EUR ili HRK):\t').lower()
    while account_currency not in ['eur', 'euro', 'hrk', 'kuna', 'kn']:
        print(f'Niste unijeli "EUR" ili "HRK". Molimo pokušajte ponovno.')
        account_currency = input('Upišite naziv valute računa (EUR ili HRK):\t').lower()
    if account_currency in ['eur', 'euro']:
        account_currency = 'EUR'
    elif account_currency in ['hrk', 'kuna', 'kn']:
        account_currency = 'HRK'

    initial_balance = 0
    input("\nSPREMI? (Pritisnite bilo koju tipku) ")
    account_number = generate_account_number()

    for company in companies.values():
        if company[8] == account_number:
            print("Račun s ovim brojem već postoji.")
            return

    companies[ordinal_number] = [company_name, street_and_number, postal_code, city, oib, responsible_person, account_currency, initial_balance, account_number]
    ordinal_number += 1

    print(f'\nRačun tvrtke s imenom {company_name} je kreiran i broj računa glasi {account_number}\n')

    input("\nZa Povratak u Glavni izbornik pritisnite bilo koju tipku ")


def generate_account_number():
    date_now = datetime.datetime.now()
    serial_number = len(companies) + 1
    return "BA-{}-{}-{:05}".format(date_now.year, date_now.month, serial_number)


def display_account_balance():
    clear_screen()
    line_of_stars_print()
    header_text_centered_print("PyBANK ALGEBRA")
    print("\n" * 2)
    header_text_centered_print("PRIKAZ STANJA RAČUNA")
    print("")
    account_number = input("Unesite broj računa: ")
    for company in companies.values():
        if company[8] == account_number:
            print(f"\nBroj računa: {company[8]}")
            print(f"\nTrenutno stanje računa: {company[7]} {company[6]}\n")

    input("\nZa Povratak u Glavni izbornik pritisnite bilo koju tipku ")


def view_transactions():
    clear_screen()
    line_of_stars_print()
    header_text_centered_print("PyBANK ALGEBRA")
    print("\n" * 2)
    header_text_centered_print("PRIKAZ PROMETA PO RAČUNU")
    print("")
    account_number = input("Unesite broj računa za koji želite pogledati promet: \n")
    if account_number in transactions:
        for transaction in transactions[account_number]:
            print(f"{transaction[0]}: {transaction[1]}")
    else:
        print("Nisu pronađene transakcije za ovaj broj računa.")

    input("\nZa Povratak u Glavni izbornik pritisnite bilo koju tipku ")


def deposit_money():
    clear_screen()
    line_of_stars_print()
    header_text_centered_print("PyBANK ALGEBRA")
    print("\n" * 2)
    header_text_centered_print("PRIKAZ STANJA RAČUNA")
    print("")
    
    while True:
        account_number = input("Unesite broj računa na koji želite položiti novac: ")
        if any(company[8] == account_number for company in companies.values()):
            break
        else:
            print("Broj računa ne postoji. Pokušajte ponovno.")

    amount = float(input("Molimo Vas upisite iznos koji zelite poloziti na racun.\nNAPOMENA Molimo Vas koristite decimalnu tocku, a ne zarez.\n\n\t"))
    for company in companies.values():
        if company[8] == account_number:
            company[7] += amount
            if account_number in transactions:
                transactions[account_number].append(('Polog', amount))
            else:
                transactions[account_number] = [('Polog', amount)]
            print(f"\nPolog je bio uspješan. Novo stanje računa iznosi {company[7]} {company[6]}.")

    input("\nZa Povratak u Glavni izbornik pritisnite bilo koju tipku ")


def withdraw_money():
    account_number = input("\nUnesite broj računa s kojeg želite podići novac: ")
    amount = float(input("Unesite iznos koji želite isplatiti s računa: "))
    for company in companies.values():
        if company[8] == account_number:
            if amount > company[7]:
                print("Nemate dovoljno sredstava na računu.")
                return
            company[7] -= amount
            if account_number in transactions:
                transactions[account_number].append(('Isplata', amount))
            else:
                transactions[account_number] = [('Isplata', amount)]
            print(f"\nIsplata je bila uspješna. Novo stanje računa iznosi {company[7]} {company[6]}.\n")

    input("\nZa Povratak u Glavni izbornik pritisnite bilo koju tipku ")


def main_menu():
    while True:
        clear_screen()
        line_of_stars_print()
        header_text_centered_print("PyBANK ALGEBRA")
        print("\n" * 2)
        header_text_centered_print("GLAVNI IZBORNIK")
        print("")
        print(f'1. Kreiranje računa')
        print(f'2. Prikaz stanja računa')
        print(f'3. Prikaz prometa po računu')
        print(f'4. Polog novca na račun')
        print(f'5. Podizanje novca s racuna')
        print(f'0. Izlaz')
        line_of_underscores_print()
        if len(companies) == 0:
            print(f'Još niste otvorili račun. Molimo prvo kreirajte račun. Hvala!')
            line_of_underscores_print()
        choice = input("Vaš izbor:\t")
        if choice == '1':
            create_account()
        elif choice == '2':
            display_account_balance()
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            deposit_money()
        elif choice == '5':
            withdraw_money()
        elif choice == '0':
            break

main_menu()