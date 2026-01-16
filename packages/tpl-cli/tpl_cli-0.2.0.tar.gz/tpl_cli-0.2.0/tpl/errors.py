class TPLError(Exception):
    """Base exception for tpl runtime errors."""


class GitError(TPLError):
    """Raised when git commands fail or return unexpected output."""


class TemplateError(TPLError):
    """Raised for template metadata, config parsing, or rendering failures."""
