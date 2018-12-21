from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import cv2
import testt

Window.size = (160*4,90*4)
# class Functions():
#     def run(self):
#         import run


#opencv_python_playscreen
class TryImage(Image):

    def build(self):
        self.capture = cv2.VideoCapture(1)
        ret, img = self.capture.read()
        self.my_camera = KivyCamera(capture=self.capture, fps=30)


    def on_stop(self):
        self.capture.release()


class KivyCamera(Image):

    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        print('hi')
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            print('duck')
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

class CloseCamera(Screen):
    pass

class ActiveCamera(Screen):
    TryImage = ObjectProperty(None)



class CameraZone(ScreenManager):
    active_cam = ObjectProperty(None)
    close_cam = ObjectProperty(None)


#image_button_stagescreen_homescreen
class ImageButton(ButtonBehavior, FloatLayout, Image):
    pass

class ScreenHome(Screen):

    def __init__(self, **kwargs):
        super(ScreenHome, self).__init__(**kwargs)

    def delay_home_switch(self):
        print('1')
        Clock.schedule_once(Manager.home_switch(self),3)
        print('2')

    # def home_switch(self):
    #     print('3')
    #     self.ids.home_screen.manager.current = 'level'

class ScreenLevel(Screen):
    pass


class ScreenStage(Screen):
    pass

class ScreenPlay(Screen):

    def call_cam(self):
        if self.ids.play_pause.text == 'Play':
            self.ids.play_pause.text = 'Stop'
            self.ids.close_cam.manager.current = 'active_cam'
            TryImage.build(self)
            # ActiveCamera.run(self)
            # Functions.run(self)
        else:
            self.ids.play_pause.text = 'Play'
            self.ids.active_cam.manager.current = 'close_cam'
            # ActiveCamera.on_stop(self)


class Manager(ScreenManager):
    home_screen = ObjectProperty(None)
    level_screen = ObjectProperty(None)

    # def home_switch(self):
    #     print('3')
    #     self.ids.home_screen.manager.current = 'level'

# presentation = Builder.load_file("main.kv")

class Main(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    Main().run()