from dataclasses import dataclass
from numpy.typing import NDArray

import pytelicam as teli
from pytelicam import (
    CameraDevice,
    CameraInfo,
    SignalHandle,
    CamApiStatus,
    CameraPixelFormat,
    OutputImageType
    )

from telivision.telienums import VerbosityLevel


@dataclass
class TeliCameraSettings:
    exposure_time: float = 8500  # in µs
    gain: float = 0
    frame_rate: float = 60
    trigger_mode: bool = False


@dataclass
class TeliInfo:
    interface_type: str
    vendor: str
    model: str
    serial_number: str
    version: str
    user_defined_name: str
    display_name: str
    tl_vendor: str  # Transport layer vendor
    tl_model: str  # Transport layer model
    tl_version: str  # Transport layer version
    tl_display_name: str  # Transport layer display name
    tl_if_display_name: str  # Transport layer interface display name

    def __repr__(self):
        info = (
            f"Interface Type: {self.interface_type}\n"
            f"Vendor: {self.vendor}\n"
            f"Model: {self.model}\n"
            f"Serial Number: {self.serial_number}\n"
            f"Version: {self.version}\n"
            f"User Defined Name: {self.user_defined_name}\n"
            f"Display Name: {self.display_name}\n"
        )
        return info

    @staticmethod
    def from_camera_info(cam_info: CameraInfo):
        return TeliInfo(
            interface_type=cam_info.cam_type,
            vendor=cam_info.cam_vendor,
            model=cam_info.cam_model,
            serial_number=cam_info.cam_serial_number,
            version=cam_info.cam_version,
            user_defined_name=cam_info.cam_user_defined_name,
            display_name=cam_info.cam_display_name,
            tl_vendor=cam_info.tl_vendor,
            tl_model=cam_info.tl_model,
            tl_version=cam_info.tl_version,
            tl_display_name=cam_info.tl_display_name,
            tl_if_display_name=cam_info.tl_if_display_name
        )


class TeliCamera:
    def __init__(
            self,
            cam_system,
            index,
            cam_device: CameraDevice,
            trigger_signal: SignalHandle | None = None,
            verbosity=VerbosityLevel.NONE):
        self.verbosity = verbosity
        self.cam_system = cam_system

        self.index = index
        self.cam_device = cam_device
        self.cam_device.open()

        self.cam_control = self.cam_device.cam_control
        self.info = TeliInfo.from_camera_info(self.cam_device.get_information())

        self.trigger_signal = trigger_signal
        self.event = self.cam_device.cam_event

        self._init_stream(cam_device)

        self.cam_control = self.cam_device.cam_control

    def _init_stream(self, cam_device: CameraDevice):
        self.stream = cam_device.cam_stream
        self.stream_running = False
        print(self.stream.is_open)

        # Set trigger mode
        if self.trigger_signal is not None:
            response = self.cam_control.set_trigger_mode(True)
            if response != CamApiStatus.Success:
                raise Exception(f"Failed to enable trigger mode on camera {self.index}. Status: {response}")

            response = self.cam_control.set_trigger_source(teli.pytelicam.CameraTriggerSource.Software)
            if response != CamApiStatus.Success:
                raise Exception(f"Failed to set trigger source on camera {self.index}. Status: {response}")

            self.cam_control.set_trigger_sequence(teli.pytelicam.CameraTriggerSequence.Sequence0)

            if self.verbosity >= VerbosityLevel.LOW:
                print(f"Trigger mode enabled for camera {self.index}.")
        else:
            response = self.cam_control.set_trigger_mode(False)
            if response != CamApiStatus.Success:
                raise Exception(f"Failed to disable trigger mode on camera {self.index}. Status: {response}")

        self.stream.open(self.trigger_signal)

    def apply_settings(self, settings: TeliCameraSettings):
        self.cam_device.cam_control.set_exposure_time(settings.exposure_time)
        self.cam_device.cam_control.set_gain(settings.gain)
        self.cam_device.cam_control.set_frame_rate(settings.frame_rate)
        self.cam_device.cam_control.enable_trigger_mode(settings.trigger_mode)

    def start_stream(self):
        if self.stream.is_open:
            if not self.stream_running:
                self.stream.start()
                self.stream_running = True
                if self.verbosity >= VerbosityLevel.LOW:
                    print(f"Stream for camera {self.index} started.")
            elif self.verbosity >= VerbosityLevel.LOW:
                print(f"Stream for camera {self.index} is already running.")
        elif self.verbosity >= VerbosityLevel.LOW:
            print(f"Cannot start stream. Stream resource for camera {self.index} is not open.")

    def stop_stream(self):
        if self.stream.is_open:
            if self.stream_running:
                self.stream.stop()
                self.stream_running = False
                if self.verbosity >= VerbosityLevel.LOW:
                    print(f"Stream for camera {self.index} closed.")
            elif self.verbosity >= VerbosityLevel.LOW:
                print(f"Stream for camera {self.index} is not running.")
        elif self.verbosity >= VerbosityLevel.LOW:
            print(f"Cannot stop stream. Stream resource for camera {self.index} is not open.")

    def trigger_capture(self) -> NDArray:
        assert self.stream.is_open, "Stream must be open to trigger capture."

        response = self.cam_device.genapi.execute_command('TriggerSoftware')
        if response != CamApiStatus.Success:
            raise Exception(f"Failed to trigger capture on camera {self.index}. Status: {response}")

        response = self.cam_system.wait_for_signal(self.trigger_signal)
        if response != CamApiStatus.Success:
            raise Exception(f"Failed to wait for trigger signal on camera {self.index}. Status: {response}")

        current_index = self.stream.get_current_buffer_index()
        with self.stream.get_buffered_image(current_index) as image_data:
            if image_data.status != CamApiStatus.Success:
                raise Exception(f"Failed to get buffered image on camera {self.index}. Status: {image_data.status}")
            if image_data.pixel_format == CameraPixelFormat.Mono8:
                if self.verbosity >= VerbosityLevel.LOW:
                    print(f"Captured Mono8 image from camera {self.index}.")
                np_image = image_data.get_ndarray(OutputImageType.Raw)
            else:
                if self.verbosity >= VerbosityLevel.LOW:
                    print(f"Captured Bgr24 image from camera {self.index}.")
                np_image = image_data.get_ndarray(OutputImageType.Bgr24)

            return np_image

    def __enter__(self):
        self.start_stream()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_stream()
        self.cam_device.close()

    def __del__(self):
        self.stop_stream()
        self.cam_device.close()


class TeliWrapper:
    def __init__(self, verbosity=VerbosityLevel.NONE):
        self.verbosity = verbosity
        self.cam_system = teli.get_camera_system()
        print("Telicam system initialized."
              f" Number of cameras detected: {self.cam_system.get_num_of_cameras()}")

    def create_camera(self, cam_index=0):
        camera = self.cam_system.create_device_object(cam_index)
        trigger_signal = self.cam_system.create_signal()
        telicamera = TeliCamera(
            self.cam_system,
            cam_index, camera,
            trigger_signal=trigger_signal,
            verbosity=self.verbosity
            )
        return telicamera


if __name__ == "__main__":
    import cv2
    wrap = TeliWrapper()
    cam = wrap.create_camera(0)
    cam.start_stream()
    while True:
        image = cam.trigger_capture()
        cv2.imshow("Teli Camera", image)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            cv2.destroyAllWindows()
            break
    cam.stop_stream()
