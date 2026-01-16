"""
VibeKit CLI - Configure AI coding workflows in SaaS, execute locally.

Getting Started:
    $ pip install vibekit-cli
    $ vk login              # Authenticate
    $ vk link owner/repo    # Link to project
    $ vk pull               # Sync config from SaaS

Commands:
    vk login                # Authenticate with VibeKit
    vk pull                 # SaaS -> Local
    vk push                 # Local -> SaaS
    vk status               # View sync status

Documentation: https://vkcli.com/docs
"""

__version__ = "0.1.0"
__author__ = "ZySec AI"
__license__ = "MIT"

# Public API
from vk.auth import AuthClient
from vk.client import VKClient
from vk.generator import ClaudeMdGenerator
from vk.sync import SyncClient

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "AuthClient",
    "VKClient",
    "SyncClient",
    "ClaudeMdGenerator",
]
