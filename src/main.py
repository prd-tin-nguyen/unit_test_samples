import requests
from rich.pretty import pprint as rprint
import hashlib
import logging
import re
from typing import Optional, List
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class InvalidEmailError(ValueError):
    """Exception raised for invalid email addresses."""

    def __init__(self, email: str):
        super().__init__(f"{email} is not a valid email address.")
        self.email = email


class EmailService:
    @staticmethod
    def send_verification_email(email: str):
        randon_number: int
        # send request to get a random number from random.org
        url = "https://www.random.org/integers/?num=1&min=1&max=100&col=5&base=10&format=plain&rnd=new"
        res = requests.get(url)
        res.raise_for_status()
        randon_number = int(res.text)

        logging.info(f"{randon_number} --- Verification email sent to " + email)
        return randon_number


class Logger:
    @staticmethod
    def log_info(message: str):
        logging.info(message)

    @staticmethod
    def log_error(message: str):
        logging.error(message)


class UserProfile:
    """Represents a user profile in the system."""

    def __init__(self, username: str, email: str, age: int, password: str, email_service=EmailService, logger=Logger):
        """Initialize a new user profile with username, email, age, and password."""
        self.logger = logger
        self.username: str = username
        self.email: str = self._validate_and_set_email(email)
        self.age: int = age
        self.verified: bool = False
        self.profile_visibility: str = "private"
        self.activity_log: List[str] = []
        self._password_hash: str = self._hash_password(password)
        self.email_service = email_service
        self.logger.log_info(f"User profile created for {username} with email {email}.")

    # @staticmethod
    def _is_valid_email(self, email: str) -> bool:
        """Check if the provided email address is valid."""
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$)"
        return re.match(pattern, email) is not None

    def _validate_and_set_email(self, email: str) -> str:
        """Validate and set the user's email address."""
        if not self._is_valid_email(email):
            self.logger.log_error(f"Invalid email attempt: {email}")
            raise InvalidEmailError(email)

        # set the email if it is valid
        self.logger.log_info(f"Email for user set to {email}.")
        self.email = email
        return email

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, password: str):
        """Set or update the user's password."""
        self._password_hash = self._hash_password(password)
        self.activity_log.append("Password updated.")
        self.logger.log_info("Password for user updated.")

    def validate_password(self, password: str) -> bool:
        """Validate the user's password."""
        return self._hash_password(password) == self._password_hash

    def send_verification_email(self):
        """Simulate sending a verification email."""
        self.verified = True
        self.activity_log.append("Verification email sent.")
        self.email_service.send_verification_email(self.email)

    def update_user(
        self,
        age: Optional[int] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
        visibility: Optional[str] = None,
    ):
        """Update user profile details with optional parameters."""
        if email:
            self.email = self._validate_and_set_email(email)
        if visibility in ["public", "private"]:
            self.profile_visibility = visibility
        self.username = username or self.username
        self.age = age if age is not None else self.age
        self.activity_log.append("User profile updated.")
        self.logger.log_info(f"User profile for {self.username} updated with new details.")

    def enable_2fa(self):
        """Simulate enabling two-factor authentication."""
        self.activity_log.append("2FA enabled.")
        self.logger.log_info("Two-factor authentication enabled.")

    def delete_user(self):
        """Safely delete user profile attributes."""
        self.logger.log_info(f"Deleting user profile for {self.username}.")
        self.username = self.email = self.age = self._password_hash = self.name = None
        self.activity_log.append("User profile deleted.")


def load_hf_model():
    """Load a pre-trained Hugging Face model."""
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

    print(model)
    print("=" * 20)
    pipe = pipeline(model=model, tokenizer=tokenizer)
    print(pipe)
    print("=" * 20)
    return pipe


if __name__ == "__main__":
    user = UserProfile(
        age=25,
        logger=Logger,
        username="asd",
        password="1234",
        email="asd@gmail.com",
        email_service=EmailService,
    )
    user.set_password("12345")

    # run all the methods
    user.send_verification_email()
    # user.update_user(username="qwe", visibility="public", age=30)
    # user.enable_2fa()
    # user.delete_user()

    # logging user detail
    rprint(user.__dict__, expand_all=True)

    load_hf_model()
