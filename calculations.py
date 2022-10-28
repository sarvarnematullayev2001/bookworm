import babel.numbers


def calculate_a4(book):
    if book['color'] == 'rangli':
        price = ((int(book['pages']) * 250) + 10000) * int(book['number_of_books'])
    else:
        price = ((int(book['pages']) * 125) + 10000) * int(book['number_of_books'])
    return babel.numbers.format_currency(price, '', locale='uz')


def calculate_a5(book):
    if book['color'] == 'rangli':
        if book['cover'] == 'yumshoq':
            price = ((int(book['pages']) * 150) + 7000) * int(book['number_of_books'])
        else:
            price = ((int(book['pages']) * 150) + 15000) * int(book['number_of_books'])
    else:
        if book['cover'] == 'yumshoq':
            price = ((int(book['pages']) * 75) + 7000) * int(book['number_of_books'])
        else:
            price = ((int(book['pages']) * 75) + 15000) * int(book['number_of_books'])
    return babel.numbers.format_currency(price, '', locale='uz')
