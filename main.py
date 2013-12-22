from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from tpb import Tpb
from torrenthandler import TorrentHandler

class Cinematik(BoxLayout):
    th = TorrentHandler()
    
    def play(self, uri):
        instance = self.th.start_from_magnet(uri)
        Clock.max_iteration = 300
        Clock.schedule_once(self.check_process, 15)
        self.clear_widgets()
        self.add_widget(Label(text='Loading Metadata'))
        
    def check_process(self, dt):
        progress = self.th.check_progress()
        if progress > 0.05:
            self.clear_widgets()
            player = VideoPlayer(image_loading = 'spinner.png')
            player.source = 'http://localhost:5001/files/'+self.th.get_biggest_file()['name']
            self.add_widget(player)
        else:
            Clock.schedule_once(self.check_process, 5)
            if progress > 0.008:
                self.clear_widgets()
                n = progress/0.045*100
                self.add_widget(Label(text='Buffering: %.1f' %n))
			
    def search(self, search_string):
        self.results.search(search_string)

class CinematikSearch(Widget):
    search_box = ObjectProperty(None)
    
    def search_movie(self):
    	value = self.search_box.text
    	self.parent.search(value)

class CinematikResults(BoxLayout):
    def search(self, search_string):
    	t = Tpb()
    	self.parent.play(t.first_by_keyword(search_string))

class CinematikLatest(Widget):
    pass

class CinematikPlayer(Widget):
    pass


class CinematikApp(App):
    def build(self):
        return Cinematik()


if __name__ == '__main__':
    CinematikApp().run()