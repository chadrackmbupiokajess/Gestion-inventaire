"""
Écran de connexion
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from models.utilisateur import Utilisateur


class LoginScreen(Screen):
    """Écran de connexion de l'application"""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'
        self.build_ui()

    def build_ui(self):
        """Construire l'interface de connexion"""
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Titre
        titre = Label(
            text='AGIB - Gestion d\'Inventaire',
            size_hint=(1, 0.2),
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1)  # Texte blanc
        )
        main_layout.add_widget(titre)

        # Formulaire de connexion
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.6))

        # Nom d'utilisateur
        form_layout.add_widget(Label(
            text='Nom d\'utilisateur:',
            size_hint=(1, None),
            height=dp(30),
            color=(0.9, 0.9, 0.9, 1)
        ))
        self.username_input = TextInput(
            multiline=False,
            size_hint=(1, None),
            height=dp(40),
            font_size='16sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form_layout.add_widget(self.username_input)

        # Mot de passe
        form_layout.add_widget(Label(
            text='Mot de passe:',
            size_hint=(1, None),
            height=dp(30),
            color=(0.9, 0.9, 0.9, 1)
        ))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(40),
            font_size='16sp',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form_layout.add_widget(self.password_input)

        # Bouton de connexion
        login_btn = Button(
            text='Se connecter',
            size_hint=(1, None),
            height=dp(50),
            font_size='18sp',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.on_login)
        form_layout.add_widget(login_btn)

        main_layout.add_widget(form_layout)

        # Espace vide en bas
        main_layout.add_widget(Label(size_hint=(1, 0.2)))

        self.add_widget(main_layout)

        # Permettre la connexion avec Enter
        self.password_input.bind(on_text_validate=self.on_login)

    def on_login(self, instance):
        """Gérer la tentative de connexion"""
        username = self.username_input.text.strip()
        password = self.password_input.text

        if not username or not password:
            self.show_error("Veuillez remplir tous les champs")
            return

        # Authentifier l'utilisateur
        user = Utilisateur.authentifier(username, password)

        if user:
            # Stocker les informations de l'utilisateur dans l'app
            from kivy.app import App
            app = App.get_running_app()
            app.current_user = user

            # Rediriger vers le tableau de bord
            self.manager.current = 'dashboard'

            # Réinitialiser les champs
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            self.show_error("Nom d'utilisateur ou mot de passe incorrect")

    def show_error(self, message):
        """Afficher un message d'erreur"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))

        close_btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        content.add_widget(close_btn)

        popup = Popup(
            title='Erreur de connexion',
            content=content,
            size_hint=(0.8, 0.3)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
