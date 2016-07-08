Decorators, with the ability to use call arguments
--------------------------------------------------

By using the `inspectcall` library, `calldecorators` decorators
can make use of call arguments to functions at runtime, and
preserves function signature metadata (which is clobbered by most
decorators) so that this functionality works even when decorators
are stacked.

The `error_context` decorator uses functionality from
`tdxutil.exceptions.try_with_lazy_context` to wrap a function call
in an error handler that can prepend contextual information to an
error without affecting the stacktrace. This allows errors raised
b low-level code, which may not have enough information to construct
error messages indicating what was going on, to be made far more
informative.
