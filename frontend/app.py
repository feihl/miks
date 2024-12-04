from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
import requests
from kivy.clock import Clock
from threading import Thread

BASE_URL = "http://127.0.0.1:8000"  # FastAPI server URL


# Screen for Register
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Username Input
        layout.add_widget(Label(text="Username"))
        self.username_input = TextInput(hint_text="Enter your username", multiline=False)
        layout.add_widget(self.username_input)

        # Email Input
        layout.add_widget(Label(text="Email"))
        self.email_input = TextInput(hint_text="Enter your email", multiline=False)
        layout.add_widget(self.email_input)

        # Password Input
        layout.add_widget(Label(text="Password"))
        self.password_input = TextInput(hint_text="Enter your password", password=True, multiline=False)
        layout.add_widget(self.password_input)

        # Submit Button
        self.submit_button = Button(text="Register")
        self.submit_button.bind(on_press=self.register_user)
        layout.add_widget(self.submit_button)

        # Login Button (added)
        self.login_button = Button(text="Go to Login")
        self.login_button.bind(on_press=self.go_to_login)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def register_user(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not username or not email or not password:
            print("All fields are required.")
            return

        payload = {"username": username, "email": email, "password": password}
        try:
            response = requests.post(f"{BASE_URL}/users/", json=payload)
            if response.status_code == 200:
                print("User registered successfully.")
                self.manager.current = "login"  # Navigate to LoginScreen
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def go_to_login(self, instance):
        self.manager.current = "login"  # Navigate to LoginScreen


# Screen for Login
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Username Input
        layout.add_widget(Label(text="Username"))
        self.username_input = TextInput(hint_text="Enter your username", multiline=False)
        layout.add_widget(self.username_input)

        # Password Input
        layout.add_widget(Label(text="Password"))
        self.password_input = TextInput(hint_text="Enter your password", password=True, multiline=False)
        layout.add_widget(self.password_input)

        # Login Button
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.login_user)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            print("Both fields are required.")
            return

        payload = {"username": username, "password": password}
        try:
            response = requests.post(f"{BASE_URL}/login/", json=payload)
            if response.status_code == 200:
                print("Login successful.")
                self.manager.current = "playlist"  # Navigate to PlaylistScreen
            else:
                print("Invalid credentials.")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")


# Screen for Playlist CRUD Operations
class PlaylistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Create Playlist Section
        layout.add_widget(Label(text="Create Playlist"))
        self.playlist_name_input = TextInput(hint_text="Playlist Name", multiline=False)
        self.user_id_input = TextInput(hint_text="User ID", multiline=False)
        layout.add_widget(self.playlist_name_input)
        layout.add_widget(self.user_id_input)
        self.create_button = Button(text="Create Playlist")
        self.create_button.bind(on_press=self.create_playlist)
        layout.add_widget(self.create_button)

        # Get All Playlists Section
        layout.add_widget(Label(text="Playlists"))
        self.playlist_list = RecycleView()
        self.playlist_list.viewclass = 'Label'  # Template for each item in the RecycleView
        layout.add_widget(self.playlist_list)
        self.get_all_button = Button(text="Get All Playlists")
        self.get_all_button.bind(on_press=self.get_all_playlists)
        layout.add_widget(self.get_all_button)

        # Update Playlist Section
        layout.add_widget(Label(text="Update Playlist"))
        self.update_id_input = TextInput(hint_text="Playlist ID", multiline=False)
        self.update_name_input = TextInput(hint_text="New Playlist Name", multiline=False)
        layout.add_widget(self.update_id_input)
        layout.add_widget(self.update_name_input)
        self.update_button = Button(text="Update Playlist")
        self.update_button.bind(on_press=self.update_playlist)
        layout.add_widget(self.update_button)

        # Delete Playlist Section
        layout.add_widget(Label(text="Delete Playlist"))
        self.delete_id_input = TextInput(hint_text="Playlist ID", multiline=False)
        layout.add_widget(self.delete_id_input)
        self.delete_button = Button(text="Delete Playlist")
        self.delete_button.bind(on_press=self.delete_playlist)
        layout.add_widget(self.delete_button)

        self.add_widget(layout)

    def create_playlist(self, instance):
        name = self.playlist_name_input.text
        user_id = self.user_id_input.text
        if name and user_id:
            try:
                response = requests.post(f"{BASE_URL}/playlists/", json={"name": name, "user_id": int(user_id)})
                response_data = response.json()
                print(response_data)
                if response.status_code == 200:
                    print("Playlist created successfully.")
                else:
                    print(f"Error: {response_data}")
            except ValueError:
                print("Invalid user ID format.")
            except Exception as e:
                print(f"Failed to connect to the server: {e}")
        else:
            print("Name and User ID are required")

    def get_all_playlists(self, instance):
        def fetch_playlists():
            try:
                response = requests.get(f"{BASE_URL}/playlists/")
                if response.status_code == 200:
                    playlists = response.json()
                    if playlists:
                        Clock.schedule_once(lambda dt: self.update_playlist_list(playlists), 0)
                        print("Playlists fetched and scheduled for UI update")
                    else:
                        print("No playlists found")
                else:
                    print("Failed to retrieve playlists")
            except Exception as e:
                print(f"Failed to connect to the server: {e}")

        # Run the request in a separate thread to avoid blocking the UI
        Thread(target=fetch_playlists, daemon=True).start()

    def update_playlist_list(self, playlists):
        # Check if the response is a list of dictionaries or a simple list
        self.playlist_list.data.clear()
        if isinstance(playlists, list):
            for playlist in playlists:
                # If the response is a list of dictionaries with a 'name' key
                if isinstance(playlist, dict) and 'name' in playlist:
                    self.playlist_list.data.append({"text": playlist['name']})
                elif isinstance(playlist, str):  # If it's a simple list of names
                    self.playlist_list.data.append({"text": playlist})
                else:
                    self.playlist_list.data.append({"text": "Unknown item"})
        else:
            print("Unexpected response format")

    def update_playlist(self, instance):
        playlist_id = self.update_id_input.text
        new_name = self.update_name_input.text
        user_id = self.user_id_input.text  # Assume you have a field for user ID if needed

        # Debug: Print the values to ensure they are correct
        print(f"Playlist ID: {playlist_id}")
        print(f"New Name: {new_name}")
        print(f"User ID: {user_id}")

        if playlist_id and new_name:
            try:
                # Convert user_id to int and handle possible ValueError
                if user_id:
                    user_id = int(user_id)  # Ensure user ID is an integer
                    response = requests.put(
                        f"{BASE_URL}/playlists/{playlist_id}",
                        json={"name": new_name, "user_id": user_id}
                    )
                else:
                    response = requests.put(
                        f"{BASE_URL}/playlists/{playlist_id}",
                        json={"name": new_name}
                    )
                
                response_data = response.json()
                print(response_data)

            except ValueError:
                print("Invalid user ID format. Ensure the user ID is a number.")
            except Exception as e:
                print(f"Failed to connect to the server: {e}")
        else:
            print("Playlist ID, New Name, and User ID are required")

    def delete_playlist(self, instance):
        playlist_id = self.delete_id_input.text
        if playlist_id:
            response = requests.delete(f"{BASE_URL}/playlists/{playlist_id}")
            print(response.json())
        else:
            print("Playlist ID is required")


# Main App
class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        return sm


if __name__ == '__main__':
    MainApp().run()
