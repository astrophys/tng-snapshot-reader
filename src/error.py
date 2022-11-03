# Author : Ali Snedden
# Date   : 11/1/22
# License: MIT
"""Module that provides function for error handling.
"""
import sys
def exit_with_error(String):
    """
    Prints String to stderr, exits with error code 1

    Args:
        String      : string to print then exit

    Returns :
        N/A
    """
    sys.stderr.write(String)
    sys.exit(1)


def warning(String):
    """
    Prints String to stderr,

    Args:
        String      : string to print then exit

    Returns :
        N/A
    """
    sys.stderr.write(String)
