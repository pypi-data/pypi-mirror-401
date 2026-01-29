"""
Example client implementation using the unified VLA transport library
Supports both local and remote modes based on parameters
"""

import numpy as np
from loguru import logger
from superbot.transport import PolicyClient
import time


def run_local_requests():
    """Test local mode using socket"""
    logger.info("Testing local requests...")

    # Using local mode with socket_name
    client = PolicyClient(socket_name="xvla_policy")

    # Create dummy observation data
    obs = {
        "image0": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image1": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image2": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "lang": "move towards the blue object",
        "state": np.random.random((64,)).astype(np.float32),
    }

    times = []
    for i in range(3):
        logger.info(f"Local request {i+1}/3")
        start_time = time.time()

        try:
            result = client.call(obs)
            end_time = time.time()

            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            times.append(elapsed_time)

            print(f"Local vla result: {result['action'].shape}")

            logger.success(f"Local request {i+1} took {elapsed_time:.2f}ms")
        except Exception as e:
            logger.error(f"Error in local request {i+1}: {e}")

    if times:
        avg_time = sum(times) / len(times)
        logger.info(f"Average local response time: {avg_time:.2f}ms")


def run_remote_requests():
    """Test remote mode using URL"""
    logger.info("Testing remote requests...")

    # Using remote mode with URL
    client = PolicyClient(url="tcp://localhost:5555")

    # Create dummy observation data
    obs = {
        "image0": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image1": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image2": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "lang": "move towards the blue object",
        "state": np.random.random((64,)).astype(np.float32),
    }

    times = []
    for i in range(3):
        logger.info(f"Remote request {i+1}/3")
        start_time = time.time()

        try:
            result = client.call(obs)
            end_time = time.time()

            elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
            times.append(elapsed_time)

            print(f"Remote vla result: {result['action'].shape}")

            logger.success(f"Remote request {i+1} took {elapsed_time:.2f}ms")
        except Exception as e:
            logger.error(f"Error in remote request {i+1}: {e}")

    if times:
        avg_time = sum(times) / len(times)
        logger.info(f"Average remote response time: {avg_time:.2f}ms")


if __name__ == "__main__":
    # Test local mode
    # run_local_requests()

    # Test remote mode
    run_remote_requests()
