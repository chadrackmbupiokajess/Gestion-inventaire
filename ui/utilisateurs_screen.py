"""
Écran de gestion des utilisateurs (Administrateur uniquement)
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from models.utilisateur import Utilisateur
from config import MIN_PASSWORD_LENGTH


class UtilisateursScreen(Screen):
    """Écran de gestion des utilisateurs"""

    def __init__(self, **kwargs):
        super(UtilisateursScreen, self).__init__(**kwargs)
        self.name = 'utilisateurs'
        self.utilisateurs = []
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = Label(text='Gestion des Utilisateurs', font_size='20sp', bold=True, size_hint=(0.5, 1), color=(1, 1, 1, 1))
        top_bar.add_widget(titre)

        retour_btn = Button(text='Retour', size_hint=(0.25, 1), background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        ajouter_btn = Button(text='Ajouter Utilisateur', size_hint=(0.25, 1), background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        ajouter_btn.bind(on_press=self.show_add_popup)
        top_bar.add_widget(ajouter_btn)

        main_layout.add_widget(top_bar)

        # Information
        info_label = Label(
            text='Gérez les comptes utilisateurs (Administrateurs et Vendeurs)',
            size_hint=(1, None),
            height=dp(30),
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(info_label)

        # Liste des utilisateurs
        self.utilisateurs_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.utilisateurs_layout.bind(minimum_height=self.utilisateurs_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.utilisateurs_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Vérifier que l'utilisateur est admin
        from kivy.app import App
        app = App.get_running_app()
        if not hasattr(app, 'current_user') or not app.current_user:
            self.manager.current = 'login'
            return

        if app.current_user['role'] != 'Administrateur':
            self.show_message('Accès refusé', 'Seuls les administrateurs peuvent accéder à cette section')
            self.manager.current = 'dashboard'
            return

        self.refresh_list()

    def refresh_list(self):
        """Rafraîchir la liste des utilisateurs"""
        self.utilisateurs_layout.clear_widgets()
        self.utilisateurs = Utilisateur.obtenir_tous()

        for utilisateur in self.utilisateurs:
            item = self.create_utilisateur_item(utilisateur)
            self.utilisateurs_layout.add_widget(item)

    def create_utilisateur_item(self, utilisateur):
        """Créer un widget pour un utilisateur"""
        layout = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(5), padding=dp(5))

        # Informations de l'utilisateur
        info_layout = BoxLayout(orientation='vertical', size_hint=(0.6, 1))

        nom_label = Label(
            text=f"{utilisateur['nom']}",
            font_size='16sp',
            bold=True,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        nom_label.bind(size=nom_label.setter('text_size'))
        info_layout.add_widget(nom_label)

        # Couleur selon le rôle
        role_color = (0.2, 0.8, 1, 1) if utilisateur['role'] == 'Administrateur' else (0.4, 1, 0.6, 1)
        details_label = Label(
            text=f"Rôle: {utilisateur['role']}",
            font_size='14sp',
            halign='left',
            valign='middle',
            color=role_color
        )
        details_label.bind(size=details_label.setter('text_size'))
        info_layout.add_widget(details_label)

        layout.add_widget(info_layout)

        # Boutons d'action
        actions_layout = BoxLayout(orientation='vertical', size_hint=(0.4, 1), spacing=dp(5))

        changer_mdp_btn = Button(text='Changer mot de passe', background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        changer_mdp_btn.bind(on_press=lambda x: self.show_change_password_popup(utilisateur))
        actions_layout.add_widget(changer_mdp_btn)

        supprimer_btn = Button(text='Supprimer', background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        supprimer_btn.bind(on_press=lambda x: self.confirm_delete(utilisateur))
        actions_layout.add_widget(supprimer_btn)

        layout.add_widget(actions_layout)

        return layout

    def show_add_popup(self, instance):
        """Afficher le popup d'ajout d'utilisateur"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Formulaire
        form = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.7))

        # Nom d'utilisateur
        form.add_widget(Label(text='Nom d\'utilisateur:', color=(1, 1, 1, 1)))
        nom_input = TextInput(
            multiline=False,
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(nom_input)

        # Rôle
        form.add_widget(Label(text='Rôle:', color=(1, 1, 1, 1)))
        role_spinner = Spinner(
            text='Vendeur',
            values=['Administrateur', 'Vendeur']
        )
        form.add_widget(role_spinner)

        # Mot de passe
        form.add_widget(Label(text='Mot de passe:', color=(1, 1, 1, 1)))
        password_input = TextInput(
            multiline=False,
            password=True,
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(password_input)

        # Confirmation mot de passe
        form.add_widget(Label(text='Confirmer mot de passe:', color=(1, 1, 1, 1)))
        confirm_password_input = TextInput(
            multiline=False,
            password=True,
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(confirm_password_input)

        content.add_widget(form)

        # Information
        info_label = Label(
            text=f'Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères',
            size_hint=(1, 0.1),
            color=(0.7, 0.7, 0.7, 1),
            font_size='12sp'
        )
        content.add_widget(info_label)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))

        annuler_btn = Button(text='Annuler', background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(annuler_btn)

        creer_btn = Button(text='Créer', background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(creer_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Ajouter un utilisateur',
            content=content,
            size_hint=(0.8, 0.7)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        creer_btn.bind(on_press=lambda x: self.create_utilisateur(
            popup, nom_input.text, role_spinner.text, password_input.text, confirm_password_input.text
        ))

        popup.open()

    def create_utilisateur(self, popup, nom, role, password, confirm_password):
        """Créer un nouvel utilisateur"""
        try:
            # Validation
            if not nom or not password:
                self.show_message('Erreur', 'Le nom et le mot de passe sont obligatoires')
                return

            if len(password) < MIN_PASSWORD_LENGTH:
                self.show_message('Erreur', f'Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères')
                return

            if password != confirm_password:
                self.show_message('Erreur', 'Les mots de passe ne correspondent pas')
                return

            # Créer l'utilisateur
            Utilisateur.creer(nom, role, password)
            self.show_message('Succès', f'Utilisateur "{nom}" créé avec succès')
            popup.dismiss()
            self.refresh_list()

        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la création: {str(e)}')

    def show_change_password_popup(self, utilisateur):
        """Afficher le popup de changement de mot de passe"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Information
        info_label = Label(
            text=f'Changer le mot de passe de : {utilisateur["nom"]}',
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        content.add_widget(info_label)

        # Formulaire
        form = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.5))

        # Nouveau mot de passe
        form.add_widget(Label(text='Nouveau mot de passe:', color=(1, 1, 1, 1)))
        new_password_input = TextInput(
            multiline=False,
            password=True,
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(new_password_input)

        # Confirmation
        form.add_widget(Label(text='Confirmer:', color=(1, 1, 1, 1)))
        confirm_password_input = TextInput(
            multiline=False,
            password=True,
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(confirm_password_input)

        content.add_widget(form)

        # Information
        info_label2 = Label(
            text=f'Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères',
            size_hint=(1, 0.1),
            color=(0.7, 0.7, 0.7, 1),
            font_size='12sp'
        )
        content.add_widget(info_label2)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))

        annuler_btn = Button(text='Annuler', background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(annuler_btn)

        modifier_btn = Button(text='Modifier', background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(modifier_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Changer le mot de passe',
            content=content,
            size_hint=(0.7, 0.6)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        modifier_btn.bind(on_press=lambda x: self.change_password(
            popup, utilisateur['id'], new_password_input.text, confirm_password_input.text
        ))

        popup.open()

    def change_password(self, popup, utilisateur_id, new_password, confirm_password):
        """Changer le mot de passe d'un utilisateur"""
        try:
            # Validation
            if not new_password:
                self.show_message('Erreur', 'Le mot de passe ne peut pas être vide')
                return

            if len(new_password) < MIN_PASSWORD_LENGTH:
                self.show_message('Erreur', f'Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères')
                return

            if new_password != confirm_password:
                self.show_message('Erreur', 'Les mots de passe ne correspondent pas')
                return

            # Modifier le mot de passe
            Utilisateur.modifier_mot_de_passe(utilisateur_id, new_password)
            self.show_message('Succès', 'Mot de passe modifié avec succès')
            popup.dismiss()

        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la modification: {str(e)}')

    def confirm_delete(self, utilisateur):
        """Confirmer la suppression d'un utilisateur"""
        # Empêcher la suppression de son propre compte
        from kivy.app import App
        app = App.get_running_app()
        if app.current_user['id'] == utilisateur['id']:
            self.show_message('Erreur', 'Vous ne pouvez pas supprimer votre propre compte')
            return

        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        content.add_widget(Label(
            text=f"Voulez-vous vraiment supprimer\nl'utilisateur '{utilisateur['nom']}' ?",
            color=(1, 1, 1, 1)
        ))

        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        annuler_btn = Button(text='Annuler', background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(annuler_btn)

        confirmer_btn = Button(text='Supprimer', background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(confirmer_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Confirmer la suppression',
            content=content,
            size_hint=(0.7, 0.3)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        confirmer_btn.bind(on_press=lambda x: self.delete_utilisateur(popup, utilisateur))

        popup.open()

    def delete_utilisateur(self, popup, utilisateur):
        """Supprimer un utilisateur"""
        try:
            Utilisateur.supprimer(utilisateur['id'])
            self.show_message('Succès', 'Utilisateur supprimé avec succès')
            popup.dismiss()
            self.refresh_list()
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la suppression: {str(e)}')

    def show_message(self, titre, message):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, color=(1, 1, 1, 1)))

        ok_btn = Button(text='OK', size_hint=(1, None), height=dp(40), background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        content.add_widget(ok_btn)

        popup = Popup(title=titre, content=content, size_hint=(0.7, 0.3))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
