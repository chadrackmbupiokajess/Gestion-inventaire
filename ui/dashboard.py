"""
Tableau de bord principal
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from models.produit import Produit
from models.vente import Vente
from config import SEUIL_STOCK_FAIBLE
from datetime import datetime


class DashboardScreen(Screen):
    """Écran du tableau de bord"""

    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.name = 'dashboard'
        self.build_ui()

    def build_ui(self):
        """Construire l'interface du tableau de bord"""
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure avec titre et déconnexion
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        self.titre_label = Label(
            text='Tableau de bord - AGIB',
            font_size='20sp',
            bold=True,
            size_hint=(0.7, 1),
            color=(1, 1, 1, 1)
        )
        top_bar.add_widget(self.titre_label)

        logout_btn = Button(
            text='Déconnexion',
            size_hint=(0.3, 1),
            background_color=(0.9, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        logout_btn.bind(on_press=self.on_logout)
        top_bar.add_widget(logout_btn)

        main_layout.add_widget(top_bar)

        # Zone des statistiques
        stats_layout = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.3))

        self.total_produits_label = Label(
            text='Total produits: 0',
            font_size='16sp',
            halign='center',
            color=(0.5, 0.8, 1, 1)
        )
        stats_layout.add_widget(self.total_produits_label)

        self.ventes_jour_label = Label(
            text='Ventes du jour: 0.00',
            font_size='16sp',
            halign='center',
            color=(0.4, 1, 0.6, 1)
        )
        stats_layout.add_widget(self.ventes_jour_label)

        self.stock_faible_label = Label(
            text='Produits en rupture: 0',
            font_size='16sp',
            halign='center',
            color=(1, 0.6, 0.3, 1)
        )
        stats_layout.add_widget(self.stock_faible_label)

        self.valeur_stock_label = Label(
            text='Valeur du stock: 0.00',
            font_size='16sp',
            halign='center',
            color=(1, 0.9, 0.4, 1)
        )
        stats_layout.add_widget(self.valeur_stock_label)

        main_layout.add_widget(stats_layout)

        # Menu principal - Boutons de navigation
        self.menu_layout = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.7))

        # Bouton Produits
        produits_btn = Button(
            text='Gestion des\nProduits',
            font_size='18sp',
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        produits_btn.bind(on_press=lambda x: self.navigate_to('produits'))
        self.menu_layout.add_widget(produits_btn)

        # Bouton Ventes
        ventes_btn = Button(
            text='Gestion des\nVentes',
            font_size='18sp',
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        ventes_btn.bind(on_press=lambda x: self.navigate_to('ventes'))
        self.menu_layout.add_widget(ventes_btn)

        # Bouton Achats (uniquement pour les admins)
        self.achats_btn = Button(
            text='Gestion des\nAchats',
            font_size='18sp',
            background_color=(1, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.achats_btn.bind(on_press=lambda x: self.navigate_to('achats'))
        # Le bouton sera ajouté dynamiquement dans on_enter si l'utilisateur est admin

        # Bouton Rapports (uniquement pour les admins)
        self.rapports_btn = Button(
            text='Rapports &\nExports',
            font_size='18sp',
            background_color=(0.7, 0.3, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        self.rapports_btn.bind(on_press=lambda x: self.navigate_to('rapports'))
        # Le bouton sera ajouté dynamiquement dans on_enter si l'utilisateur est admin

        # Bouton Utilisateurs (visible uniquement pour les admins)
        self.utilisateurs_btn = Button(
            text='Gestion des\nUtilisateurs',
            font_size='18sp',
            background_color=(0.9, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.utilisateurs_btn.bind(on_press=lambda x: self.navigate_to('utilisateurs'))
        # Le bouton sera ajouté dynamiquement dans on_enter si l'utilisateur est admin

        # Bouton Rapport Journalier (visible pour les vendeurs)
        self.rapport_vendeur_btn = Button(
            text='Rapport\nJournalier',
            font_size='18sp',
            background_color=(0.3, 0.7, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        self.rapport_vendeur_btn.bind(on_press=lambda x: self.navigate_to('rapport_vendeur'))
        # Le bouton sera ajouté dynamiquement dans on_enter si l'utilisateur est vendeur

        main_layout.add_widget(self.menu_layout)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        self.refresh_stats()

        # Mettre à jour le titre avec le nom de l'utilisateur
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            user = app.current_user
            self.titre_label.text = f"Tableau de bord - {user['nom']} ({user['role']})"

            # Afficher les boutons selon le rôle
            if user['role'] == 'Administrateur':
                # Admins voient tous les boutons sauf le rapport vendeur
                if self.achats_btn not in self.menu_layout.children:
                    self.menu_layout.add_widget(self.achats_btn)
                if self.rapports_btn not in self.menu_layout.children:
                    self.menu_layout.add_widget(self.rapports_btn)
                if self.utilisateurs_btn not in self.menu_layout.children:
                    self.menu_layout.add_widget(self.utilisateurs_btn)
                # Retirer le bouton rapport vendeur pour les admins
                if self.rapport_vendeur_btn in self.menu_layout.children:
                    self.menu_layout.remove_widget(self.rapport_vendeur_btn)
            else:
                # Vendeurs ne voient pas les boutons admin mais voient le rapport journalier
                if self.achats_btn in self.menu_layout.children:
                    self.menu_layout.remove_widget(self.achats_btn)
                if self.rapports_btn in self.menu_layout.children:
                    self.menu_layout.remove_widget(self.rapports_btn)
                if self.utilisateurs_btn in self.menu_layout.children:
                    self.menu_layout.remove_widget(self.utilisateurs_btn)
                # Ajouter le bouton rapport vendeur pour les vendeurs
                if self.rapport_vendeur_btn not in self.menu_layout.children:
                    self.menu_layout.add_widget(self.rapport_vendeur_btn)

    def refresh_stats(self):
        """Rafraîchir les statistiques"""
        # Total des produits
        produits = Produit.obtenir_tous()
        self.total_produits_label.text = f'Total produits: {len(produits)}'

        # Ventes du jour
        date_aujourd_hui = datetime.now().strftime("%Y-%m-%d")
        total_ventes = Vente.calculer_total_jour(date_aujourd_hui)
        self.ventes_jour_label.text = f'Ventes du jour: {total_ventes:.2f}'

        # Produits en rupture
        produits_rupture = Produit.obtenir_stock_faible(SEUIL_STOCK_FAIBLE)
        self.stock_faible_label.text = f'Produits en rupture: {len(produits_rupture)}'

        # Valeur du stock
        valeur_stock = sum(p['quantite'] * p['prix_achat'] for p in produits)
        self.valeur_stock_label.text = f'Valeur du stock: {valeur_stock:.2f}'

    def navigate_to(self, screen_name):
        """Naviguer vers un autre écran"""
        self.manager.current = screen_name

    def on_logout(self, instance):
        """Gérer la déconnexion"""
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'current_user'):
            app.current_user = None
        self.manager.current = 'login'
