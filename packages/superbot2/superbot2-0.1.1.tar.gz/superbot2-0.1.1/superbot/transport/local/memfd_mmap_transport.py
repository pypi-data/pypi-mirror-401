"""
Socket and MemFD + MMAP utilities for zero-copy transport
"""

import os
import mmap
import struct
import socket
import tempfile
import atexit
import signal
import threading
import time
import ctypes
import ctypes.util
from ctypes import c_int, c_char_p, c_size_t, c_uint
import uuid
from loguru import logger
import array


# Load libc for memfd_create
libc = ctypes.CDLL(ctypes.util.find_library("c"))

# Define memfd_create function
memfd_create = libc.memfd_create
memfd_create.argtypes = [c_char_p, c_uint]
memfd_create.restype = c_int


def send_fds(sock, msg, fds):
    """
    Send a message along with file descriptors over a Unix socket.
    """
    # Create SCM_RIGHTS message
    fds_bytes = array.array('i', fds).tobytes()
    
    # Create control message
    ctrl_msg = [
        (socket.SOL_SOCKET, socket.SCM_RIGHTS, fds_bytes)
    ]
    
    # Send message with file descriptors
    return sock.sendmsg([msg], ctrl_msg)


def recv_fds(sock, msglen, maxfds):
    """
    Receive a message along with file descriptors from a Unix socket.
    """
    msg, ancdata, flags, addr = sock.recvmsg(msglen, socket.CMSG_SPACE(maxfds * 4))
    
    fds = []
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            fds.extend(array.array('i', cmsg_data).tolist())
    
    return msg, fds


