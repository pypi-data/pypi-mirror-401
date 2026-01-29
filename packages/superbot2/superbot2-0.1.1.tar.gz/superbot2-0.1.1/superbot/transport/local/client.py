"""
Policy Client implementation using socket and memfd+mmap transport
"""

import socket
import time
import os
from loguru import logger
from .memfd_mmap_transport import MemfdMmapTransport


class PolicyClient:
    """
    Client that sends policy requests via UDS and memfd+mmap.
    """

    def __init__(self, socket_name):
        self.socket_path = f"/tmp/{socket_name}.sock"
        self.transport = MemfdMmapTransport()

    def __del__(self):
        """Cleanup when client is destroyed."""
        try:
            # Perform comprehensive cleanup of any remaining memfds
            self.transport._cleanup_tracked_memfds()
            # Also run cleanup for old memfds that might have lingered
            self.transport._cleanup_old_memfds(max_age_seconds=10)  # Cleanup very old memfds
        except Exception:
            # Don't let cleanup errors propagate during destruction
            pass

    def call(self, inputs):
        """
        Call the policy server with inputs.
        """
        # Connect to server
        conn = self.transport.connect_socket(self.socket_path)

        # Initialize cleanup variables
        request_fd = (
            None  # In case we need to clean up request memfd if server fails
        )
        response_fd_to_cleanup = None

        try:
            # Serialize inputs metadata
            metadata_bytes = self.transport.serialize_metadata(inputs)

            # Calculate total size needed for data in memfd
            total_size = sum(
                v.nbytes if hasattr(v, "nbytes") else len(str(v).encode("utf-8"))
                for v in inputs.values()
                if hasattr(v, "nbytes") or isinstance(v, str)
            )

            if total_size > 0:
                # Create memfd for sending data
                request_fd = self.transport.create_memfd(total_size)

                # Map the memfd to memory
                mapped_memory = self.transport.map_memfd(request_fd, total_size)

                # Parse metadata to get layout
                metadata = self.transport.deserialize_metadata(metadata_bytes)

                # Write data to mapped memory
                self.transport.write_data_to_mapped_memory(mapped_memory, inputs, metadata)

                # Send metadata size
                conn.send(len(metadata_bytes).to_bytes(4, byteorder="little"))
                # Send metadata
                conn.send(metadata_bytes)

                # Send memfd info (send the fd number as identifier)
                memfd_info = f"{request_fd}:{total_size}"
                conn.send(len(memfd_info).to_bytes(4, byteorder="little"))

                # Send the actual file descriptor using SCM_RIGHTS
                from .memfd_mmap_transport import send_fds
                send_fds(conn, memfd_info.encode("utf-8"), [request_fd])

                # Close the mapped memory but keep the fd open for the server to use
                mapped_memory.close()
            else:
                # Send metadata size
                conn.send(len(metadata_bytes).to_bytes(4, byteorder="little"))
                # Send metadata
                conn.send(metadata_bytes)

            # Receive response metadata size
            response_metadata_size_bytes = conn.recv(4)
            response_metadata_size = int.from_bytes(
                response_metadata_size_bytes, byteorder="little"
            )

            # Receive response metadata
            response_metadata_bytes = b""
            remaining = response_metadata_size
            while remaining > 0:
                chunk = conn.recv(remaining)
                if not chunk:
                    break
                response_metadata_bytes += chunk
                remaining -= len(chunk)

            # Deserialize response metadata
            response_metadata = self.transport.deserialize_metadata(
                response_metadata_bytes
            )

            # Check if response contains memfd data
            has_memfd_response = any(
                v.get("type") == "ndarray" or v.get("type") == "str"
                for v in response_metadata.values()
            )

            if has_memfd_response:
                # Receive memfd info for response
                response_memfd_info_size_bytes = conn.recv(4)
                response_memfd_info_size = int.from_bytes(
                    response_memfd_info_size_bytes, byteorder="little"
                )

                # Receive the response file descriptor using SCM_RIGHTS
                from .memfd_mmap_transport import recv_fds
                response_memfd_info_bytes, response_fds = recv_fds(conn, response_memfd_info_size, 1)

                if response_fds:
                    # Get the received response file descriptor
                    response_fd = response_fds[0]

                    # Parse the memfd info to get the size
                    response_memfd_info = response_memfd_info_bytes.decode("utf-8").split(":")
                    response_size = int(response_memfd_info[1])

                    # Map the received response memfd to memory
                    response_mapped_memory = self.transport.map_memfd(response_fd, response_size)

                    # Read response data from mapped memory
                    result = self.transport.read_data_from_mapped_memory(
                        response_mapped_memory, response_metadata
                    )

                    # Close the mapped memory and the received fd
                    response_mapped_memory.close()
                    os.close(response_fd)
                else:
                    # Response was in metadata
                    result = {
                        k: v["data"]
                        for k, v in response_metadata.items()
                        if v["type"] == "raw"
                    }
            else:
                # Response was in metadata
                result = {
                    k: v["data"]
                    for k, v in response_metadata.items()
                    if v["type"] == "raw"
                }

        except Exception:
            # If there was an exception during communication, we may need to clean up
            # the request memfd if the server didn't get a chance to
            if request_fd:
                try:
                    # Attempt to clean up request memfd if server hasn't
                    os.close(request_fd)
                except OSError:
                    # Already closed by server
                    pass
                except Exception as e:
                    logger.warning(
                        f"Could not close request memfd {request_fd}: {e}"
                    )
            raise  # Re-raise the exception
        finally:
            # Perform cleanup of response memfd if needed (backup cleanup)
            if response_fd_to_cleanup:
                try:
                    os.close(response_fd_to_cleanup)
                except OSError:
                    # Already closed
                    pass
                except Exception as e:
                    logger.warning(
                        f"Could not close response memfd {response_fd_to_cleanup}: {e}"
                    )
            conn.close()

        return result
