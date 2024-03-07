import django_tables2 as tables


data = [
    {
        'number_lesson': '1',
        'time': '12:00 - 12:45',
        'name': 'Говнопара',
        'teacher': 'Говноед',
        'address': 'Ленина',
    },
]


class MyTable(tables.Table):
    number_lesson = tables.Column()
    time = tables.Column()
    name = tables.Column()
    teacher = tables.Column()
    address = tables.Column()


schedule = MyTable(data)
print(schedule)
