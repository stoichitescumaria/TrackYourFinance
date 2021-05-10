from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
import json, glob
from datetime import datetime
from pathlib import Path
import transactions

Builder.load_file('design.kv')

class RootWidget(ScreenManager):
    screen_home = ObjectProperty(None)
    screen_add = ObjectProperty(None)

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"

    def login(self, username, password):
        with open("users.json", 'r') as file:
            users = json.load(file)
        if username in users and users[username]['password'] == password:
            self.manager.current = 'screen_home'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

class SignUpScreen(Screen):
    def add_user(self, username, password):
        with open("users.json", 'r') as file:
            users = json.load(file)
        users[username] = {'username': username, 'password': password,
                            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "screen_home"
class AddNewForm(Widget):
    def submit_input(self, type, price, comment):
        with open("transactions.json", 'r') as file:
            data = json.load(file)

        data += [{'type': type, 'price': price,
                            'comment': comment}]
        with open("transactions.json", 'w') as file:
            json.dump(data, file)
        self.manager.current = "screen_home"


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


class HomeScreen(Screen):
    pass


class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.addNewForm = AddNewForm()
        self.add_widget(self.addNewForm)



class MainApp(App):

    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()