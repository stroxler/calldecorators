from tdxutil.exceptions import try_with_lazy_context
from inspectcall.wrapping import wraps
from inspectcall.reflection import get_callargs


def error_context(context_message):
    """
    Decorator for wrapping any function in a call to
    `tdxutil.exceptions.try_with_lazy_context`, with a context message that
    will be formatted based on the arguments of the call.

    PARAMETERS
    ----------
    context_message : str
        A message to prepend to any exceptions thrown by the function
        we are decorating. If an exception is thrown, we will format
        the context message with the arguments (including defaults)
        before raising.

    RETURNS
    -------
    decorator : function
        A decorator to wrap functions with error context prepending.
        If there's a problem formatting the message with the call
        arguments, the original message is prepended along with a
        message indicating a formatting error and the args / kwargs
        of the actual call.

    EXAMPLE
    -------

    >>> @error_context("In call, x={x}, y={y}, z={z}, fkwargs={fkwargs}")
    >>> def f(x, y=2, z=3, **fkwargs): raise Exception("error")

    >>> f(1, z=4, this='that')
    # ...traceback information, which isn't affected...
    # Exception: In call, x=1, y=2, z=4, fkwargs={'this': 'that'}:
    #    error

    NOTE
    ----
    This decorator depends on `inspectcall`, which requires information
    that can be clobbered by many third-party decorator functions.
    To ensure that the argument information is still available when
    this decorator runs, you must ensure that all the decorators in
    between the raw function and this use `inspectcall.wrapping.wraps`.

    So, for example, if you are decorating a function staticmethod,
    make sure that this decorator is *underneath* the `@staticmethod`.

    """
    def decorator(f):

        def format_context_message(*args, **kwargs):
            arguments = get_callargs(f, *args, **kwargs)
            print arguments
            try:
                return context_message.format(**arguments)
            except:
                return (
                    context_message +
                    '\n...FAILED TO FORMAT args=%r kwargs=%r' % (args, kwargs)
                )

        @wraps(f)
        def wrapped(*args, **kwargs):
            def error_context():
                return format_context_message(*args, **kwargs)
            return try_with_lazy_context(error_context, f, *args, **kwargs)

        return wrapped

    return decorator

