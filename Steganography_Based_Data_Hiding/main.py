from kivy import *
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from plyer import filechooser
from cryptography.fernet import Fernet
from stegano import lsb
Clock.max_iteration = 2

Window.size = (1000, 700)


class Application(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("kivyFile/pre-splash.kv"))
        screen_manager.add_widget(Builder.load_file("kivyFile/dashboard.kv"))
        screen_manager.add_widget(Builder.load_file("kivyFile/hiding.kv"))
        screen_manager.add_widget(Builder.load_file("kivyFile/unhiding.kv"))
        
        return screen_manager

    def on_start(self):
        Clock.schedule_once(self.dashboard, 4)
        # self.dashboard()

    def dashboard(self, *args):
        screen_manager.current = "dashboard"

    def hiding(self, *args):
        global h
        h = screen_manager.get_screen("hiding")
        screen_manager.current = "hiding"

    def hselect_file(self):
        filechooser.open_file(on_selection = self.hselected)

    def hselected(self, filename):
        global plainimage
        # print ("selected: %s" % filename[0])
        plainimage = filename[0]
        h.ids.imgid.source = filename[0]

    def encryption(self, ptext):
        key = Fernet.generate_key()
        # print(key)
        cypher = Fernet(key)
        plaintext = ptext
        cyphertext = cypher.encrypt(bytes(plaintext,'utf8'))
        # print(str(cyphertext,'utf8'))
        secret = lsb.hide(plainimage, str(cyphertext,'utf8'))
        secret.save("./encrypted.png")
        h.ids.privateKey.text = str(key,'utf8')

    
    def unhiding(self, *args):
        global u
        u = screen_manager.get_screen("unhiding")
        screen_manager.current = "unhiding"

    def uselect_file(self):
        filechooser.open_file(on_selection = self.uselected)

    def uselected(self, filename):
        global cypherimage
        # print ("selected: %s" % filename[0])
        cypherimage = filename[0]
        u.ids.imgId.source = filename[0]

    def decryption(self, ktext):
        key = ktext
        # print(key)
        try:
            cypher = Fernet(bytes(key,'utf8'))
            cyphertext = lsb.reveal(cypherimage)
            # print(str(cyphertext,'utf8'))
            plaintext = cypher.decrypt(bytes(cyphertext,'utf8'))
            # print(str(plaintext,'utf8'))
            u.ids.plainText.text = str(plaintext,'utf8')
        except Exception as e:
            print(str(e))
            u.ids.plainText.text = "{HMAC SHA256 Authentication Failed}"

if __name__ == "__main__":
    Application().run()
