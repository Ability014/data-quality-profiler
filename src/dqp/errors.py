class DqpError(Exception):
    """Base for errors dqp raises deliberately — expected, user-facing."""


class SchemaError(DqpError):
    """The data doesn't match the expected shape (e.g. ragged rows)."""
