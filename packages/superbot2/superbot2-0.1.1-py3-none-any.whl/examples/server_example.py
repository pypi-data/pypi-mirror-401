"""
Example server implementation using the unified VLA transport library
Supports both local and remote modes based on parameters
"""

import numpy as np
from loguru import logger
from superbot.transport import PolicyServer


class VLAPolicy:

    def __init__(self):
        pass

    def forward(self, inputs):
        # print(inputs)
        for k, v in inputs.items():
            if isinstance(v, np.ndarray):
                logger.info(f"{k}: {v.shape}")
            else:
                logger.info(f"{k}: {v}")
        # chunksize 50 with 20 dimensions
        return {"action": np.random.random([50, 20])}


def run_local_server():
    """Run server in local mode using socket"""
    logger.info("Starting local policy server example...")

    vla_policy = VLAPolicy()

    def policy_wrapper(inputs):
        return vla_policy.forward(inputs)

    # Create sample inputs for warmup
    warmup_inputs = {
        "image0": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image1": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image2": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "lang": "move towards the blue object",
        "state": np.random.random((64,)).astype(np.float32),
    }

    # Using local mode with socket_name (the unified server automatically detects this)
    server = PolicyServer(
        policy_wrapper, socket_name="xvla_policy", warmup_inputs=warmup_inputs
    )

    logger.info("Local policy server initialized, starting to serve...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Local server interrupted, shutting down...")


def run_remote_server():
    """Run server in remote mode using URL"""
    logger.info("Starting remote policy server example...")

    vla_policy = VLAPolicy()

    def policy_wrapper(inputs):
        return vla_policy.forward(inputs)

    # Create sample inputs for warmup
    warmup_inputs = {
        "image0": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image1": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "image2": np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8),
        "lang": "move towards the blue object",
        "state": np.random.random((64,)).astype(np.float32),
    }

    # Using remote mode with URL (the unified server automatically detects this)
    server = PolicyServer(
        policy_wrapper, url="tcp://*:5555", warmup_inputs=warmup_inputs
    )

    logger.info("Remote policy server initialized, starting to serve...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Remote server interrupted, shutting down...")


if __name__ == "__main__":
    # You can choose to run either local or remote server
    # run_local_server()  # For local mode using Unix domain socket
    run_remote_server()   # For remote mode using TCP
