"""
Écran de gestion des produits
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
from models.categorie import Categorie


class ProduitsScreen(Screen):
    """Écran de gestion des produits"""

    def __init__(self, **kwargs):
        super(ProduitsScreen, self).__init__(**kwargs)
        self.name = 'produits'
        self.produits = []
        self.categories = []
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = Label(text='Gestion des Produits', font_size='20sp', bold=True, size_hint=(0.5, 1), color=(1, 1, 1, 1))
        top_bar.add_widget(titre)

        retour_btn = Button(text='Retour', size_hint=(0.25, 1), background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        # Bouton Ajouter uniquement pour les admins
        self.ajouter_btn = Button(text='Ajouter Produit', size_hint=(0.25, 1), background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        self.ajouter_btn.bind(on_press=self.show_add_popup)
        top_bar.add_widget(self.ajouter_btn)

        main_layout.add_widget(top_bar)

        # Barre de recherche
        search_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))
        search_layout.add_widget(Label(text='Rechercher:', size_hint=(0.2, 1), color=(0.9, 0.9, 0.9, 1)))

        self.search_input = TextInput(
            multiline=False,
            size_hint=(0.6, 1),
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        self.search_input.bind(text=self.on_search)
        search_layout.add_widget(self.search_input)

        refresh_btn = Button(text='Actualiser', size_hint=(0.2, 1), background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        refresh_btn.bind(on_press=lambda x: self.refresh_list())
        search_layout.add_widget(refresh_btn)

        main_layout.add_widget(search_layout)

        # Liste des produits
        self.produits_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.produits_layout.bind(minimum_height=self.produits_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.produits_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Vérifier le rôle de l'utilisateur
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            # Les vendeurs peuvent seulement consulter, pas modifier
            is_admin = app.current_user['role'] == 'Administrateur'
            # Masquer le bouton Ajouter pour les vendeurs
            if not is_admin:
                self.ajouter_btn.disabled = True
                self.ajouter_btn.opacity = 0.5
            else:
                self.ajouter_btn.disabled = False
                self.ajouter_btn.opacity = 1

        self.refresh_list()

    def refresh_list(self):
        """Rafraîchir la liste des produits"""
        self.produits_layout.clear_widgets()
        self.produits = Produit.obtenir_tous()
        self.categories = Categorie.obtenir_toutes()

        for produit in self.produits:
            item = self.create_produit_item(produit)
            self.produits_layout.add_widget(item)

    def on_search(self, instance, value):
        """Rechercher des produits"""
        if value.strip():
            self.produits = Produit.rechercher(value)
        else:
            self.produits = Produit.obtenir_tous()

        self.produits_layout.clear_widgets()
        for produit in self.produits:
            item = self.create_produit_item(produit)
            self.produits_layout.add_widget(item)

    def create_produit_item(self, produit):
        """Créer un widget pour un produit"""
        layout = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(5), padding=dp(5))

        # Informations du produit
        info_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))

        nom_label = Label(
            text=f"{produit['nom']} ({produit['code']})",
            font_size='16sp',
            bold=True,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        nom_label.bind(size=nom_label.setter('text_size'))
        info_layout.add_widget(nom_label)

        details_label = Label(
            text=f"Stock: {produit['quantite']} | Prix vente: {produit['prix_vente']:.2f} | Catégorie: {produit['categorie_nom'] or 'N/A'}",
            font_size='14sp',
            halign='left',
            valign='middle',
            color=(0.8, 0.8, 0.8, 1)
        )
        details_label.bind(size=details_label.setter('text_size'))
        info_layout.add_widget(details_label)

        layout.add_widget(info_layout)

        # Boutons d'action (uniquement pour les admins)
        from kivy.app import App
        app = App.get_running_app()
        is_admin = hasattr(app, 'current_user') and app.current_user and app.current_user['role'] == 'Administrateur'

        if is_admin:
            actions_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=dp(5))

            modifier_btn = Button(text='Modifier', background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
            modifier_btn.bind(on_press=lambda x: self.show_edit_popup(produit))
            actions_layout.add_widget(modifier_btn)

            supprimer_btn = Button(text='Supprimer', background_color=(0.9, 0.3, 0.3, 1), color=(1, 1, 1, 1))
            supprimer_btn.bind(on_press=lambda x: self.confirm_delete(produit))
            actions_layout.add_widget(supprimer_btn)

            layout.add_widget(actions_layout)

        return layout

    def show_add_popup(self, instance):
        """Afficher le popup d'ajout de produit"""
        self.show_produit_popup(None)

    def show_edit_popup(self, produit):
        """Afficher le popup de modification de produit"""
        self.show_produit_popup(produit)

    def show_produit_popup(self, produit=None):
        """Afficher le popup de création/modification de produit"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Formulaire
        form = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.8))

        # Nom
        form.add_widget(Label(text='Nom:'))
        nom_input = TextInput(multiline=False, text=produit['nom'] if produit else '')
        form.add_widget(nom_input)

        # Prix d'achat
        form.add_widget(Label(text='Prix d\'achat:'))
        prix_achat_input = TextInput(multiline=False, input_filter='float', text=str(produit['prix_achat']) if produit else '')
        form.add_widget(prix_achat_input)

        # Prix de vente
        form.add_widget(Label(text='Prix de vente:'))
        prix_vente_input = TextInput(multiline=False, input_filter='float', text=str(produit['prix_vente']) if produit else '')
        form.add_widget(prix_vente_input)

        # Quantité
        form.add_widget(Label(text='Quantité:'))
        quantite_input = TextInput(multiline=False, input_filter='int', text=str(produit['quantite']) if produit else '0')
        form.add_widget(quantite_input)

        # Catégorie
        form.add_widget(Label(text='Catégorie:'))
        categories_list = ['Aucune'] + [cat['nom'] for cat in self.categories]
        categorie_spinner = Spinner(
            text=produit['categorie_nom'] if produit and produit['categorie_nom'] else 'Aucune',
            values=categories_list
        )
        form.add_widget(categorie_spinner)

        # Date d'expiration
        form.add_widget(Label(text='Date expiration\n(YYYY-MM-DD):'))
        date_exp_input = TextInput(multiline=False, text=produit['date_expiration'] if produit and produit['date_expiration'] else '')
        form.add_widget(date_exp_input)

        content.add_widget(form)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))

        annuler_btn = Button(text='Annuler')
        buttons_layout.add_widget(annuler_btn)

        sauvegarder_btn = Button(text='Sauvegarder', background_color=(0.2, 0.8, 0.4, 1))
        buttons_layout.add_widget(sauvegarder_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Modifier Produit' if produit else 'Ajouter Produit',
            content=content,
            size_hint=(0.9, 0.9)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        sauvegarder_btn.bind(on_press=lambda x: self.save_produit(
            popup, produit, nom_input.text,
            prix_achat_input.text, prix_vente_input.text,
            quantite_input.text, categorie_spinner.text,
            date_exp_input.text
        ))

        popup.open()

    def save_produit(self, popup, produit, nom, prix_achat, prix_vente, quantite, categorie, date_exp):
        """Sauvegarder un produit"""
        try:
            # Validation
            if not nom:
                self.show_message('Erreur', 'Le nom est obligatoire')
                return

            prix_achat = float(prix_achat) if prix_achat else 0.0
            prix_vente = float(prix_vente) if prix_vente else 0.0
            quantite = int(quantite) if quantite else 0

            # Trouver l'ID de la catégorie
            categorie_id = None
            if categorie and categorie != 'Aucune':
                for cat in self.categories:
                    if cat['nom'] == categorie:
                        categorie_id = cat['id']
                        break

            date_expiration = date_exp if date_exp else None

            # Sauvegarder
            if produit:
                # Modification
                Produit.modifier(produit['id'], nom, produit['code'], prix_achat, prix_vente, quantite, categorie_id, date_expiration)
                self.show_message('Succès', 'Produit modifié avec succès')
            else:
                # Création
                Produit.creer(nom, prix_achat, prix_vente, quantite, categorie_id, date_expiration)
                self.show_message('Succès', 'Produit ajouté avec succès')

            popup.dismiss()
            self.refresh_list()

        except ValueError as e:
            self.show_message('Erreur', f'Valeurs invalides: {str(e)}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la sauvegarde: {str(e)}')

    def confirm_delete(self, produit):
        """Confirmer la suppression d'un produit"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        content.add_widget(Label(text=f"Voulez-vous vraiment supprimer\n{produit['nom']} ?"))

        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        annuler_btn = Button(text='Annuler')
        buttons_layout.add_widget(annuler_btn)

        confirmer_btn = Button(text='Supprimer', background_color=(0.8, 0.2, 0.2, 1))
        buttons_layout.add_widget(confirmer_btn)

        content.add_widget(buttons_layout)

        popup = Popup(
            title='Confirmer la suppression',
            content=content,
            size_hint=(0.8, 0.3)
        )

        annuler_btn.bind(on_press=popup.dismiss)
        confirmer_btn.bind(on_press=lambda x: self.delete_produit(popup, produit))

        popup.open()

    def delete_produit(self, popup, produit):
        """Supprimer un produit"""
        try:
            Produit.supprimer(produit['id'])
            self.show_message('Succès', 'Produit supprimé avec succès')
            popup.dismiss()
            self.refresh_list()
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la suppression: {str(e)}')

    def show_message(self, titre, message):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))

        ok_btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        content.add_widget(ok_btn)

        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.3))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
