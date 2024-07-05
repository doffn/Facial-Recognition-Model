# Import kivy dependencies first
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.logger import Logger
from kivy.graphics.texture import Texture
from kivy.clock import Clock

# Import other dependencies
import cv2
import pandas as pd
from deepface import DeepFace
from PIL import Image as PILImage
import numpy as np
import os
import time

# This are list of models that we can select for the models
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet",
]

class CamApp(App):
    def __init__(self, **kwargs):
        super(CamApp, self).__init__(**kwargs)
        self.verification_label_text = "Welcome"
        self.current_image = None
        self.is_verifying = False
        self.capture = cv2.VideoCapture(0)  # Assuming webcam index is 0

    def build(self):
        # Main layout components
        self.title = "Facial recognition model"
        self.camera = Camera(size_hint=(1, 0.6), pos_hint={'center_y': 0.5})  # Centered, taking 60% height
        self.button = Button(text="Verify", on_press=self.verify, size_hint=(None, 0.4))
        self.verification_label = Label(text=self.verification_label_text, size_hint=(1, 0.2))  # Taking 20% height

        # Add buttons to a horizontal box layout with padding and spacing
        button_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, 0.4))  # Taking 20% height
        button_layout.padding = dp(40)  # Left and right padding
        self.button.size_hint_x = self.camera.size_hint_x
        button_layout.add_widget(self.button)

        # Add items to main vertical layout
        layout = BoxLayout(orientation='vertical')
        layout.padding = dp(40)
        layout.add_widget(self.camera)
        button_layout.pos_hint = {'center_x': 0.5}
        layout.add_widget(button_layout)
        layout.add_widget(self.verification_label)

        # Setup video capture and update loop
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update every 30 FPS
        self.verification_label.bind(text=self.on_verification_label_text_change)

        return layout

    def on_verification_label_text_change(self, instance, value):
        self.verification_label_text = value

    def update(self, *args):
        if self.is_verifying is False:
            try:
                # Read frame from OpenCV
                ret, frame = self.capture.read()
                if ret:
                    # Flip the frame horizontally and convert it to a texture
                    frame = cv2.flip(frame, 0)
                    buf = frame.tobytes()
                    img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

                    # Update the webcam texture
                    if not self.is_verifying:
                        self.camera.texture = img_texture
                else:
                    Logger.warning("Failed to capture frame from the camera.")
            except cv2.error as e:
                Logger.error(f"OpenCV error: {e}")
            except Exception as e:
                Logger.error(f"Unexpected error occurred: {e}")

    def face_detect(self, imgpath):
        try:
            dfs = DeepFace.find(imgpath, db_path="train", model_name="ArcFace")
            if len(dfs) > 0:
                df = pd.DataFrame(dfs[0])
                result = [(num+1, row['identity'].split("\\")[1], row['distance']) for num, row in df.iterrows()]
                if len(result) > 0:
                    image = cv2.imread(imgpath)
                    first_prediction = df.iloc[0]
                    x, y, w, h = first_prediction['source_x'], first_prediction['source_y'], first_prediction['source_w'], first_prediction['source_h']
                    img = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    return img, result
                else:
                    return None, "No match"
        except Exception as e:
            Logger.error(f"Error in face_detect: {e}")
            return None, "Face Not Detected"

    def verify(self, *args):
        start = time.time()
        self.save_path = os.path.join('input_image', 'input_image.jpg')
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite(self.save_path, frame)
            pass
        else:
            Logger.error("Failed to capture frame for verification.")
            self.verification_label.text = "Failed to capture frame"
            self.verification_label.color = get_color_from_hex('#FF0000')  # Red
            return

        img_rec, output_data = self.face_detect(self.save_path)
        if img_rec is not None:
            cv2.imwrite(self.save_path, img_rec)

        self.is_verifying = True
        self.current_image = cv2.imread(self.save_path)
        end = time.time()
        timer = end - start

        img_texture = Texture.create(size=(500, 500), colorfmt='bgr')
        img_texture.blit_buffer(self.current_image.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.camera.texture = img_texture

        # Update label based on output
        if output_data == "No match":
            self.verification_label.text = output_data
            self.verification_label.color = get_color_from_hex('#FF0000')  # Red
        elif output_data == "Face Not Detected":
            self.verification_label.text = output_data
            self.verification_label.color = get_color_from_hex('#FF0000')  # Red
        else:
            self.verification_label.text = f"Face Predicted \n {output_data[0]}"
            self.verification_label.color = get_color_from_hex('#00FF00')  # Green

        Logger.info(f"Output: {output_data}")
        Logger.info(f"Execution time: {timer*1000:.2f} ms")
        print("\n")

        Clock.schedule_once(self.reset_verification_label, 5)
        return output_data

    def reset_verification_label(self, *args):
        self.verification_label.color = "white"
        self.verification_label.text = "Welcome"
        self.is_verifying = False

        ret, _ = self.capture.read()

if __name__ == '__main__':
    CamApp().run()
