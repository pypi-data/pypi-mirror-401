import copy
import threading
import time
import numpy as np
import cv2
from typing import Any, cast

from loguru import logger

# --- Orbbec SDK Import ---
try:
    from pyorbbecsdk import *
    import pyorbbecsdk as orb
except ImportError:
    print("Warning: pyorbbecsdk not available. Orbbec functionality will be disabled.")
    orb = None

# --- RealSense SDK Import ---
try:
    import pyrealsense2 as rs
except ImportError:
    print(
        "Warning: pyrealsense2 not available. RealSense functionality will be disabled."
    )
    rs = None
if rs is not None:
    rs = cast(Any, rs)

from superbot.sensors.cams.utils import frame_to_bgr_image


class CameraWrapper:
    def __init__(
        self,
        devices=None,
        width=640,
        height=480,
        fps=30,
        num_realsense=0,
        num_orbbec=0,  # [新增] 奥比中光相机数量
        cv_format="MJPEG",
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.num_realsense = max(0, int(num_realsense))
        self.num_orbbec = max(0, int(num_orbbec))  # [新增]
        self.cv_format = cv_format
        self.cameras = []  # list of dicts: {type: 'rs'|'orb'|'cv', handle: ...}
        self.device_ids = devices if devices is not None else []

        # Orbbec 上下文，只需初始化一次
        self.orb_context = None
        if self.num_orbbec > 0 and orb is not None:
            self.orb_context = Context()

        self._open_cameras()
        print(f"successfully opened {len(self.cameras)} cameras!")

    def _find_orbbec_device(self, sn):
        """[新增] 根据序列号查找奥比中光设备对象"""
        if self.orb_context is None:
            return None
        device_list = self.orb_context.query_devices()
        for i in range(device_list.get_count()):
            device = device_list.get_device_by_index(i)
            try:
                # 获取设备序列号
                curr_sn = device.get_device_info().get_serial_number()
                if str(curr_sn) == str(sn):
                    return device
            except OBError:
                continue
        return None

    def _open_cameras(self):
        if not self.device_ids:
            print("No devices provided for CameraWrapper")
            return

        for idx, dev in enumerate(self.device_ids):
            # 逻辑：前 N 个是 RS，中间 M 个是 Orbbec，剩下是 CV
            is_realsense = idx < self.num_realsense
            is_orbbec = (not is_realsense) and (
                idx < self.num_realsense + self.num_orbbec
            )

            # --- 1. RealSense ---
            if is_realsense:
                if rs is None:
                    print(f"pyrealsense2 missing, skipping index {idx}")
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
                    self.cameras.append({"type": "rs", "handle": pipeline})
                    print(f"RealSense camera {serial} opened successfully")
                except Exception as e:
                    print(f"Failed to open RealSense camera {dev}: {e}")

            # --- 2. Orbbec [新增] ---
            elif is_orbbec:
                if orb is None:
                    print(f"pyorbbecsdk missing, skipping index {idx}")
                    continue
                try:
                    serial = str(dev)
                    device = self._find_orbbec_device(serial)
                    if device is None:
                        print(
                            f"Orbbec device with SN {serial} not found in connection list."
                        )
                        continue

                    pipeline = Pipeline(device)
                    config = Config()
                    try:
                        profile_list = pipeline.get_stream_profile_list(
                            OBSensorType.COLOR_SENSOR
                        )
                        # 尝试匹配指定的宽高帧率，格式默认 RGB
                        color_profile = profile_list.get_video_stream_profile(
                            self.width, self.height, OBFormat.RGB, self.fps
                        )
                    except OBError:
                        print(
                            f"Orbbec: {serial} does not support {self.width}x{self.height}@{self.fps}, using default."
                        )
                        color_profile = profile_list.get_default_video_stream_profile()

                    config.enable_stream(color_profile)
                    pipeline.start(config)
                    self.cameras.append({"type": "orb", "handle": pipeline})
                    print(f"Orbbec camera {serial} opened successfully")
                except Exception as e:
                    print(f"Failed to open Orbbec camera {dev}: {e}")

            # --- 3. OpenCV ---
            else:
                try:
                    device_index = int(dev)
                    print(f"Ready to read device: {device_index}")
                    cap = cv2.VideoCapture(device_index)

                    if self.cv_format == "MJPEG":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
                    elif self.cv_format == "YUYV":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))

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
            print("error: no cameras available, returning dummy images")
            for _ in range(max(1, len(self.device_ids))):
                dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                dummy_img[:, :, :] = 128
                images.append(dummy_img)
            return images

        for cam in self.cameras:
            # --- RealSense ---
            if cam["type"] == "rs":
                try:
                    pipeline = cam["handle"]
                    frames = pipeline.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    if not color_frame:
                        raise ValueError("Empty frame")
                    img = np.asanyarray(color_frame.get_data())
                    images.append(img)
                except Exception as e:
                    # print(f"Error reading from RealSense: {e}")
                    dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    dummy_img[:, :, :] = 128
                    images.append(dummy_img)

            elif cam["type"] == "orb":
                try:
                    pipeline = cam["handle"]

                    frames = pipeline.wait_for_frames(100)
                    if frames is None:
                        raise ValueError("Wait frame timeout")
                    color_frame = frames.get_color_frame()
                    if color_frame is None:
                        raise ValueError("No color frame")

                    # 转换数据 (RGB -> BGR for OpenCV compatibility)
                    # 原始数据通常是 bytes，需要转换
                    width = color_frame.get_width()
                    height = color_frame.get_height()
                    raw_data = color_frame.get_data()
                    data = np.frombuffer(raw_data, dtype=np.uint8)
                    data = data.reshape((height, width, 3))

                    # Orbbec 默认出来是 RGB，转 BGR
                    img = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
                    images.append(img)
                except Exception as e:
                    # print(f"Error reading from Orbbec: {e}")
                    dummy_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                    dummy_img[:, :, :] = 128
                    images.append(dummy_img)

            # --- OpenCV ---
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
                except:
                    pass
            elif cam["type"] == "orb":  # [新增]
                try:
                    cam["handle"].stop()
                except:
                    pass
            elif cam["type"] == "cv":
                try:
                    cam["handle"].release()
                except:
                    pass
        self.cameras = []


