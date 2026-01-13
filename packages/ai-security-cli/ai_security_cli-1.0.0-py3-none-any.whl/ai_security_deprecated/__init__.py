"""
DEPRECATED: ai-security-cli has been renamed to aisentry.

Please update your installation:
    pip uninstall ai-security-cli
    pip install aisentry

The new CLI command is: aisentry
"""
import warnings

warnings.warn(
    "\n\n"
    "=" * 60 + "\n"
    "DEPRECATION WARNING: ai-security-cli is now 'aisentry'\n"
    "=" * 60 + "\n\n"
    "Please update your installation:\n"
    "    pip uninstall ai-security-cli\n"
    "    pip install aisentry\n\n"
    "The new CLI command is: aisentry\n"
    "=" * 60 + "\n",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from aisentry for backwards compatibility
from aisentry import *
