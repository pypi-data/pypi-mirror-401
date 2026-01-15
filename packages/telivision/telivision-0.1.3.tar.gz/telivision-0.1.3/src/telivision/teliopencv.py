from telivision.teliwrap import TeliWrapper, TeliCamera
from telivision.telienums import VerbosityLevel, CaptureMode

import cv2
from tkinter import filedialog
import tkinter as tk
import traceback


class TeliOpenCV:
    def __init__(self, cam_index=0, verbosity=VerbosityLevel.NONE):
        self.verbosity = verbosity
        print(verbosity)
        self.teli_wrapper = TeliWrapper(verbosity=self.verbosity)
        self.camera: TeliCamera = self.teli_wrapper.create_camera(cam_index=cam_index)

    def handle_input(self, key):
        if key == 'q' or key == 27:  # 'q' or ESC key
            print("Exiting display loop.")
            self.capture_mode = CaptureMode.END
        if key == ord('s'):
            # Create a hidden root window for the file dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            # Open file save dialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save Image As"
            )

            # Save if user didn't cancel
            if filepath:
                cv2.imwrite(filepath, self.image_data)
                print(f"Image saved to '{filepath}'.")
            elif self.verbosity >= VerbosityLevel.LOW:
                print("Save cancelled.")

            root.destroy()  # Clean up the root window

        if key == ord(' '):
            if self.capture_mode == CaptureMode.CONTINUOUS:
                self.capture_mode = CaptureMode.MANUAL
            elif self.capture_mode == CaptureMode.MANUAL:
                self.capture_mode = CaptureMode.CONTINUOUS

            if self.capture_mode == CaptureMode.CONTINUOUS:
                print("Resuming display loop.")
            elif self.capture_mode == CaptureMode.MANUAL:
                print("Pausing display loop.")

        if key == ord('r'):
            # Manual trigger
            self.triggered = True

    def display_loop(self):
        # Start in continuous mode
        self.capture_mode = CaptureMode.CONTINUOUS
        self.triggered = True

        # Start camera stream
        with self.camera as cam:
            while self.capture_mode != CaptureMode.END:
                if self.capture_mode == CaptureMode.CONTINUOUS or self.triggered:
                    self.triggered = False
                    self.image_data = cam.trigger_capture()
                    xy_ratio = self.image_data.shape[1] / self.image_data.shape[0]

                    # Resize to reasonable display size
                    show_image = cv2.resize(self.image_data, dsize=(int(1080 * xy_ratio), 1080))
                    cv2.imshow('image', show_image)

                user_input = cv2.waitKey(5) & 0xFF
                self.handle_input(user_input)


def teli_opencv_main():
    try:
        teli_opencv = TeliOpenCV(cam_index=0, verbosity=VerbosityLevel.NONE)
        teli_opencv.display_loop()

    except Exception as exception:
        traceback.print_exc()
        print(exception)

    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    teli_opencv_main()
