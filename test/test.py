from subprocess import check_output, call

import os


EXPECTED_RETURN_CODE_WRONG_USAGE = 3
EXPECTED_RETURN_CODE_COMMAND_NOT_FOUND = 3
EXPECTED_RETURN_CODE_INTERNAL_ERROR = 3


def test_simple():
    os.environ["SSH_ORIGINAL_COMMAND"] = "simple"
    assert b"TEST_SIMPLE\n" == check_output(["./ssh-restrict", "./test/config"])


def test_args():
    os.environ["SSH_ORIGINAL_COMMAND"] = "args 23 42"
    assert b"23 42\n" == check_output(["./ssh-restrict", "./test/config"])


def test_args_type_overwriting():
    os.environ["SSH_ORIGINAL_COMMAND"] = "args text 42"
    assert b"text 42\n" == check_output(["./ssh-restrict", "./test/config"])


def test_undefined():
    os.environ["SSH_ORIGINAL_COMMAND"] = "undefined"
    assert call(["./ssh-restrict", "./test/config"]) == EXPECTED_RETURN_CODE_COMMAND_NOT_FOUND


def test_not_found():
    os.environ["SSH_ORIGINAL_COMMAND"] = "not_found"
    assert call(["./ssh-restrict", "./test/config"]) == EXPECTED_RETURN_CODE_WRONG_USAGE


def test_regex_exception():
    os.environ["SSH_ORIGINAL_COMMAND"] = "bad_regex test"
    assert call(["./ssh-restrict", "./test/config"]) == EXPECTED_RETURN_CODE_INTERNAL_ERROR


def test_escape_exception():
    os.environ["SSH_ORIGINAL_COMMAND"] = "bad_escape"
    assert call(["./ssh-restrict", "./test/config"]) == EXPECTED_RETURN_CODE_INTERNAL_ERROR


def test_command_formatting():
    os.environ["SSH_ORIGINAL_COMMAND"] = "bad_formatting 123"
    assert call(["./ssh-restrict", "./test/config"]) == EXPECTED_RETURN_CODE_INTERNAL_ERROR

def test_upper_lower():
    os.environ["SSH_ORIGINAL_COMMAND"] = "UpperLower"
    assert b"UpperLower\n" == check_output(["./ssh-restrict", "./test/config"])
