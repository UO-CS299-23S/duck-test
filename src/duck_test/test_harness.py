"""Snippets of what I would like in a test harness
that avoids some aggravations of unittest.
"""
from typing import Callable
import inspect
import dis

"""A collection of test cases we can run"""

FOUND_TESTS: list[Callable] = []
SUCCESSES: list[str] = []
FAILURES: list[str] = []
ERRORS: list[str] = []
TESTS_FOR: dict[str, int] = {}


def init():
    """In case the module is already loaded."""
    global FOUND_TESTS, SUCCESSES, FAILURES, ERRORS
    FOUND_TESTS = []
    TESTS_FOR = []
    SUCCESSES = []
    FAILURES = []
    ERRORS = []

def record_coverage(f: Callable):
    """Record that we have a test case for f"""
    name = f.__name__
    if name not in TESTS_FOR:
        TESTS_FOR[name] = 0
    TESTS_FOR[name] += 1

def dump(f: Callable):
    """What do the instructions look like?"""
    instructions = dis.get_instructions(f)
    dis.dis(f)
    for i in instructions:
        i_name = i.opname
        print(i.opname)
        if i.opname == "CALL":
            print(i)


def test_case(subject = None) -> Callable:
    """Wrap this function in test case harness
    and mark it as a callqble test case.
    """
    def register(f: callable):
        def harness():
            """Run the test function within an assertion error checker."""
            try:
                f()
                SUCCESSES.append(f.__name__)
            except AssertionError as err:
                if len(err.args) > 0:
                    desc = f": {err.args[0]}"
                else:
                    desc = ""
                FAILURES.append(f"{f.__name__}(){desc}")
                print(err)
            except Exception as err:
                ERRORS.append(f.__name__)
        harness.__name__ = f.__name__
        FOUND_TESTS.append(harness)
        # For test thoroughness checking, record
        # the (claimed) coverage of subject
        # dump(f)  # We did this to understand what we could clean from bytecode
        if isinstance(subject, Callable):
            record_coverage(subject)
        elif isinstance(subject, list):
            for called in subject:
                record_coverage(called)
        return harness
    return register

def coverage() -> list[str]:
    """Which functions did we find tests for?"""
    return [name for name in TESTS_FOR.keys()]

def uncovered(m) -> list[str]:
    """Have we covered all the functions in a module?"""
    missing = []
    covered = set(TESTS_FOR.keys())
    members = inspect.getmembers_static(m)
    f_type = type(lambda x: x + 1)
    for member in members:
        # Check coverage of classes and functions
        m_name, m_value = member
        if isinstance(m_value, type) or isinstance(m_value, f_type):
            if m_name not in covered:
                missing.append(m_name)
    return missing


def main():
    for test in FOUND_TESTS:
        print(f"Testing {test.__name__}")
        test()
    print(f"** {len(SUCCESSES)} successes")
    print(f"** {len(FAILURES)} failures")
    print("\n".join(FAILURES))
    print(f"** {len(ERRORS)} other errors")
    print("\n".join(ERRORS))


