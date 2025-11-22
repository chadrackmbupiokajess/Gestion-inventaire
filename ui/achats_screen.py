"""
Écran de gestion des achats
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
from models.produit import Produit
from models.achat import Achat
from datetime import datetime


class AchatsScreen(Screen):
    """Écran de gestion des achats"""

    def __init__(self, **kwargs):
        super(AchatsScreen, self).__init__(**kwargs)
        self.name = 'achats'
        self.achats = []
        self.produits = []
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = Label(text='Gestion des Achats', font_size='20sp', bold=True, size_hint=(0.5, 1), color=(1, 1, 1, 1))
        top_bar.add_widget(titre)

        retour_btn = Button(text='Retour', size_hint=(0.25, 1), background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        nouvel_achat_btn = Button(text='Nouvel Achat', size_hint=(0.25, 1), background_color=(1, 0.6, 0.2, 1), color=(1, 1, 1, 1))
        nouvel_achat_btn.bind(on_press=self.show_nouvel_achat_popup)
        top_bar.add_widget(nouvel_achat_btn)

        main_layout.add_widget(top_bar)

        # Statistiques
        stats_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))

        self.nb_achats_label = Label(
            text='Nombre d\'achats: 0',
            font_size='16sp',
            color=(0.9, 0.9, 0.9, 1)
        )
        stats_layout.add_widget(self.nb_achats_label)

        refresh_btn = Button(text='Actualiser', size_hint=(0.3, 1), background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        refresh_btn.bind(on_press=lambda x: self.refresh_list())
        stats_layout.add_widget(refresh_btn)

        main_layout.add_widget(stats_layout)

        # Liste des achats
        self.achats_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.achats_layout.bind(minimum_height=self.achats_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.achats_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Vérifier que l'utilisateur est admin (les vendeurs ne peuvent pas gérer les achats)
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            if app.current_user['role'] != 'Administrateur':
                self.show_message('Accès refusé', 'Seuls les administrateurs peuvent gérer les achats')
                self.manager.current = 'dashboard'
                return

        self.refresh_list()

    def refresh_list(self):
        """Rafraîchir la liste des achats"""
        self.achats_layout.clear_widgets()

        # Obtenir tous les achats
        self.achats = Achat.obtenir_tous()

        # Mettre à jour les statistiques
        self.nb_achats_label.text = f'Nombre d\'achats: {len(self.achats)}'

        # Afficher les achats
        for achat in self.achats:
            item = self.create_achat_item(achat)
            self.achats_layout.add_widget(item)

        # Charger les produits pour les nouveaux achats
        self.produits = Produit.obtenir_tous()

    def create_achat_item(self, achat):
        """Créer un widget pour un achat"""
        layout = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(5), padding=dp(5))

        # Informations de l'achat
        info_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        dt = datetime.fromisoformat(achat['date'])
        date_str = dt.strftime("%d/%m/%Y %H:%M")

        produit_label = Label(
            text=f"{achat['produit_nom']} ({achat['produit_code']}) - {date_str}",
            font_size='16sp',
            bold=True,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        produit_label.bind(size=produit_label.setter('text_size'))
        info_layout.add_widget(produit_label)

        details_label = Label(
            text=f"Quantité: {achat['quantite']} | Fournisseur: {achat['fournisseur'] or 'N/A'} | Par: {achat['utilisateur_nom']}",
            font_size='14sp',
            halign='left',
            valign='middle',
            color=(0.8, 0.8, 0.8, 1)
        )
        details_label.bind(size=details_label.setter('text_size'))
        info_layout.add_widget(details_label)

        layout.add_widget(info_layout)

        return layout

    def show_nouvel_achat_popup(self, instance):
        """Afficher le popup de nouvel achat"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Formulaire
        form = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.7))

        # Sélection du produit
        form.add_widget(Label(text='Produit:'))
        produits_list = [f"{p['nom']} ({p['code']}) - Stock actuel: {p['quantite']}" for p in self.produits]
        produit_spinner = Spinner(
            text='Sélectionner un produit',
            values=produits_list
        )
        form.add_widget(produit_spinner)

        # Quantité
        form.add_widget(Label(text='Quantité achetée:'))
        quantite_input = TextInput(multiline=False, input_filter='int', text='1')
        form.add_widget(quantite_input)

        # Fournisseur
        form.add_widget(Label(text='Fournisseur:'))
        fournisseur_input = TextInput(multiline=False, text='')
        form.add_widget(fournisseur_input)

        # Nouveau stock (calculé)
        form.add_widget(Label(text='Nouveau stock:'))
        nouveau_stock_label = Label(text='0', font_size='18sp', bold=True, color=(0.2, 0.8, 0.4, 1))
        form.add_widget(nouveau_stock_label)

        content.add_widget(form)

        # Fonction pour mettre à jour le nouveau stock
        def update_nouveau_stock(instance, value):
            # Extraire le code du produit sélectionné
            if '(' in produit_spinner.text and ')' in produit_spinner.text:
                code = produit_spinner.text.split('(')[1].split(')')[0]
                for p in self.produits:
                    if p['code'] == code:
                        try:
                            qte = int(quantite_input.text) if quantite_input.text else 0
                            nouveau_stock_label.text = str(p['quantite'] + qte)
                        except:
                            nouveau_stock_label.text = str(p['quantite'])
                        break

        produit_spinner.bind(text=update_nouveau_stock)
        quantite_input.bind(text=update_nouveau_stock)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, 0.3), spacing=dp(10))

        annuler_btn = Button(text='Annuler')
        buttons_layout.add_widget(annuler_btn)

        valider_btn = Button(text='Valider l\'achat', background_color=(0.8, 0.6, 0.2, 1))
        buttons_layout.add_widget(valider_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Nouvel Achat',
            content=content,
            size_hint=(0.9, 0.7)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        valider_btn.bind(on_press=lambda x: self.save_achat(
            popup, produit_spinner.text, quantite_input.text, fournisseur_input.text
        ))

        popup.open()

    def save_achat(self, popup, produit_text, quantite_text, fournisseur):
        """Sauvegarder un achat"""
        try:
            # Validation
            if produit_text == 'Sélectionner un produit':
                self.show_message('Erreur', 'Veuillez sélectionner un produit')
                return

            # Extraire le code du produit
            code = produit_text.split('(')[1].split(')')[0]
            produit = None
            for p in self.produits:
                if p['code'] == code:
                    produit = p
                    break

            if not produit:
                self.show_message('Erreur', 'Produit introuvable')
                return

            quantite = int(quantite_text) if quantite_text else 0

            if quantite <= 0:
                self.show_message('Erreur', 'La quantité doit être supérieure à 0')
                return

            # Obtenir l'utilisateur actuel
            from kivy.app import App
            app = App.get_running_app()
            if not hasattr(app, 'current_user') or not app.current_user:
                self.show_message('Erreur', 'Utilisateur non connecté')
                return

            utilisateur_id = app.current_user['id']

            # Créer l'achat
            Achat.creer(produit['id'], quantite, fournisseur, utilisateur_id)

            popup.dismiss()
            self.show_message('Succès', f'Achat enregistré avec succès!\nNouveau stock: {produit["quantite"] + quantite}')
            self.refresh_list()

        except ValueError as e:
            self.show_message('Erreur', str(e))
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'achat: {str(e)}')

    def show_message(self, titre, message):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))

        ok_btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        content.add_widget(ok_btn)

        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.3))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
