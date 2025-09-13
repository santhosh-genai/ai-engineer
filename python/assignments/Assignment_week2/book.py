from datetime import datetime

class book:
    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year
    def get_age(self):
        current_year = datetime.now().year
        return current_year - self.publication_year

book1 = book("Python Programming", "John Doe", 2020)
print("Book age:", book1.get_age())