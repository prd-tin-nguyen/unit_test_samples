# FILE: test_main.py

from typing import Dict
from unittest.mock import MagicMock, patch
import pytest
from main import UserProfile, InvalidEmailError, EmailService, Logger, load_hf_model

from data import (
    is_valid_email_data,
    validate_and_set_email_data,
    hash_password_data,
    validate_password_data,
    update_user_data,
    send_verification_email_data,
)


# Fixtures for common setup
@pytest.fixture
def user_profile_fixture():
    """Fixture to create a default UserProfile for testing."""
    return UserProfile(
        username="testuser",
        email="test@example.com",
        age=25,
        password="securepassword",
        logger=Logger,
        email_service=EmailService,
    )


@pytest.fixture
def logger_mock(mocker):
    """Fixture to mock Logger."""
    return mocker.patch.object(Logger, "log_info")


# Test class for UserProfile
class TestUserProfile:
    @pytest.mark.parametrize("sample", is_valid_email_data)
    def test__is_valid_email(self, user_profile_fixture, sample: Dict):
        email, expected = sample["email"], sample["expected"]
        assert user_profile_fixture._is_valid_email(email) == expected

    @pytest.mark.parametrize("sample", validate_and_set_email_data)
    def test__validate_and_set_email(self, user_profile_fixture, sample: Dict):
        email, raises = sample["email"], sample["raises"]
        if raises:
            with pytest.raises(InvalidEmailError):
                user_profile_fixture._validate_and_set_email(email)
        else:
            try:
                user_profile_fixture._validate_and_set_email(email)
                assert user_profile_fixture.email == email
            except InvalidEmailError:
                assert False, "InvalidEmailError raised unexpectedly"

    @pytest.mark.parametrize("password,expected", hash_password_data)
    def test__hash_password(self, user_profile_fixture, password: str, expected: str):
        assert user_profile_fixture._hash_password(password) == expected

    def test_set_password(self, user_profile_fixture):
        new_password = "newsecurepassword"
        user_profile_fixture.set_password(new_password)
        assert user_profile_fixture.validate_password(new_password) is True

    @pytest.mark.parametrize("password,expected", validate_password_data)
    def test_validate_password(self, user_profile_fixture, password: str, expected: bool):
        assert user_profile_fixture.validate_password(password) == expected

    @pytest.mark.parametrize("username,email,age,visibility", update_user_data)
    def test_update_user(self, user_profile_fixture, username, email, age, visibility):
        user_profile_fixture.update_user(username=username, email=email, age=age, visibility=visibility)
        if username:
            assert user_profile_fixture.username == username
        if email:
            assert user_profile_fixture.email == email
        if age:
            assert user_profile_fixture.age == age
        assert user_profile_fixture.profile_visibility == visibility

    def test_enable_2fa(self, user_profile_fixture):
        user_profile_fixture.enable_2fa()
        assert user_profile_fixture.two_factor_auth_enabled is True

    def test_delete_user(self, user_profile_fixture):
        user_profile_fixture.delete_user()

        # List of attributes expected to be None after deletion
        attributes = ["username", "email", "age", "_password_hash", "name"]

        # Assert all specified attributes are set to None
        for attr in attributes:
            assert getattr(user_profile_fixture, attr) is None, f"{attr} should be None after deletion"


class TestEmailService:
    @pytest.mark.parametrize("sample", send_verification_email_data)
    def test_send_verification_email(self, mock_request_get, sample):
        # Simulate a failure response by raising an exception
        mock_get = mock_request_get
        mock_get.side_effect = sample["random_numbers"]

        res = EmailService.send_verification_email(sample["email"])

        print(f"Response: {res} --- Expected: {sample['expected']}")
        assert res == sample["expected"]


class TestLogger:
    def test_log_info(self, logger_mock):
        message = "Info message"
        Logger.log_info(message)
        logger_mock.assert_called_once_with(message)

    def test_log_error(self, logger_mock):
        message = "Error message"
        Logger.log_error(message)
        logger_mock.assert_called_once_with(message)


class TestLoadHFModel:
    @patch(target="main.AutoModelForSequenceClassification.from_pretrained")
    @patch(target="main.pipeline")
    def test_load_hf_model(self, mock_pipeline, mock_from_pretrained):
        # Setup mock return values
        mock_model = MagicMock(model={"nlptown/bert-base-multilingual-uncased-sentiment"})
        mock_from_pretrained.return_value = mock_model

        mock_pipe = MagicMock(pipe="custom pipeline")
        mock_pipeline.return_value = mock_pipe

        # Call the function under test
        result = load_hf_model()

        # Assertions to ensure the mocks were called as expected
        mock_from_pretrained.assert_called_once_with("nlptown/bert-base-multilingual-uncased-sentiment")
        # self.assertEqual(result, mock_pipe)
        print(f"Result: {result.pipe} --- Expected: {mock_pipe.pipe}")
