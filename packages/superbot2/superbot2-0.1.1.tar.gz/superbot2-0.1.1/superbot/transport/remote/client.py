"""
Policy Client implementation using ZeroMQ for remote transport with efficient multipart messaging
"""

import zmq
import json
import numpy as np
from loguru import logger


class PolicyClient:
    """
    Client that sends policy requests via ZeroMQ to a remote server using efficient multipart messaging.
    """

    def __init__(self, url="tcp://localhost:5555"):
        self.url = url
        self.context = zmq.Context()
        self.socket = None
        self._connect()

    def _connect(self):
        """Establish connection to the server."""
        if self.socket:
            self.socket.close()

        self.socket = self.context.socket(zmq.REQ)  # Request socket
        self.socket.connect(self.url)

    def call(self, inputs):
        """
        Call the policy server with inputs using efficient multipart messaging.
        """
        try:
            # Serialize the inputs using multipart format
            message_parts = self._serialize_request(inputs)

            # Send the multipart request
            self.socket.send_multipart(message_parts)

            # Receive the multipart response
            response_parts = self.socket.recv_multipart()

            # Deserialize the response
            result = self._deserialize_response(response_parts)

            # Check if there was an error in processing
            if isinstance(result, dict) and "error" in result:
                raise RuntimeError(f"Server error: {result['error']}")

            return result

        except Exception as e:
            logger.error(f"Error in client call: {e}")
            raise

    def _serialize_request(self, inputs):
        """
        Serialize request using efficient multipart format.
        """
        # Build header with metadata
        header = {'arrays': {}, 'scalars': {}}

        # Separate arrays and scalars in the inputs
        data_parts = []
        for key, value in inputs.items():
            if isinstance(value, np.ndarray):
                # Store array metadata in header
                header['arrays'][key] = {
                    'shape': value.shape,
                    'dtype': str(value.dtype),
                    'size': value.nbytes
                }
                # Add raw data as a part
                data_parts.append(memoryview(value))
            else:
                # Store scalar values directly in header
                header['scalars'][key] = value

        # Encode header as JSON
        header_bytes = json.dumps(header).encode('utf-8')

        # Return multipart message: [header, data_part1, data_part2, ...]
        return [header_bytes] + data_parts

    def _deserialize_response(self, response_parts):
        """
        Deserialize response from multipart format.
        """
        # First part is the header (JSON)
        header_json = response_parts[0].decode('utf-8')
        header = json.loads(header_json)

        # Remaining parts are the raw data
        data_parts = response_parts[1:]

        # Reconstruct the result from header and data parts
        result = {}
        data_idx = 0

        # Extract metadata from header
        arrays_info = header.get('arrays', {})
        scalars = header.get('scalars', {})

        # Reconstruct scalar values
        for key, value in scalars.items():
            result[key] = value

        # Reconstruct array values from data parts
        for key, array_info in arrays_info.items():
            shape = tuple(array_info['shape'])
            dtype = np.dtype(array_info['dtype'])
            size_in_bytes = array_info['size']

            # Get the corresponding data part
            raw_data = data_parts[data_idx]
            data_idx += 1

            # Create numpy array from raw data
            array = np.frombuffer(raw_data, dtype=dtype).reshape(shape)
            result[key] = array

        return result

    def __del__(self):
        """Cleanup when client is destroyed."""
        try:
            if self.socket:
                self.socket.close()
            if self.context:
                self.context.term()
        except Exception:
            # Don't let cleanup errors propagate during destruction
            pass