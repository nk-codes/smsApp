from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.phone_input = TextInput(hint_text='Enter Phone Number')
        self.password_input = TextInput(hint_text='Enter Password', password=True)
        self.layout.add_widget(Label(text='Login'))
        self.layout.add_widget(Label(text='Phone Number:'))
        self.layout.add_widget(self.phone_input)
        self.layout.add_widget(Label(text='Password:'))
        self.layout.add_widget(self.password_input)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)
        self.layout.add_widget(login_button)
        self.add_widget(self.layout)

    def login(self, instance):
        # Add your authentication logic here
        # For simplicity, let's just check if the phone number and password are not empty
        phone_number = self.phone_input.text
        password = self.password_input.text

        if phone_number and password:
            self.manager.current = 'main'
        else:
            print('Invalid login credentials')

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.file_chooser = FileChooserListView()
        self.layout.add_widget(Label(text='Select Excel file:'))
        self.layout.add_widget(self.file_chooser)
        send_button = Button(text='Send Messages')
        send_button.bind(on_press=self.send_messages)
        self.layout.add_widget(send_button)
        self.add_widget(self.layout)

    def send_messages(self, instance):
        # Get the selected file path from the file chooser
        file_path = self.file_chooser.selection[0]

        try:
            # Read the data from the Excel file
            data = pd.read_excel(file_path)

            # Iterate through the rows and send messages
            for index, row in data.iterrows():
                name = row['Name']
                phone_number = str(row['Phone'])
                message = row['Message']
                self.send_message(name, phone_number, message)

        except Exception as e:
            print(f'Error reading Excel file or sending messages: {e}')

    def send_message(self, name, phone_number, message):
        # Modify this method to send messages using your preferred method
        # For example, you can use a messaging API or any other method to send messages
        print(f'Sending message to {name} ({phone_number}): {message}')
        # Add your message-sending logic here

class BulkMessageApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        return self.sm

if __name__ == '__main__':
    BulkMessageApp().run()
