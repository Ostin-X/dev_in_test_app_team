import logging
import os

import allure
import pytest
from dotenv import load_dotenv

from tests.funcs import login_to_app

load_dotenv()
invalid_email = 'invalid_email@example.com'
wrong_format_email1 = 'invalid_email'
wrong_format_email2 = 'invalid_email@example'
wrong_format_email3 = 'example.com'
invalid_pass = 'invalid_password'
qa_email = os.getenv('QA_EMAIL')
qa_pass = os.getenv('QA_PASSWORD')


@pytest.mark.skip
def test_some_test(caplog):
    with caplog.at_level(logging.INFO):
        logging.info(f'Stupid test')
    assert 1 == 1


@pytest.mark.parametrize("email, password", [
    (qa_email, qa_pass),
    (wrong_format_email1, qa_pass),  # fail on purpose
])
@allure.title("Test Login with Valid Credentials")
def test_login_right(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == True else "failed"} - email: {email},'
            f' password: {password}, expected: True')

    with allure.step("Check login status"):
        allure.attach(f'is_login: {is_login}', name='is_login', attachment_type=allure.attachment_type.TEXT)
        allure.attach(f'reason: {reason}', name='reason', attachment_type=allure.attachment_type.TEXT)
        assert is_login is True, f'Login failed for email: {email}, password: {password}. Reason: {reason}'
        assert reason is None, f'Unexpected reason: {reason} for email: {email}, password: {password}'


@pytest.mark.parametrize("email, password", [
    (invalid_email, qa_pass),
    (qa_email, invalid_pass),
    (qa_email, qa_pass),  # fail on purpose
    (wrong_format_email1, qa_pass),  # fail on purpose

])
@allure.title("Test Login with Invalid Credentials")
def test_login_wrong_creds(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == False else "failed"} - email: {email},'
            f' password: {password}, expected: False')

    with allure.step("Check login status"):
        allure.attach(f'is_login: {is_login}', name='is_login', attachment_type=allure.attachment_type.TEXT)
        allure.attach(f'reason: {reason}', name='reason', attachment_type=allure.attachment_type.TEXT)
        assert is_login is False, f'Login succeeded for invalid creds - email: {email}, password: {password}'
        assert reason == 'Невірний логін або пароль', f'Unexpected reason: {reason} for email: {email}, password: {password}'


@pytest.mark.parametrize("email, password", [
    (wrong_format_email1, qa_pass),
    (wrong_format_email2, qa_pass),
    (wrong_format_email3, qa_pass),
    (invalid_email, invalid_pass),  # fail on purpose
    (qa_email, qa_pass),  # fail on purpose
])
@allure.title("Test Login with Wrong Email Format")
def test_login_wrong_email_format(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == False else "failed"} - email: {email},'
            f' password: {password}, expected: False')
    with allure.step("Check login status"):
        allure.attach(f'is_login: {is_login}', name='is_login', attachment_type=allure.attachment_type.TEXT)
        allure.attach(f'reason: {reason}', name='reason', attachment_type=allure.attachment_type.TEXT)
        assert is_login is False, f'Login succeeded for invalid creds - email: {email}, password: {password}'
        assert reason == 'Невірний формат електронної пошти', f'Unexpected reason: {reason} for email: {email}, password: {password}'
