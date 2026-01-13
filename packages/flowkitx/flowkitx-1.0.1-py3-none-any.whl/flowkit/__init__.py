"""FlowKit - Simplify async workflows in Python.

FlowKit dramatically reduces async/await complexity with a clean, intuitive API
that automatically handles context management and async patterns.

Example:
    @flowkit.simple
    def fetch_data(url):
        return flowkit.get(url).json().pipe(process_data)
"""

from .core import FlowClient, FlowRequest
from .decorators import simple, flow
from ._version import __version__

__all__ = ["FlowClient", "FlowRequest", "simple", "flow", "__version__"]

# Create default flowkit instance for easy usage
_flowkit = FlowClient()

# Expose main methods at package level
get = _flowkit.get
post = _flowkit.post
put = _flowkit.put
delete = _flowkit.delete
patch = _flowkit.patch
head = _flowkit.head
options = _flowkit.options