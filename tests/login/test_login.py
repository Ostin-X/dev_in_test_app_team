import logging
import os

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
def test_login_right(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == True else "failed"} - email: {email},'
            f' password: {password}, expected: True')
    assert is_login is True
    assert reason is None


@pytest.mark.parametrize("email, password", [
    (invalid_email, qa_pass),
    (qa_email, invalid_pass),
    (qa_email, qa_pass),  # fail on purpose
    (wrong_format_email1, qa_pass),  # fail on purpose

])
def test_login_wrong_creds(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == False else "failed"} - email: {email},'
            f' password: {password}, expected: False')
    assert is_login is False
    assert reason == 'Невірний логін або пароль'


@pytest.mark.parametrize("email, password", [
    (wrong_format_email1, qa_pass),
    (wrong_format_email2, qa_pass),
    (wrong_format_email3, qa_pass),
    (invalid_email, invalid_pass),  # fail on purpose
    (qa_email, qa_pass),  # fail on purpose
])
def test_login_wrong_email_format(user_login_fixture, email, password, caplog):
    is_login, reason = login_to_app(user_login_fixture, email, password)

    with caplog.at_level(logging.INFO):
        logging.info(
            f'Test {"passed" if is_login == False else "failed"} - email: {email},'
            f' password: {password}, expected: False')
    assert is_login is False
    assert reason == 'Невірний формат електронної пошти'