class MemfdMmapTransport:
    """
    A transport layer using Unix Domain Sockets for control and MemFD + MMAP for data.
    """

    # Class-level tracker for memfd objects to prevent leaks
    _tracked_memfds = {}

    def __init__(self):
        self.socket_path = None
        self.mapped_memory = None
        # Register cleanup function to run at exit
        atexit.register(self._cleanup_tracked_memfds)

        # Only register signal handlers in the main thread
        if threading.current_thread() is threading.main_thread():
            try:
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
            except ValueError:
                # Signal handling not available in this context (e.g., non-main thread)
                pass

    @classmethod
    def track_memfd(cls, fd, size):
        """Track a memfd object for cleanup with timestamp."""
        import time

        cls._tracked_memfds[fd] = {
            'size': size,
            'creation_time': time.time(),
            'mapped_memory': None  # Will store the mmap object if mapped
        }

    @classmethod
    def untrack_memfd(cls, fd):
        """Remove a memfd object from tracking."""
        if fd in cls._tracked_memfds:
            # If there's a mapped memory associated, close it first
            entry = cls._tracked_memfds[fd]
            if entry['mapped_memory']:
                try:
                    entry['mapped_memory'].close()
                except:
                    pass
            del cls._tracked_memfds[fd]

    @classmethod
    def _cleanup_tracked_memfds(cls):
        """Clean up all tracked memfd objects."""
        import time

        # Make a copy of the keys to iterate over
        fds_to_cleanup = list(cls._tracked_memfds.keys())

        for fd in fds_to_cleanup:
            try:
                # Close the mapped memory if it exists
                entry = cls._tracked_memfds[fd]
                if entry['mapped_memory']:
                    try:
                        entry['mapped_memory'].close()
                    except:
                        pass

                # Close the file descriptor
                os.close(fd)
                # Remove from tracking
                cls._tracked_memfds.pop(fd, None)
            except OSError:
                # Already closed by another process or client
                cls._tracked_memfds.pop(fd, None)
            except Exception:
                # Could not close, might be accessed by another process
                # Still remove from tracking
                cls._tracked_memfds.pop(fd, None)

    @classmethod
    def _cleanup_old_memfds(cls, max_age_seconds=300):  # 5 minutes default
        """Clean up memfd objects that have been tracked for too long."""
        import time

        current_time = time.time()
        for fd, info in list(cls._tracked_memfds.items()):
            if current_time - info['creation_time'] > max_age_seconds:
                try:
                    # Close the mapped memory if it exists
                    if info['mapped_memory']:
                        try:
                            info['mapped_memory'].close()
                        except:
                            pass

                    # Close the file descriptor
                    os.close(fd)
                    cls._tracked_memfds.pop(fd, None)
                except OSError:
                    # Already closed
                    cls._tracked_memfds.pop(fd, None)
                except Exception:
                    # Could not close, might be accessed by another process
                    # Still remove from tracking
                    cls._tracked_memfds.pop(fd, None)

    @classmethod
    def _signal_handler(cls, signum, frame):
        """Handle signals to ensure cleanup."""
        cls._cleanup_tracked_memfds()
        # Re-raise the signal to allow normal termination
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    def create_socket(self, socket_path):
        """Create a Unix domain socket for control messages."""
        if os.path.exists(socket_path):
            os.unlink(socket_path)

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(socket_path)
        os.chmod(socket_path, 0o777)  # Make accessible
        return sock

    def connect_socket(self, socket_path):
        """Connect to a Unix domain socket."""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(socket_path)
        return sock

    def create_memfd(self, size, name=None):
        """Create a memfd and resize it to the specified size."""
        if name is None:
            name = f"zerorpc_{uuid.uuid4().hex[:8]}".encode('utf-8')
        else:
            name = name.encode('utf-8') if isinstance(name, str) else name
            
        # Create memfd
        fd = memfd_create(name, 0)
        if fd == -1:
            raise OSError("Failed to create memfd")
        
        # Resize the memfd to the desired size
        os.ftruncate(fd, size)
        
        # Track this memfd for cleanup
        self.track_memfd(fd, size)
        
        return fd

    def map_memfd(self, fd, size, access=mmap.ACCESS_WRITE):
        """Map a memfd to memory."""
        mapped_memory = mmap.mmap(fd, size, access=access)
        
        # Update tracking info with the mapped memory
        if fd in self._tracked_memfds:
            self._tracked_memfds[fd]['mapped_memory'] = mapped_memory
        
        return mapped_memory

    def serialize_metadata(self, data_dict):
        """Serialize metadata about the data to be sent over the socket."""
        import json
        import numpy as np

        assert isinstance(
            data_dict, dict
        ), f"Expected dict, got {type(data_dict)}, policy return must be a dict contains any types."

        metadata = {}
        offset = 0

        for key, value in data_dict.items():
            if isinstance(value, np.ndarray):
                metadata[key] = {
                    "type": "ndarray",
                    "shape": value.shape,
                    "dtype": str(value.dtype),
                    "offset": offset,
                    "size": value.nbytes,
                }
                offset += value.nbytes
            elif isinstance(value, str):
                metadata[key] = {
                    "type": "str",
                    "data": value,
                    "offset": offset,
                    "size": len(value.encode("utf-8")),
                }
                offset += len(value.encode("utf-8"))
            else:
                # For other types, store directly in metadata
                metadata[key] = {"type": "raw", "data": value}

        return json.dumps(metadata).encode("utf-8")

    def deserialize_metadata(self, metadata_bytes):
        """Deserialize metadata received over the socket."""
        import json

        return json.loads(metadata_bytes.decode("utf-8"))

    def write_data_to_mapped_memory(self, mapped_memory, data_dict, metadata):
        """Write data to mapped memory according to metadata layout."""
        import numpy as np

        offset = 0
        for key, info in metadata.items():
            if info["type"] == "ndarray":
                value = data_dict[key]
                data_bytes = value.tobytes()
                mapped_memory[offset : offset + len(data_bytes)] = data_bytes
                offset += len(data_bytes)
            elif info["type"] == "str":
                value = data_dict[key].encode("utf-8")
                mapped_memory[offset : offset + len(value)] = value
                offset += len(value)

    def read_data_from_mapped_memory(self, mapped_memory, metadata):
        """Read data from mapped memory according to metadata layout."""
        import numpy as np

        result = {}
        offset = 0

        for key, info in metadata.items():
            if info["type"] == "ndarray":
                shape = tuple(info["shape"])
                dtype = info["dtype"]
                size = info["size"]

                # Extract bytes from mapped memory
                data_bytes = bytes(mapped_memory[offset : offset + size])
                # Reconstruct numpy array
                arr = np.frombuffer(data_bytes, dtype=dtype).reshape(shape)
                result[key] = arr.copy()  # Copy to avoid holding onto mapped memory

                offset += size
            elif info["type"] == "str":
                size = info["size"]
                data_bytes = bytes(mapped_memory[offset : offset + size])
                result[key] = data_bytes.decode("utf-8")
                offset += size
            elif info["type"] == "raw":
                result[key] = info["data"]

        return result