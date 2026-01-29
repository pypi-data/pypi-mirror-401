"""
Unified Policy Server that automatically switches between local and remote modes
"""

from .local.server import PolicyServer as LocalPolicyServer
from .remote.server import PolicyServer as RemotePolicyServer


class PolicyServer:
    """
    Unified server that automatically switches between local and remote modes based on parameters.
    If socket_name is provided, uses local mode. Otherwise uses remote mode with URL.
    """

    def __init__(self, policy_func, socket_name=None, url="tcp://*:5555", warmup_inputs=None):
        if socket_name is not None:
            # Use local mode with socket
            self._server = LocalPolicyServer(policy_func, socket_name=socket_name, warmup_inputs=warmup_inputs)
            self.mode = "local"
        else:
            # Use remote mode with URL
            self._server = RemotePolicyServer(policy_func, url=url, warmup_inputs=warmup_inputs)
            self.mode = "remote"

    def serve_forever(self):
        """
        Start the server and listen for connections.
        """
        self._server.serve_forever()

    def stop(self):
        """
        Stop the server.
        """
        if hasattr(self._server, 'stop'):
            self._server.stop()

    def warmup(self):
        """
        Perform warmup by simulating a full request cycle.
        """
        if hasattr(self._server, 'warmup'):
            self._server.warmup()

