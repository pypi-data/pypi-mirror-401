"""cosmo-ent: Cosmopolitan builds of ent(1) as a Python package.

This package provides the ent(1) random sequence tester built with Cosmopolitan libc,
allowing entropy analysis and randomness testing across multiple platforms from a single
universal binary.

Example:
    >>> import cosmo_ent
    >>> result = cosmo_ent.run('random_data.bin')
    >>> print(result.stdout.decode())
    Entropy = 7.998814 bits per byte.
    ...

    >>> # Or use from command line:
    $ cosmo-ent random_data.bin
    Entropy = 7.998814 bits per byte.
"""

import platform
import subprocess
from pathlib import Path
from typing import Union, Optional

from ._version import __version__

__all__ = ["run", "get_binary_path"]


def get_binary_path() -> Path:
    """Get the path to the ent.com binary.

    Returns:
        Path object pointing to the ent.com binary.

    Raises:
        FileNotFoundError: If the binary cannot be found.
    """
    binary_path = Path(__file__).parent / "data" / "ent.com"
    if not binary_path.exists():
        raise FileNotFoundError(
            f"ent.com binary not found at {binary_path}. "
            "The package may not be properly installed."
        )
    return binary_path


def get_base_command() -> list[str]:
    """Get the base command to execute the ent.com binary.

    Returns:
        List of command components to execute the binary.
    """
    binary = get_binary_path()
    if platform.system() == "Windows":
        return [str(binary)]
    else:
        return ["sh", str(binary)]


def run(
    *args: Union[str, Path],
    stdin: Optional[Union[str, bytes]] = None,
    capture_output: bool = True,
    check: bool = False,
    **kwargs
) -> subprocess.CompletedProcess:
    """Run the ent command with the given arguments.

    Args:
        *args: Arguments to pass to the ent command (e.g., file paths, options).
        stdin: Optional input to pass to stdin (str or bytes).
        capture_output: If True, capture stdout and stderr. If False, they go to
                       the parent process streams.
        check: If True, raise CalledProcessError if the command returns non-zero.
        **kwargs: Additional keyword arguments to pass to subprocess.run().

    Returns:
        CompletedProcess instance with returncode, stdout, stderr attributes.

    Raises:
        FileNotFoundError: If the ent.com binary cannot be found.
        subprocess.CalledProcessError: If check=True and command fails.

    Example:
        >>> result = cosmo_ent.run('random.bin')
        >>> print(result.stdout.decode())

        >>> result = cosmo_ent.run('-t', 'data.bin')  # csv output
        >>> print(result.stdout.decode())

        >>> result = cosmo_ent.run('--', stdin=b'\\x00\\x01\\x02\\x03')
        >>> print(result.stdout.decode())
    """
    binary = get_binary_path()

    # Convert all args to strings
    cmd = get_base_command() + [str(arg) for arg in args]

    # Handle stdin
    stdin_input = None
    if stdin is not None:
        if isinstance(stdin, str):
            stdin_input = stdin.encode()
        else:
            stdin_input = stdin

    # Run the command
    return subprocess.run(
        cmd,
        input=stdin_input,
        capture_output=capture_output,
        check=check,
        **kwargs
    )
