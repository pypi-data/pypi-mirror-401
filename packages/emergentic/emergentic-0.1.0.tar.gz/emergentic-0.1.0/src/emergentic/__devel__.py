"""developer utilities"""
from pathlib import Path
from autilities.pythonic.packaging import find_package_dir
from autilities.testing import watch as test_watcher    


def watch():
    print("not implemented yet.")


def dev():
    """start a test driven dev/agent session"""

    pkg_path = find_package_dir()
    test_watcher(root=pkg_path)
