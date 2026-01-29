import copy
import threading
import time
import numpy as np
import cv2
from typing import Any, cast

from loguru import logger

try:
    import pyrealsense2 as rs
except ImportError:
    print("Warning: pyrealsense2 not available. Camera functionality will be limited.")
    rs = None
# Help static analyzers: treat rs as dynamic Any when available
if rs is not None:
    rs = cast(Any, rs)


class CameraWrapper:
    def __init__(
        self,
        devices=None,
        width=640,
        height=480,
        fps=30,
        num_realsense=0,
        cv_format="MJPEG",
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.num_realsense = max(0, int(num_realsense))
        self.cv_format = cv_format
        self.cameras = []  # list of dicts: {type: 'rs'|'cv', handle: pipeline|cap}
        self.device_ids = devices if devices is not None else []
        self._open_cameras()
        print(f"successfully opened {len(self.cameras)} cameras!")

    def _open_cameras(self):
        if not self.device_ids:
            print("No devices provided for CameraWrapper")
            return

        for idx, dev in enumerate(self.device_ids):
            # Decide camera type
            use_realsense = idx < self.num_realsense

            if use_realsense:
                if rs is None:
                    print(
                        f"pyrealsense2 not available, skipping RealSense device at index {idx} (id: {dev})"
                    )
                    continue
                try:
                    serial = str(dev)
                    pipeline = rs.pipeline()  # type: ignore[attr-defined]
                    config = rs.config()  # type: ignore[attr-defined]
                    config.enable_device(serial)
                    config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)  # type: ignore[attr-defined]
                    pipeline.start(config)
                    self.cameras.append({"type": "rs", "handle": pipeline})
                    print(f"RealSense camera {serial} opened successfully")
                except Exception as e:
                    print(f"Failed to open RealSense camera {dev}: {e}")
            else:
                try:
                    device_index = int(dev)
                    print(f"Ready to read deive: {device_index}")
                    cap = cv2.VideoCapture(device_index)

                    if self.cv_format == "MJPEG":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # type: ignore[attr-defined]
                    elif self.cv_format == "YUYV":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))  # type: ignore[attr-defined]

                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    cap.set(cv2.CAP_PROP_FPS, self.fps)

                    if not cap.isOpened():
                        raise ValueError(f"Cannot open OpenCV camera {device_index}")

                    self.cameras.append({"type": "cv", "handle": cap})
                    print(f"OpenCV camera {device_index} opened successfully")
                except Exception as e:
                    print(f"Failed to open OpenCV camera {dev}: {e}")

    def get_images(self):
        images = []
        if len(self.cameras) == 0:
            logger.error("!! error: no cameras available, returning dummy images")
            # Return dummy images if no cameras available - use 640x480 which is expected by the model
            for _ in range(max(1, len(self.device_ids))):
                dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                dummy_img[:, :, :] = 128  # Gray color instead of black
                images.append(dummy_img)
            return images

        for cam in self.cameras:
            if cam["type"] == "rs":
                try:
                    pipeline = cam["handle"]
                    frames = pipeline.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    if not color_frame:
                        dummy_img = np.zeros(
                            (self.height, self.width, 3), dtype=np.uint8
                        )
                        dummy_img[:, :, :] = 128
                        images.append(dummy_img)
                    else:
                        img = np.asanyarray(color_frame.get_data())
                        images.append(img)
                except Exception as e:
                    print(f"Error reading from RealSense: {e}")
                    dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    dummy_img[:, :, :] = 128
                    images.append(dummy_img)
            elif cam["type"] == "cv":
                cap = cam["handle"]
                ret, frame = cap.read()
                if not ret or frame is None:
                    dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    dummy_img[:, :, :] = 128
                    images.append(dummy_img)
                else:
                    images.append(frame)
        return images

    def release(self):
        for cam in self.cameras:
            if cam["type"] == "rs":
                try:
                    cam["handle"].stop()
                except Exception:
                    pass
            elif cam["type"] == "cv":
                try:
                    cam["handle"].release()
                except Exception:
                    pass
        self.cameras = []


