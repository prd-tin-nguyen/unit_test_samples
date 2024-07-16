# Test data for TestUserProfile
from unittest.mock import AsyncMock, MagicMock
import pytest
import hashlib

# Data for test__is_valid_email
is_valid_email_data = [
    pytest.param({"email": "valid@example.com", "expected": True}, id="valid_email"),
    pytest.param({"email": "invalidemail", "expected": False}, id="invalid_email"),
    pytest.param({"email": "user@domain.co", "expected": True}, id="valid_user_domain_co"),
    pytest.param({"email": "@nouser.com", "expected": False}, id="no_user"),
    pytest.param({"email": "user.name@domain.com", "expected": True}, id="valid_user_name_domain"),
    pytest.param({"email": "user@domain", "expected": False}, id="user_domain_no_tld"),
]
# Data for test__validate_and_set_email


validate_and_set_email_data = [
    pytest.param({"email": "valid@example.com", "raises": False}, id="valid_email"),
    pytest.param({"email": "invalidemail", "raises": True}, id="invalid_email_no_domain"),
    pytest.param({"email": "user@domain.com", "raises": False}, id="valid_email_with_domain"),
    pytest.param({"email": "noatsign", "raises": True}, id="invalid_email_no_at_sign"),
    pytest.param({"email": "user@nodotcom", "raises": True}, id="invalid_email_no_tld"),
    pytest.param({"email": "user@domain", "raises": True}, id="invalid_email_domain_no_tld"),
    pytest.param({"email": "user.name@domain.com", "raises": False}, id="valid_email_with_dot"),
]

# Data for test__hash_password
hash_password_data = [
    pytest.param("password", hashlib.sha256("password".encode()).hexdigest(), id="simple_password"),
    pytest.param("123456", hashlib.sha256("123456".encode()).hexdigest(), id="numeric_password"),
    pytest.param("password123", hashlib.sha256("password123".encode()).hexdigest(), id="alphanumeric_password"),
]

# Data for test_validate_password
validate_password_data = [
    pytest.param("securepassword", True, id="valid_secure_password"),
    pytest.param("wrongpassword", False, id="invalid_wrong_password"),
    pytest.param("123456", False, id="invalid_numeric_password"),
    pytest.param("securepassword", True, id="duplicate_valid_secure_password"),
]

# Data for test_update_user
update_user_data = [
    pytest.param(None, "new@example.com", None, "public", id="email_only_public"),
    pytest.param("newuser", None, 30, "private", id="username_age_private"),
    pytest.param("user2", "user2@example.com", 22, "public", id="complete_user_public"),
    pytest.param(None, None, None, "private", id="private_no_info"),
]

# Data for test_send_verification_email
send_verification_email_data = [
    pytest.param(
        {"email": "random@gmail.com", "random_numbers": [MagicMock(status=200, text="1")], "expected": 1},
        id="random_gmail",
    ),
    pytest.param(
        {"email": "new@example.com", "random_numbers": [MagicMock(status=200, text="2")], "expected": 2},
        id="new_example",
    ),
    pytest.param(
        {"email": "user2@gmail.com", "random_numbers": [MagicMock(status=200, text="3")], "expected": 3},
        id="user2_gmail",
    ),
    pytest.param(
        {"email": "user3@outlook.com", "random_numbers": [MagicMock(status=200, text="4")], "expected": 4},
        id="user3_outlook",
    ),
]
