"""
Unified Policy Client that automatically switches between local and remote modes
"""

from .local.client import PolicyClient as LocalPolicyClient
from .remote.client import PolicyClient as RemotePolicyClient


class PolicyClient:
    """
    Unified client that automatically switches between local and remote modes based on parameters.
    If socket_name is provided, uses local mode. Otherwise uses remote mode with URL.
    """

    def __init__(self, socket_name=None, url="tcp://localhost:5555"):
        if socket_name is not None:
            # Use local mode with socket
            self._client = LocalPolicyClient(socket_name=socket_name)
            self.mode = "local"
        else:
            # Use remote mode with URL
            self._client = RemotePolicyClient(url=url)
            self.mode = "remote"

    def call(self, inputs):
        """
        Call the policy server with inputs.
        """
        return self._client.call(inputs)

    def __del__(self):
        """Cleanup when client is destroyed."""
        if hasattr(self, '_client'):
            del self._client