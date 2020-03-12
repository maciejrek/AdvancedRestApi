from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str()  # can be required=True - won't work without 'title' key. Defalt = false
    author = fields.Str()
    description = fields.Str()


# Serialization
class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description


book_ser = Book("Clean Code", "Bob Martin", "A book about writing cleaner code.")

book_schema = BookSchema()
book_dict = book_schema.dump(book_ser)

print(book_dict)

# Deserialization

incoming_book_data = {
    "title": "Clean Code",
    "author": "Bob Martin",
    "description": "A book about writing cleaner code.",
}

book_de = book_schema.load(incoming_book_data)
book_obj = Book(**book_de)

print(book_de)
print(book_obj)