class AsyncCameraWrapper:
    def __init__(
        self,
        devices=None,
        sizes=[],
        fps=30,
        num_realsense=0,
        num_orbbec=0,
        cv_format="MJPEG",
    ):
        self.sizes = sizes
        self.fps = fps
        self.num_realsense = max(0, int(num_realsense))
        self.num_orbbec = max(0, int(num_orbbec))
        self.cv_format = cv_format
        self.device_ids = devices if devices is not None else []
        self.width = 640
        self.height = 480
        self.cameras = []
        # Orbbec Context
        self.orb_context = None
        if self.num_orbbec > 0 and orb is not None:
            self.orb_context = Context()

        self.running = True
        self.lock = threading.Lock()
        self.latest_frames = [
            self._create_dummy_image(idx) for idx, _ in enumerate(self.device_ids)
        ]
        self.threads = []

        self._open_cameras()
        self._start_threads()

        logger.info(f"Successfully opened {len(self.cameras)} cameras (Async)!")

    def _create_dummy_image(self, idx):
        dummy = np.zeros((self.sizes[idx][1], self.sizes[idx][0], 3), dtype=np.uint8)
        dummy[:, :, :] = 128
        return dummy

    def _find_orbbec_device(self, sn):
        """[新增] Helper to find Orbbec device by SN"""
        if self.orb_context is None:
            return None
        device_list = self.orb_context.query_devices()
        for i in range(device_list.get_count()):
            device = device_list.get_device_by_index(i)
            try:
                curr_sn = device.get_device_info().get_serial_number()
                if str(curr_sn) == str(sn):
                    return device
            except OBError:
                continue
        return None

    def _open_cameras(self):
        if not self.device_ids:
            return

        for idx, dev in enumerate(self.device_ids):
            # 区分三种类型
            is_orbbec = idx < self.num_orbbec
            is_realsense = (not is_orbbec) and (
                idx < self.num_realsense + self.num_orbbec
            )

            cam_info = {"type": "unknown", "handle": None, "id": idx}

            # --- 1. RealSense ---
            if is_realsense:
                if rs is None:
                    continue
                try:
                    serial = str(dev)
                    pipeline = rs.pipeline()
                    config = rs.config()
                    config.enable_device(serial)
                    print(self.sizes[idx])
                    config.enable_stream(
                        rs.stream.color,
                        self.sizes[idx][0],
                        self.sizes[idx][1],
                        rs.format.bgr8,
                        self.fps,
                    )
                    pipeline.start(config)
                    cam_info = {"type": "rs", "handle": pipeline, "id": idx}
                    logger.info(f"RealSense {serial} opened.")
                except Exception as e:
                    logger.error(f"Failed RealSense {dev}: {e}")

            elif is_orbbec:
                if orb is None:
                    continue
                try:
                    serial = str(dev)
                    device = self._find_orbbec_device(serial)
                    if device:
                        pipeline = Pipeline(device)
                        config = Config()
                        try:
                            profile_list = pipeline.get_stream_profile_list(
                                OBSensorType.COLOR_SENSOR
                            )
                            color_profile = profile_list.get_video_stream_profile(
                                self.sizes[idx][0],
                                self.sizes[idx][1],
                                OBFormat.RGB,
                                self.fps,
                            )
                        except OBError:
                            color_profile = (
                                profile_list.get_default_video_stream_profile()
                            )

                        config.enable_stream(color_profile)
                        pipeline.start(config)
                        cam_info = {"type": "orb", "handle": pipeline, "id": idx}
                        logger.info(f"Orbbec {serial} opened.")
                    else:
                        logger.error(f"Orbbec {serial} not found.")
                except Exception as e:
                    logger.error(f"Failed Orbbec {dev}: {e}")

            else:
                try:
                    device_index = int(dev)
                    cap = cv2.VideoCapture(device_index)
                    if self.cv_format == "MJPEG":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
                    elif self.cv_format == "YUYV":
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.sizes[idx][0])
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.sizes[idx][1])
                    cap.set(cv2.CAP_PROP_FPS, self.fps)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                    if not cap.isOpened():
                        raise ValueError(f"Cannot open OpenCV camera {device_index}")

                    cam_info = {"type": "cv", "handle": cap, "id": idx}
                    logger.info(f"OpenCV {device_index} opened.")
                except Exception as e:
                    logger.error(f"Failed OpenCV {dev}: {e}")

            self.cameras.append(cam_info)

    def _start_threads(self):
        for cam_info in self.cameras:
            t = threading.Thread(target=self._worker, args=(cam_info,), daemon=True)
            t.start()
            self.threads.append(t)

    def _worker(self, cam_info):
        cam_type = cam_info["type"]
        handle = cam_info["handle"]
        idx = cam_info["id"]

        while self.running:
            img = None
            try:
                # --- RealSense ---
                if cam_type == "rs":
                    frames = handle.wait_for_frames()
                    color_frame = frames.get_color_frame()
                    if color_frame:
                        img = np.asanyarray(color_frame.get_data())

                elif cam_type == "orb":
                    frames = handle.wait_for_frames(100)
                    if frames:
                        color_frame = frames.get_color_frame()
                        if color_frame:
                            w = color_frame.get_width()
                            h = color_frame.get_height()
                            raw = color_frame.get_data()
                            data = np.frombuffer(raw, dtype=np.uint8).reshape((h, w, 3))
                            img = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)

                # --- OpenCV ---
                elif cam_type == "cv":

                    ret, frame = handle.read()
                    if ret and frame is not None:
                        img = frame

                if img is not None:

                    # if img.shape[0] != self.height or img.shape[1] != self.width:
                    #     img = cv2.resize(img, (self.width, self.height))

                    with self.lock:
                        self.latest_frames[idx] = img
                else:
                    time.sleep(0.005)

            except Exception as e:
                # logger.warning(f"Camera {idx} error: {e}")
                time.sleep(0.1)

    def get_images(self):
        with self.lock:
            current_images = copy.deepcopy(self.latest_frames)
        return current_images

    def release(self):
        self.running = False
        for t in self.threads:
            t.join(timeout=1.0)

        for cam in self.cameras:
            if cam["type"] == "rs":
                try:
                    cam["handle"].stop()
                except:
                    pass
            elif cam["type"] == "orb":
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
