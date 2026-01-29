"""
Policy Server implementation using ZeroMQ for remote transport with efficient multipart messaging
"""

import zmq
import json
import numpy as np
from loguru import logger
import io


class PolicyServer:
    """
    Server that receives policy requests via ZeroMQ using efficient multipart messaging.
    """

    def __init__(self, policy_func, url="tcp://*:5555", warmup_inputs=None):
        self.policy_func = policy_func
        self.url = url
        self.context = zmq.Context()
        self.socket = None
        self.running = False
        self.warmup_inputs = warmup_inputs

    def warmup(self):
        """Perform warmup by simulating a full request cycle."""
        if self.warmup_inputs is not None:
            logger.info("Performing server warmup...")
            try:
                # Simulate the full request processing to trigger all initialization paths
                result = self.policy_func(self.warmup_inputs)
                logger.info("Warmup completed successfully.")
            except Exception as e:
                logger.error(f"Warmup failed: {e}")
                logger.exception(e)
        else:
            logger.info("No warmup inputs provided, skipping warmup.")

    def serve_forever(self):
        """Start the server and listen for connections."""
        self.socket = self.context.socket(zmq.REP)  # Reply socket
        self.socket.bind(self.url)
        self.running = True

        # Perform warmup after socket setup but before entering the main loop
        self.warmup()

        logger.info(f"Policy server listening on {self.url}")

        try:
            while self.running:
                try:
                    # Receive multipart message
                    message_parts = self.socket.recv_multipart()

                    # First part is the header (JSON)
                    header_json = message_parts[0].decode('utf-8')
                    header = json.loads(header_json)

                    # Remaining parts are the raw data
                    data_parts = message_parts[1:]

                    # Reconstruct the inputs from header and data parts
                    inputs = self._reconstruct_inputs(header, data_parts)

                    # Process the request
                    result = self.policy_func(inputs)

                    # Serialize the response using the same efficient format
                    response_parts = self._serialize_response(result)

                    # Send the response back as multipart
                    self.socket.send_multipart(response_parts)

                except Exception as e:
                    if self.running:
                        logger.error(f"Error handling request: {e}")
                        logger.exception(e)

                        # Send error response as multipart
                        error_header = json.dumps({"error": str(e)}).encode('utf-8')
                        self.socket.send_multipart([error_header])
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
        finally:
            self.stop()

    def _reconstruct_inputs(self, header, data_parts):
        """
        Reconstruct inputs from header and raw data parts.
        """
        inputs = {}
        data_idx = 0

        # Extract metadata from header
        arrays_info = header.get('arrays', {})
        scalars = header.get('scalars', {})

        # Reconstruct scalar values
        for key, value in scalars.items():
            inputs[key] = value

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
            inputs[key] = array

        return inputs

    def _serialize_response(self, result):
        """
        Serialize response using efficient multipart format.
        """
        # Build header with metadata
        header = {'arrays': {}, 'scalars': {}}

        # Separate arrays and scalars in the result
        data_parts = []
        for key, value in result.items():
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

    def stop(self):
        """Stop the server."""
        self.running = False
        if self.socket:
            self.socket.close()
        if self.context:
            self.context.term()