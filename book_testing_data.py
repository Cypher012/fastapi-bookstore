users = [
  {
    "first_name": "John",
    "last_name": "Doe",
    "username": "jdoe123",
    "email": "john.doe@example.com",
    "password": "secureP@ss1"
  },
  {
    "first_name": "Alice",
    "last_name": "Smith",
    "username": "alice_s",
    "email": "alice.smith@example.com",
    "password": "password123"
  },
  {
    "first_name": "Michael",
    "last_name": "Johnson",
    "username": "mjohnson",
    "email": "michael.johnson@example.com",
    "password": "M!chael2024"
  },
  {
    "first_name": "Emily",
    "last_name": "Davis",
    "username": "emilyd",
    "email": "emily.davis@example.com",
    "password": "Em1lyRules"
  },
  {
    "first_name": "Robert",
    "last_name": "Brown",
    "username": "rob_brown",
    "email": "robert.brown@example.com",
    "password": "Bobby@456"
  },
  {
    "first_name": "Jessica",
    "last_name": "Wilson",
    "username": "jesswil",
    "email": "jessica.wilson@example.com",
    "password": "Jess!ca007"
  },
  {
    "first_name": "David",
    "last_name": "Martinez",
    "username": "d_martinez",
    "email": "david.martinez@example.com",
    "password": "Dmart@Secure"
  },
  {
    "first_name": "Sophia",
    "last_name": "Anderson",
    "username": "sophiand",
    "email": "sophia.anderson@example.com",
    "password": "Sophia@2023"
  },
  {
    "first_name": "William",
    "last_name": "Taylor",
    "username": "will_t",
    "email": "william.taylor@example.com",
    "password": "TaylorStrong!"
  },
  {
    "first_name": "Olivia",
    "last_name": "Thomas",
    "username": "oliviat",
    "email": "olivia.thomas@example.com",
    "password": "OliviaPower1"
  }
]

books = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Scribner",
        "published_date": "1925-04-10",
        "page_count": 180,
        "language": "English"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "published_date": "1949-06-08",
        "page_count": 328,
        "language": "English"
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "published_date": "1960-07-11",
        "page_count": 281,
        "language": "English"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publisher": "T. Egerton",
        "published_date": "1813-01-28",
        "page_count": 279,
        "language": "English"
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "published_date": "1951-07-16",
        "page_count": 214,
        "language": "English"
    },
    {
        "title": "Moby-Dick",
        "author": "Herman Melville",
        "publisher": "Harper & Brothers",
        "published_date": "1851-10-18",
        "page_count": 635,
        "language": "English"
    },
    {
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "publisher": "The Russian Messenger",
        "published_date": "1869-01-01",
        "page_count": 1225,
        "language": "Russian"
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publisher": "George Allen & Unwin",
        "published_date": "1937-09-21",
        "page_count": 310,
        "language": "English"
    },
    {
        "title": "The Divine Comedy",
        "author": "Dante Alighieri",
        "publisher": "Nicolò di Lorenzo",
        "published_date": "1472-01-01",
        "page_count": 798,
        "language": "Italian"
    },
    {
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "publisher": "The Russian Messenger",
        "published_date": "1866-01-01",
        "page_count": 671,
        "language": "Russian"
    }
]

# from random import choice, randint
# from data_testing import AutomateRequest

# user = AutomateRequest().user_details

# def book(num:int, user):
#   for i in range(num):
#     year = randint(1880, 2020)
#     month = randint(1, 12)
#     date = randint(1,28)
#     page_count = randint(300, 2000)
#     languages = ["English", "Spanish", "French", "Russian", "italian"]
#     language = choice(languages)
#     content = {
#         "title": f"{user['username']} title",
#         "author": f"{user['username']} author",
#         "publisher": f"{user['username']} publisher",
#         "published_date": f"{year}-{month}-{date}",
#         "page_count": page_count,
#         "language": language
#     }
#     print(content)
     

# book(5,user)