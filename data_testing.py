import requests
import logging
from random import choice
from book_testing_data import users  
from faker import Faker

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

fake = Faker()

class AutomateRequest:
    AUTH_URL: str = "http://127.0.0.1:8000/api/v1/auth"
    BOOK_URL: str = "http://127.0.0.1:8000/api/v1/books"
    user_details: list[dict] = []
    token_list: list[str] = []

    @classmethod
    def registerUser(cls):
        logging.info("Registering Users...")
        for user in users:
            try:
                response = requests.post(f"{cls.AUTH_URL}/register", json=user)
                response.raise_for_status()  
                
                if response.status_code == 201:
                    data = {"email": user["email"], "password": user["password"], "username": user["username"]}
                    cls.user_details.append(data)
                    logging.info(f"{user['username']} registered successfully")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to register {user['username']}: {e}")

        logging.info("Done Registering Users...")

    @classmethod
    def loginUser(cls):
        logging.info("Logging in Users...")
        for user in cls.user_details:
            login = {"email": user["email"], "password": user["password"]}
            try:
                response = requests.post(f"{cls.AUTH_URL}/login", json=login)
                response.raise_for_status()
                
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    if token:
                        cls.token_list.append(token)
                        logging.info(f"{user['email']} logged in successfully")
                    else:
                        logging.warning(f"Token missing for {user['email']}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Login failed for {user['email']}: {e}")

        logging.info("Done Logging in Users...")

    
    @staticmethod
    def createBook():
        common_languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Russian", "Italian"]
        content = {
            "title": fake.catch_phrase().title(),
            "author": fake.name(),
            "publisher": fake.company(),
            "published_date": fake.date_between(start_date="-50y", end_date="today").isoformat(),
            "page_count": fake.random_int(min=300, max=2000),
            "language": choice(common_languages)
        }
        return content
    
    @classmethod
    def CreateUsersBooks(cls):
        logging.info("Creating users' books...")
        for token, user in zip(cls.token_list, cls.user_details):
            headers = {"Authorization": f"Bearer {token}"}
            for i in range(5):
                content = cls.createBook()

                try:
                    response = requests.post(cls.BOOK_URL, json=content, headers=headers)
                    response.raise_for_status()
                    
                    if response.status_code == 201:
                        logging.info(response.json())  
                    else:
                        logging.warning(f"Failed to create book for {user['username']}: {response.text}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Book creation failed for {user['username']}: {e}")

AutomateRequest.registerUser()
AutomateRequest.loginUser()
AutomateRequest.CreateUsersBooks()

