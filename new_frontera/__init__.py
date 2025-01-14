from __future__ import absolute_import

from ._version import get_versions
from .core.components import Backend, DistributedBackend, Middleware
from .core.models import Request, Response
from .settings import Settings
from .utils.tester import FrontierTester

__version__ = get_versions()["version"]
del get_versions

from . import _version
__version__ = _version.get_versions()['version']
