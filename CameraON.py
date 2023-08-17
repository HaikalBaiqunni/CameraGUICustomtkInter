import cv2
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class FocusSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Simulation App")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_frame = ctk.CTkFrame(root)
        self.button_frame.grid(row=0, column=1, padx=0, pady=10, sticky="ns")

        self.camera_label1 = ctk.CTkLabel(self.main_frame, text="")
        self.camera_label1.grid(row=0, column=0, padx=10, pady=10)

        self.camera_label2 = ctk.CTkLabel(self.main_frame, text="")
        self.camera_label2.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = ctk.CTkButton(self.button_frame, text="Start Webcam", command=self.start_webcam)
        self.load_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.focus_slider = ctk.CTkSlider(self.button_frame, width=150, height=20, from_=0, to=100, number_of_steps=None)
        self.focus_slider.grid(row=2, column=0, padx=15, pady=20, sticky="w")

        self.slider_value_label = ctk.CTkLabel(self.main_frame, text="Slider Value: 0.0")
        self.slider_value_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.is_binary = False
        self.current_camera_label = self.camera_label1

        self.video_capture = None

    def start_webcam(self):
        self.video_capture = cv2.VideoCapture(0)
        self.update_webcam()

    def update_webcam(self):
        ret, frame = self.video_capture.read()
        if ret:
            focus_value = self.focus_slider.get() / 100.0
            blurred_frame = self.apply_focus(frame, focus_value)
            img = Image.fromarray(blurred_frame)
            img = ImageTk.PhotoImage(image=img)
            self.current_camera_label.configure(image=img)
            self.current_camera_label.image = img
            self.root.after(10, self.update_webcam)

    def apply_focus(self, image, focus_value):
        kernel_size = int(15 * focus_value) // 2 * 2 + 1  # Ensure it's an odd value
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        return blurred_image

if __name__ == "__main__":
    root = ctk.CTk()
    app = FocusSimulationApp(root)
    root.mainloop()
