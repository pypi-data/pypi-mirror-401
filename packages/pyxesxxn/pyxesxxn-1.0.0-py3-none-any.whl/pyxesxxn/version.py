# SPDX-FileCopyrightText: PyXESXXN Contributors
#
# SPDX-License-Identifier: MIT

"""Version information and semantic versioning management for PyXESXXN package.

This module provides comprehensive version management with semantic versioning
support, automatic version detection, and compatibility checking.

Examples
--------
>>> import pyxesxxn as px
>>> px.__version__
'1.0.0'
>>> px.__version_info__
VersionInfo(major=1, minor=0, patch=0, prerelease=None, build=None)
>>> px.is_compatible_with('1.0.0')
True
>>> px.get_version_summary()
'PyXESXXN 1.0.0 - Python for eXtended Energy System Analysis'

"""

import logging
import re
from dataclasses import dataclass
from typing import Optional, Tuple, Union

try:
    from importlib.metadata import version
except ImportError:
    # Fallback for Python < 3.8
    from importlib_metadata import version

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VersionInfo:
    """Semantic version information container."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None
    
    def __str__(self) -> str:
        """Return semantic version string."""
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version_str += f"-{self.prerelease}"
        if self.build:
            version_str += f"+{self.build}"
        return version_str
    
    @property
    def base_version(self) -> str:
        """Return base version (major.minor.patch)."""
        return f"{self.major}.{self.minor}.{self.patch}"
    
    @property
    def major_minor(self) -> str:
        """Return major.minor version."""
        return f"{self.major}.{self.minor}"


def parse_version(version_string: str) -> VersionInfo:
    """Parse semantic version string into VersionInfo object.
    
    Parameters
    ----------
    version_string : str
        Version string to parse (e.g., "1.2.3", "2.0.0-beta.1")
    
    Returns
    -------
    VersionInfo
        Parsed version information
    
    Raises
    ------
    ValueError
        If version string is not valid semantic version
    """
    # Basic semantic version pattern
    pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$"
    match = re.match(pattern, version_string)
    
    if not match:
        raise ValueError(f"Invalid semantic version: {version_string}")
    
    major, minor, patch = map(int, match.groups()[:3])
    prerelease = match.group(4)
    build = match.group(5)
    
    return VersionInfo(major, minor, patch, prerelease, build)


def is_compatible(version1: str, version2: str) -> bool:
    """Check if two versions are compatible.
    
    Compatibility rules:
    - Same major version: compatible
    - Different major version: incompatible
    - Prerelease versions are only compatible with exact matches
    
    Parameters
    ----------
    version1 : str
        First version string
    version2 : str
        Second version string
    
    Returns
    -------
    bool
        True if versions are compatible
    """
    try:
        v1 = parse_version(version1)
        v2 = parse_version(version2)
        
        # Prerelease versions require exact match
        if v1.prerelease or v2.prerelease:
            return str(v1) == str(v2)
        
        # Same major version are compatible
        return v1.major == v2.major
        
    except ValueError:
        # Fallback to string comparison for invalid versions
        return version1 == version2


def check_pyxesxxn_version(version_string: str) -> None:
    """Check if the installed PyXESXXN version was resolved correctly."""
    if version_string.startswith("0.0"):
        logger.warning(
            "The correct version of PyXESXXN could not be resolved. This is likely due to "
            "a local clone without pulling tags. Please run `git fetch --tags`."
        )


def get_version() -> str:
    """Get the PyXESXXN version, with fallback to static version."""
    try:
        return version("pyxesxxn")
    except Exception:
        # Fallback to static version when package is not installed
        return "1.0.0"


def get_version_info() -> VersionInfo:
    """Get PyXESXXN version as VersionInfo object."""
    return parse_version(__version__)


def is_compatible_with(other_version: str) -> bool:
    """Check if current PyXESXXN version is compatible with another version."""
    return is_compatible(__version__, other_version)


def get_version_summary() -> str:
    """Get formatted version summary string."""
    version_info = get_version_info()
    summary = f"PyXESXXN {version_info} - Python for eXtended Energy System Analysis"
    
    if version_info.prerelease:
        summary += f" (Prerelease: {version_info.prerelease})"
    if version_info.build:
        summary += f" (Build: {version_info.build})"
    
    return summary


# Static version information for packaging
__version__ = "1.0.0"
__version_info__ = parse_version(__version__)
__version_base__ = __version_info__.base_version
__version_major_minor__ = __version_info__.major_minor

# Dynamic version resolution when package is installed
try:
    installed_version = get_version()
    if installed_version != "1.0.0":  # Only update if different from static version
        __version__ = installed_version
        __version_info__ = parse_version(__version__)
        __version_base__ = __version_info__.base_version
        __version_major_minor__ = __version_info__.major_minor
        
        # Check pyxesxxn version
        check_pyxesxxn_version(__version__)
except Exception:
    # Use static version if dynamic resolution fails
    pass
