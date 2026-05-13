import datetime, json, uuid

class Base:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.datetime.now().isoformat()

    def save(self, filename=None):
        filename = filename or f"{type(self).__name__.lower()}_{self.id[:8]}.json"
        json.dump(self.__dict__, open(filename, "w"), indent=4)
        print(f"Saved to {filename}")


class Book(Base):
    def __init__(self, title, author, genre, year):
        super().__init__()
        self.title, self.author, self.genre, self.year = title, author, genre, year
        self.is_borrowed, self.borrowed_by = False, None

    def status(self):
        who = f"borrowed by {self.borrowed_by}" if self.borrowed_by else "available"
        return f"'{self.title}' ({self.genre}, {self.year}) is {who}"

    def borrow(self, user):
        if self.borrowed_by:
            print(f"Sorry, '{self.title}' is already borrowed by {self.borrowed_by}")
            return
        self.borrowed_by, self.is_borrowed = user, True
        self.updated_at = datetime.datetime.now().isoformat()
        print(f"{user} borrowed '{self.title}' ({self.genre}, {self.year}) by {self.author}")

    def return_book(self):
        print(f"{self.borrowed_by} returned '{self.title}' ({self.genre}, {self.year})")
        self.borrowed_by, self.is_borrowed = None, False
        self.updated_at = datetime.datetime.now().isoformat()


class User(Base):
    def __init__(self, name, user_id):
        super().__init__()
        self.name, self.user_id = name, user_id


def save_all(books, users):
    json.dump({"books": [b.__dict__ for b in books], "users": [u.__dict__ for u in users]},
              open("records.json", "w"), indent=4)
    print("Saved to records.json")


# usage
book1 = Book("Harry Potter", "J.K Rowling", "Fantasy", 1997)
user1, user2 = User("Eddy", "001"), User("Bruce", "002")

book1.borrow("Eddy")
book1.borrow("Bruce")
print(book1.status())
book1.return_book()
print(book1.status())

# save with custom filenames
book1.save("book1.json")
user1.save("user1.json")
save_all([book1], [user1, user2])