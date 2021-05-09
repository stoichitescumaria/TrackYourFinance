from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
import json, glob

#form
class AddNewForm(Widget):
    def submit_input(self, type, price, comment):
        with open("transactions.json", 'r') as file:
            data = json.load(file)

        data += [{'type': type, 'price': price,
                            'comment': comment}]
        with open("transactions.json", 'w') as file:
            json.dump(data, file)


#menu
class Menu(BoxLayout):
    manager = ObjectProperty(None)


#recycle view for home screen
class MyRecycleView(RecycleView):

    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()
        print(self.load_data)
    def load_data(self, *args):
        with open("transactions.json", 'r') as file:
            data = json.load(file)
        list_data = []
        list_data.append({'text' : 'type' + "                " +'price' + "                   " +'comment'})
        for item in data:
            list_data.append({'text' : item['type'] + "                " + item['price'] + "                   " + item['comment']})

        self.data = list_data 


# Declare both screens and manager
class HomeScreen(Screen):
    pass


class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.addNewForm = AddNewForm()
        self.add_widget(self.addNewForm)


class ScreenManagement(ScreenManager):
    screen_home = ObjectProperty(None)
    screen_add = ObjectProperty(None)


#app class
class TransactionsApp(App):
    pass
    # def build(self):
    #     return Menu()

if __name__ == '__main__':
    TransactionsApp().run()