class AsyncCameraWrapper:
    def __init__(
        self,
        devices=None,
        width=640,
        height=480,
        fps=30,
        num_realsense=0,
        cv_format="MJPEG",
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.num_realsense = max(0, int(num_realsense))
        self.cv_format = cv_format
        self.device_ids = devices if devices is not None else []

        self.cameras = []  # 存放相机句柄

        # --- 异步核心变量 ---
        self.running = True
        self.lock = threading.Lock()
        # 初始化 buffer，避免主线程还没读到图就 crash
        # 列表索引对应 device_ids 的顺序
        self.latest_frames = [self._create_dummy_image() for _ in self.device_ids]
        self.threads = []

        self._open_cameras()
        self._start_threads()

        logger.info(
            f"Successfully opened {len(self.cameras)} cameras and started background threads!"
        )

    def _create_dummy_image(self):
        dummy = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        dummy[:, :, :] = 128  # 灰色背景
        return dummy

    def _open_cameras(self):
        if not self.device_ids:
            return

        for idx, dev in enumerate(self.device_ids):
            use_realsense = idx < self.num_realsense
            cam_info = {"type": "unknown", "handle": None, "id": idx}

            if use_realsense:
                if rs is None:
                    continue
                try:
                    serial = str(dev)
                    pipeline = rs.pipeline()
                    config = rs.config()
                    config.enable_device(serial)
                    config.enable_stream(
                        rs.stream.color,
                        self.width,
                        self.height,
                        rs.format.bgr8,
                        self.fps,
                    )
                    pipeline.start(config)
                    cam_info = {"type": "rs", "handle": pipeline, "id": idx}
                    logger.info(f"RealSense {serial} opened.")
                except Exception as e:
                    logger.error(f"Failed RealSense {dev}: {e}")
            else:
                try:
                    device_index = int(dev)
                    cap = cv2.VideoCapture(device_index)
                    if self.cv_format == "MJPEG":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
                    elif self.cv_format == "YUYV":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    cap.set(cv2.CAP_PROP_FPS, self.fps)

                    # 尝试设置 buffer 为 1，减少积压（即使有多线程，这也很有帮助）
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                    if not cap.isOpened():
                        raise ValueError(f"Cannot open OpenCV camera {device_index}")

                    cam_info = {"type": "cv", "handle": cap, "id": idx}
                    logger.info(f"OpenCV {device_index} opened.")
                except Exception as e:
                    logger.error(f"Failed OpenCV {dev}: {e}")

            self.cameras.append(cam_info)

    def _start_threads(self):
        """为每个相机启动一个独立的线程"""
        for cam_info in self.cameras:
            t = threading.Thread(target=self._worker, args=(cam_info,), daemon=True)
            t.start()
            self.threads.append(t)

    def _worker(self, cam_info):
        """后台工人：不断读取最新帧并覆盖缓存"""
        cam_type = cam_info["type"]
        handle = cam_info["handle"]
        idx = cam_info["id"]

        while self.running:
            img = None
            try:
                if cam_type == "rs":
                    # 这是一个阻塞调用，但因为它在独立线程里，所以无所谓
                    frames = handle.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    if color_frame:
                        img = np.asanyarray(color_frame.get_data())

                elif cam_type == "cv":
                    # 同样是阻塞调用
                    ret, frame = handle.read()
                    if ret and frame is not None:
                        img = frame

                # 只要读到了有效图片，立刻更新 buffer
                if img is not None:
                    # 这里的 Lock 极其重要，防止主线程读取时读到写了一半的数据（画面撕裂）
                    # 但 Python 的 GIL 和 numpy 赋值通常是原子的，为了保险起见加锁
                    # 实际上为了极致性能，甚至可以去掉锁（如果只做指针交换）
                    with self.lock:
                        self.latest_frames[idx] = img
                else:
                    # 如果读不到，稍微 sleep 一下防止 CPU 空转死循环
                    time.sleep(0.005)

            except Exception as e:
                # 捕获异常防止线程挂掉
                logger.warning(f"Camera {idx} error: {e}")
                time.sleep(0.1)

    def get_images(self):
        """【非阻塞】直接返回当前内存里最新的图"""
        with self.lock:
            # 深拷贝是必须的吗？
            # 1. 安全性：必须。否则你在处理 img 的时候，后台线程把 img 内容改了。
            # 2. 性能：copy 640x480 的图很快 (<1ms)。
            current_images = copy.deepcopy(self.latest_frames)
        return current_images

    def release(self):
        self.running = False  # 通知线程停止
        # 等待线程结束
        for t in self.threads:
            t.join(timeout=1.0)

        for cam in self.cameras:
            if cam["type"] == "rs":
                try:
                    cam["handle"].stop()
                except:
                    pass
            elif cam["type"] == "cv":
                try:
                    cam["handle"].release()
                except:
                    pass
        logger.info("Cameras released.")
