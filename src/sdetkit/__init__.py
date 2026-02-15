"""Public package exports for sdetkit."""

from .sqlite_scalar import ScalarFunctionRegistrationError, register_scalar_function

__all__ = ["ScalarFunctionRegistrationError", "register_scalar_function"]
