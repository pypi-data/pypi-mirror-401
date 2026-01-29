"""
Policy Server implementation using socket and memfd+mmap transport
"""

import os
import socket
import threading
import time
import traceback
from loguru import logger
from .memfd_mmap_transport import MemfdMmapTransport


class PolicyServer:
    """
    Server that receives policy requests via UDS and memfd+mmap.
    """

    def __init__(self, policy_func, socket_name="example_policy", warmup_inputs=None):
        self.policy_func = policy_func
        self.socket_path = f"/tmp/{socket_name}.sock"
        self.transport = MemfdMmapTransport()
        self.running = False
        self.server_socket = None
        # Track response memfds for cleanup
        self.response_memfds = set()
        self.warmup_inputs = warmup_inputs

    def warmup(self):
        """Perform warmup by simulating a full request cycle."""
        if self.warmup_inputs is not None:
            logger.info("Performing server warmup...")
            try:
                # Simulate the full request processing to trigger all initialization paths
                result = self.policy_func(self.warmup_inputs)

                # Also simulate response serialization to warm up that path
                import numpy as np

                has_arrays = any(isinstance(v, np.ndarray) for v in result.values())
                if has_arrays:
                    # Calculate total size needed for response
                    total_response_size = sum(
                        (
                            v.nbytes
                            if hasattr(v, "nbytes")
                            else len(str(v).encode("utf-8"))
                        )
                        for v in result.values()
                        if hasattr(v, "nbytes") or isinstance(v, str)
                    )

                    if total_response_size > 0:
                        # Create and use a memfd to warm up that path too
                        response_fd = self.transport.create_memfd(total_response_size)

                        # Map the memfd to memory
                        response_mapped_memory = self.transport.map_memfd(
                            response_fd, total_response_size
                        )

                        # Write response data to mapped memory
                        response_metadata_with_offsets = (
                            self.transport.serialize_metadata(result)
                        )
                        response_metadata_parsed = self.transport.deserialize_metadata(
                            response_metadata_with_offsets
                        )
                        self.transport.write_data_to_mapped_memory(
                            response_mapped_memory, result, response_metadata_parsed
                        )

                        # Close the mapped memory handle
                        response_mapped_memory.close()

                        # Close the fd
                        os.close(response_fd)

                logger.info("Warmup completed successfully.")
            except Exception as e:
                logger.error(f"Warmup failed: {e}")
                logger.exception(e)
        else:
            logger.info("No warmup inputs provided, skipping warmup.")

    def serve_forever(self):
        """Start the server and listen for connections."""
        self.server_socket = self.transport.create_socket(self.socket_path)
        self.server_socket.listen(5)
        self.running = True

        # Perform warmup after socket setup but before entering the main loop
        self.warmup()

        logger.info(f"Policy server listening on {self.socket_path}")

        try:
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    # Handle each request in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client, args=(conn,)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {e}")
                        logger.exception(e)
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
        finally:
            self.stop()

    def _handle_client(self, conn):
        """Handle a single client request."""
        response_fd_to_clean = None  # Track response memfd for cleanup

        try:
            # Receive the size of the metadata
            size_bytes = conn.recv(4)
            if not size_bytes:
                return

            metadata_size = int.from_bytes(size_bytes, byteorder="little")

            # Receive the metadata
            metadata_bytes = b""
            remaining = metadata_size
            while remaining > 0:
                chunk = conn.recv(remaining)
                if not chunk:
                    break
                metadata_bytes += chunk
                remaining -= len(chunk)

            # Deserialize metadata
            metadata = self.transport.deserialize_metadata(metadata_bytes)

            # Check if we need to receive memfd data
            memfd_needed = any(
                v.get("type") == "ndarray" or v.get("type") == "str"
                for v in metadata.values()
            )

            if memfd_needed:
                # Receive memfd info
                memfd_info_size_bytes = conn.recv(4)
                if not memfd_info_size_bytes:
                    return

                memfd_info_size = int.from_bytes(
                    memfd_info_size_bytes, byteorder="little"
                )

                # Receive the file descriptor using SCM_RIGHTS
                from .memfd_mmap_transport import recv_fds

                memfd_info_bytes, fds = recv_fds(conn, memfd_info_size, 1)

                if not fds:
                    logger.error("No file descriptor received from client")
                    return

                # Get the received file descriptor
                received_fd = fds[0]

                # Parse the memfd info to get the size
                memfd_info = memfd_info_bytes.decode("utf-8").split(":")
                memfd_size = int(memfd_info[1])

                # Map the received memfd to memory
                mapped_memory = self.transport.map_memfd(received_fd, memfd_size)

                # Read data from mapped memory based on metadata
                inputs = self.transport.read_data_from_mapped_memory(
                    mapped_memory, metadata
                )

                # Close the mapped memory and the received fd
                mapped_memory.close()
                os.close(received_fd)

                request_fd_to_clean = None
            else:
                # All data was in metadata
                inputs = {
                    k: v["data"] for k, v in metadata.items() if v["type"] == "raw"
                }
                request_fd_to_clean = None

            # Call the policy function
            result = self.policy_func(inputs)

            # Prepare response - serialize result metadata
            response_metadata_bytes = self.transport.serialize_metadata(result)

            # Send response metadata size
            conn.send(len(response_metadata_bytes).to_bytes(4, byteorder="little"))
            # Send response metadata
            conn.send(response_metadata_bytes)

            # If there are arrays in the response, use memfd+mmap
            import numpy as np

            has_arrays = any(isinstance(v, np.ndarray) for v in result.values())

            if has_arrays:
                # Calculate total size needed for response
                total_response_size = sum(
                    v.nbytes if hasattr(v, "nbytes") else len(str(v).encode("utf-8"))
                    for v in result.values()
                    if hasattr(v, "nbytes") or isinstance(v, str)
                )

                if total_response_size > 0:
                    # Create memfd for response
                    response_fd = self.transport.create_memfd(total_response_size)

                    # Map the memfd to memory
                    response_mapped_memory = self.transport.map_memfd(
                        response_fd, total_response_size
                    )

                    # Write response data to mapped memory
                    response_metadata_with_offsets = self.transport.serialize_metadata(
                        result
                    )
                    response_metadata_parsed = self.transport.deserialize_metadata(
                        response_metadata_with_offsets
                    )
                    self.transport.write_data_to_mapped_memory(
                        response_mapped_memory, result, response_metadata_parsed
                    )

                    # Send memfd info (we'll send the fd number as identifier)
                    response_fd_info = f"{response_fd}:{total_response_size}"
                    conn.send(len(response_fd_info).to_bytes(4, byteorder="little"))

                    # Send the actual file descriptor using SCM_RIGHTS
                    from .memfd_mmap_transport import send_fds

                    send_fds(conn, response_fd_info.encode("utf-8"), [response_fd])

                    # Close the mapped memory handle but don't close fd yet
                    # Client will be responsible for cleaning up response memfd after reading
                    response_mapped_memory.close()

                    # Track this memfd for potential cleanup if client fails to clean up
                    self.response_memfds.add(response_fd)
                    response_fd_to_clean = response_fd
                else:
                    response_fd_to_clean = None
            else:
                # No memfd needed for response
                # Send empty memfd info to maintain protocol
                response_fd_info = "none:0"
                conn.send(len(response_fd_info).to_bytes(4, byteorder="little"))
                conn.send(response_fd_info.encode("utf-8"))

        except Exception as e:
            logger.error(f"Error handling client: {e}")
            logger.exception(e)
        finally:
            # Clean up request memfd that was used to receive data from client
            if request_fd_to_clean:
                try:
                    # Close the file descriptor
                    os.close(request_fd_to_clean)
                    # Remove from any tracking if needed
                except OSError:
                    # Already closed by client or another process
                    pass
                except Exception as e:
                    logger.warning(
                        f"Could not close request memfd {request_fd_to_clean}: {e}"
                    )

            # Client is responsible for cleaning up response memfd after reading.
            # Server keeps track of response memfds for backup cleanup if client fails to clean up later.
            conn.close()

    def _cleanup_memfd(self, fd):
        """Clean up memfd."""
        try:
            # Close the file descriptor
            os.close(fd)
        except OSError:
            # Already closed by another process or client
            pass
        except Exception:
            # Could not close for other reasons
            pass

    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()

        # Clean up any response memfds that weren't cleaned up by clients
        for fd in list(
            self.response_memfds
        ):  # Convert to list to avoid modification during iteration
            try:
                os.close(fd)
                self.response_memfds.discard(fd)
            except OSError:
                # Already closed
                self.response_memfds.discard(fd)
            except Exception as e:
                logger.warning(f"Could not close response memfd {fd}: {e}")
                # Still remove from tracking even if close failed
                self.response_memfds.discard(fd)

        # Perform comprehensive cleanup of any remaining memfds
        self.transport._cleanup_tracked_memfds()
        # Also run cleanup for old memfds that might have lingered
        self.transport._cleanup_old_memfds(
            max_age_seconds=10
        )  # Cleanup very old memfds
