import csv
import re


def get_raw_contacts(file_name):
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    # pprint(contacts_list)
    return contacts_list


def fix_names(contacts):
    for contact in contacts[1:]:
        full_name_string = ' '.join(contact[:3])
        full_name_list = full_name_string.split()
        while len(full_name_list) < 3:
            full_name_list.append('')
        for i in range(3):
            contact[i] = full_name_list[i]
    return contacts


def fix_phones(contacts):
    main_pattern = re.compile(r'(\+?\d).*(\d{3}).*(\d{3}).?(\d{2}).?(\d{2})')
    main_sub = r'+7(\2)\3-\4-\5'
    exp_pattern = re.compile(r'\(?доб. (\d*)\)?')
    exp_sub = r'доб.\1'
    for contact in contacts[1:]:
        phone = contact[5]
        if phone != '':
            phone = main_pattern.sub(main_sub, phone)
            contact[5] = exp_pattern.sub(exp_sub, phone)


def find_duplicates(contacts):
    names = [' '.join(contact[:2]) for contact in contacts[1:]]
    duplicates = []
    if len(names) != len(set(names)):
        for elem in set(names):
            names.remove(elem)
        duplicates = set(names)
    return duplicates


def fix_duplicates(contacts):
    duplicate_list = find_duplicates(contacts)
    for person in duplicate_list:

        contact_dups = []
        for contact in contacts[1:]:
            if ' '.join(contact[:2]) == person:
                contact_dups.append(contact)
                contacts.remove(contact)

        full_contact = contact_dups[0]
        for duplicate in contact_dups[1:]:
            for i in range(len(duplicate)):
                if contact_dups[0][i] != duplicate[i]:
                    full_contact[i] += duplicate[i]
        contacts.append(full_contact)


def handle_contacts(contacts):
    fix_names(contacts)
    fix_phones(contacts)
    fix_duplicates(contacts)
    return contacts


def save_contacts(contacts, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',', lineterminator='\r')
        datawriter.writerows(contacts)


def handle_phonebook(input_name, output_name):
    raw_contacts = get_raw_contacts(input_name)
    contacts = handle_contacts(raw_contacts)
    save_contacts(contacts, output_name)


if __name__ == '__main__':
    handle_phonebook('phonebook_raw.csv', 'phonebook.csv')
