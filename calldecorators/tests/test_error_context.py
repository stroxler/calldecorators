from ..decorators import (
    error_context,
)


def assert_error_with_prefix(prefix, func, *args, **kwargs):
    try:
        print args
        func(*args, **kwargs)
        raise AssertionError("No error raised")
    except Exception as e:
        if not e.args[0].startswith(prefix):
            print "expected prefix %r" % prefix
            print "actual message %r" % e.args[0]
            raise


def test_error_context_no_formatting():

    @error_context("error context")
    def f(x, y):
        raise ValueError("an error")

    assert_error_with_prefix(
        "error context:\nan error",
        f, 1, 2,
    )


def test_error_context_simple_formatting():

    @error_context("error context {x} {y} {z}")
    def f(x, y, z):
        raise ValueError("an error")

    assert_error_with_prefix(
        "error context 1 2 3:\nan error",
        f, 1, 2, 3
    )


def test_error_context_formatting_with_defaults():

    @error_context("error context {x} {y} {z}")
    def f(x, y=2, z=2):
        raise ValueError("an error")

    assert_error_with_prefix(
        "error context 1 2 3:\nan error",
        f, 1, z=3
    )


def test_error_context_formatting_with_packed_args():

    @error_context("error context {fargs} {fkwargs}")
    def f(*fargs, **fkwargs):
        raise ValueError("an error")

    assert_error_with_prefix(
        "error context (1, 2) {'z': 3}:\nan error",
        f, 1, 2, z=3
    )


def test_error_context_failed_formatting():

    @error_context("error context {xx}")
    def f(x, y):
        raise ValueError("an error")

    assert_error_with_prefix(
        ("error context {xx}\n"
         "...FAILED TO FORMAT args=(1,) kwargs={'y': 2}:"
         "\nan error"),
        f, 1, y=2
    )
