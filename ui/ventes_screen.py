"""
Écran de gestion des ventes
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from models.produit import Produit
from models.vente import Vente
from utils.export import ExportManager
from datetime import datetime


class VentesScreen(Screen):
    """Écran de gestion des ventes"""

    def __init__(self, **kwargs):
        super(VentesScreen, self).__init__(**kwargs)
        self.name = 'ventes'
        self.ventes = []
        self.produits = []
        self.panier = []  # Liste des produits dans le panier
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = MDLabel(text='Gestion des Ventes', font_style='H5', bold=True, size_hint=(0.5, 1))
        top_bar.add_widget(titre)

        retour_btn = MDRaisedButton(text='Retour', size_hint=(0.25, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        nouvelle_vente_btn = MDRaisedButton(text='Nouvelle Vente', size_hint=(0.25, 1), md_bg_color=(0.2, 0.8, 0.4, 1))
        nouvelle_vente_btn.bind(on_press=self.show_nouvelle_vente_popup)
        top_bar.add_widget(nouvelle_vente_btn)

        main_layout.add_widget(top_bar)

        # Statistiques du jour
        stats_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))

        self.total_jour_label = MDLabel(
            text='Total du jour: 0.00',
            font_style='H6',
            bold=True,
            theme_text_color="Custom",
            text_color=(0.4, 1, 0.6, 1)
        )
        stats_layout.add_widget(self.total_jour_label)

        self.nb_ventes_label = MDLabel(
            text='Nombre de ventes: 0',
            font_style='H6'
        )
        stats_layout.add_widget(self.nb_ventes_label)

        main_layout.add_widget(stats_layout)

        # Liste des ventes
        self.ventes_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.ventes_layout.bind(minimum_height=self.ventes_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.ventes_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        self.refresh_list()

    def refresh_list(self):
        """Rafraîchir la liste des ventes"""
        self.ventes_layout.clear_widgets()

        # Obtenir les ventes du jour
        date_aujourd_hui = datetime.now().strftime("%Y-%m-%d")
        self.ventes = Vente.obtenir_par_jour(date_aujourd_hui)
        total = Vente.calculer_total_jour(date_aujourd_hui)

        # Mettre à jour les statistiques
        self.total_jour_label.text = f'Total du jour: {total:.2f}'
        self.nb_ventes_label.text = f'Nombre de ventes: {len(self.ventes)}'

        # Afficher les ventes
        for vente in self.ventes:
            item = self.create_vente_item(vente)
            self.ventes_layout.add_widget(item)

        # Charger les produits pour les nouvelles ventes
        self.produits = Produit.obtenir_tous()

    def create_vente_item(self, vente):
        """Créer un widget pour une vente"""
        card = MDCard(size_hint_y=None, height=dp(70), padding=dp(5))
        layout = BoxLayout(spacing=dp(5))

        # Informations de la vente
        info_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        dt = datetime.fromisoformat(vente['date'])
        heure = dt.strftime("%H:%M:%S")

        produit_label = MDLabel(
            text=f"{vente['produit_nom']} ({vente['produit_code']}) - {heure}",
            font_style='Subtitle1',
            bold=True,
        )
        info_layout.add_widget(produit_label)

        details_label = MDLabel(
            text=f"Qté: {vente['quantite']} x {vente['prix_unitaire']:.2f} = {vente['montant_total']:.2f} | Vendeur: {vente['utilisateur_nom']}",
            font_style='Body2',
            theme_text_color="Secondary"
        )
        info_layout.add_widget(details_label)

        layout.add_widget(info_layout)

        # Bouton d'export du ticket
        ticket_btn = MDIconButton(icon='receipt', on_press=lambda x: self.export_ticket(vente['id']))
        layout.add_widget(ticket_btn)
        card.add_widget(layout)

        return card

    def show_nouvelle_vente_popup(self, instance):
        """Afficher le popup de nouvelle vente avec panier"""
        self.panier = []

        # --- Layout principal du Popup ---
        popup_main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), size_hint_y=None)
        popup_main_layout.bind(minimum_height=popup_main_layout.setter('height'))

        # --- Card pour l'ajout de produit ---
        add_product_card = MDCard(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        add_product_card.bind(minimum_height=add_product_card.setter('height'))

        add_product_card.add_widget(MDLabel(text="Ajouter un Produit", font_style="H6", adaptive_height=True))

        self.produit_search_input = MDTextField(hint_text='Rechercher produit (nom ou code)', mode="fill")
        add_product_card.add_widget(self.produit_search_input)
        
        self.search_results_layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.search_results_layout.bind(minimum_height=self.search_results_layout.setter('height'))
        add_product_card.add_widget(self.search_results_layout)

        self.produit_selected_label = MDLabel(text='Aucun produit sélectionné', theme_text_color="Hint", adaptive_height=True)
        add_product_card.add_widget(self.produit_selected_label)

        # Layout pour Quantité et Prix
        inputs_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(60))
        quantite_input = MDTextField(hint_text='Quantité', input_filter='int', text='1')
        prix_input = MDTextField(hint_text='Prix unitaire', input_filter='float', text='0.00')
        inputs_layout.add_widget(quantite_input)
        inputs_layout.add_widget(prix_input)
        add_product_card.add_widget(inputs_layout)

        total_ligne_label = MDLabel(text='Total ligne: 0.00', font_style='Subtitle1', bold=True, theme_text_color="Primary", adaptive_height=True)
        add_product_card.add_widget(total_ligne_label)

        separator = BoxLayout(size_hint_y=None, height=dp(1))
        try:
            separator.md_bg_color = MDApp.get_running_app().theme_cls.divider_color
        except AttributeError: # Pour compatibilité avec anciennes versions de KivyMD
            from kivy.graphics import Color, Rectangle
            with separator.canvas.before:
                Color(rgba=MDApp.get_running_app().theme_cls.divider_color)
                Rectangle(pos=separator.pos, size=separator.size)

        add_product_card.add_widget(separator)


        ajouter_panier_btn = MDRaisedButton(text='Ajouter au panier', icon='plus', md_bg_color=(0.2, 0.8, 0.4, 1), size_hint_x=1)
        add_product_card.add_widget(ajouter_panier_btn)

        popup_main_layout.add_widget(add_product_card)

        # --- Card pour le Panier ---
        panier_card = MDCard(orientation='vertical', padding=dp(15), spacing=dp(10), size_hint_y=None)
        panier_card.bind(minimum_height=panier_card.setter('height'))

        panier_header = BoxLayout(size_hint_y=None, height=dp(30))
        panier_label = MDLabel(text="Panier", font_style="H6")
        self.panier_count_label = MDLabel(text="(0 articles)", halign="right", theme_text_color="Secondary")
        panier_header.add_widget(panier_label)
        panier_header.add_widget(self.panier_count_label)
        panier_card.add_widget(panier_header)

        self.panier_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.panier_layout.bind(minimum_height=self.panier_layout.setter('height'))
        panier_card.add_widget(self.panier_layout)

        separator2 = BoxLayout(size_hint_y=None, height=dp(1))
        try:
            separator2.md_bg_color = MDApp.get_running_app().theme_cls.divider_color
        except AttributeError:
            from kivy.graphics import Color, Rectangle
            with separator2.canvas.before:
                Color(rgba=MDApp.get_running_app().theme_cls.divider_color)
                Rectangle(pos=separator2.pos, size=separator2.size)
        panier_card.add_widget(separator2)

        total_panier_layout = BoxLayout(size_hint_y=None, height=dp(35))
        total_panier_layout.add_widget(MDLabel(text='TOTAL PANIER:', font_style='H6', bold=True))
        self.total_panier_label = MDLabel(text='0.00', font_style='H5', bold=True, halign="right", theme_text_color="Custom", text_color=(0.4, 1, 0.6, 1))
        total_panier_layout.add_widget(self.total_panier_label)
        panier_card.add_widget(total_panier_layout)

        popup_main_layout.add_widget(panier_card)

        # --- Boutons d'action finaux ---
        final_buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        annuler_btn = MDFlatButton(text='Annuler')
        valider_btn = MDRaisedButton(text='Valider la vente', icon='check-circle', md_bg_color=(0.2, 0.8, 0.4, 1))
        final_buttons_layout.add_widget(annuler_btn)
        final_buttons_layout.add_widget(valider_btn)
        popup_main_layout.add_widget(final_buttons_layout)

        # --- Logique ---
        self.selected_produit = None
        self.search_results = []

        def on_search_text_validate(instance):
            if self.search_results:
                select_produit(self.search_results[0])
            elif not instance.text:
                ajouter_au_panier(None)

        def search_produits(instance, value):
            self.search_results_layout.clear_widgets()
            self.search_results = []
            if len(value) < 2: return
            self.search_results = [p for p in self.produits if value.lower() in p['nom'].lower() or value.lower() in p['code'].lower()]
            if not self.search_results:
                self.search_results_layout.add_widget(MDLabel(text='Aucun produit trouvé', halign='center', theme_text_color="Secondary"))
            else:
                for p in self.search_results[:10]:
                    btn = MDRaisedButton(text=f"{p['nom']} ({p['code']}) - Stock: {p['quantite']}", on_press=lambda x, prod=p: select_produit(prod))
                    self.search_results_layout.add_widget(btn)

        def select_produit(produit):
            self.selected_produit = produit
            self.produit_selected_label.text = f"{produit['nom']} ({produit['code']})"
            self.produit_selected_label.theme_text_color = "Primary"
            prix_input.text = str(produit['prix_vente'])
            self.search_results_layout.clear_widgets()
            self.produit_search_input.text = ""
            update_total_ligne(None, None)

        def update_total_ligne(instance, value):
            try:
                qte = int(quantite_input.text) if quantite_input.text else 0
                prix = float(prix_input.text) if prix_input.text else 0.0
                total_ligne_label.text = f"Total ligne: {qte * prix:.2f}"
            except:
                total_ligne_label.text = "Total ligne: 0.00"

        def ajouter_au_panier(instance):
            if not self.selected_produit:
                self.show_message('Erreur', 'Veuillez sélectionner un produit')
                return
            try:
                quantite = int(quantite_input.text)
                prix_unitaire = float(prix_input.text)
                if quantite <= 0 or prix_unitaire <= 0:
                    self.show_message('Erreur', 'La quantité et le prix doivent être supérieurs à 0')
                    return
                if self.selected_produit['quantite'] < quantite:
                    self.show_message('Erreur', f"Stock insuffisant. Disponible: {self.selected_produit['quantite']}")
                    return
                self.panier.append({'produit': self.selected_produit, 'quantite': quantite, 'prix_unitaire': prix_unitaire, 'total': quantite * prix_unitaire})
                self.produit_search_input.text = ''
                quantite_input.text = '1'
                prix_input.text = '0.00'
                self.selected_produit = None
                self.produit_selected_label.text = 'Aucun produit sélectionné'
                self.produit_selected_label.theme_text_color = "Hint"
                update_panier_display()
            except Exception as e:
                self.show_message('Erreur', f'Erreur: {str(e)}')

        def update_panier_display():
            self.panier_layout.clear_widgets()
            self.panier_count_label.text = f'({len(self.panier)} articles)'
            total_panier = 0
            for idx, item in enumerate(self.panier):
                item_layout = BoxLayout(size_hint_y=None, height=dp(40))
                info_label = MDLabel(text=f"{item['produit']['nom']} - Qté: {item['quantite']} x {item['prix_unitaire']:.2f} = {item['total']:.2f}", adaptive_height=True)
                del_btn = MDIconButton(icon='delete', theme_text_color="Error", on_press=lambda x, i=idx: supprimer_du_panier(i))
                item_layout.add_widget(info_label)
                item_layout.add_widget(del_btn)
                self.panier_layout.add_widget(item_layout)
                total_panier += item['total']
            self.total_panier_label.text = f"{total_panier:.2f}"

        def supprimer_du_panier(index):
            if 0 <= index < len(self.panier):
                self.panier.pop(index)
                update_panier_display()

        self.produit_search_input.bind(text=search_produits)
        self.produit_search_input.bind(on_text_validate=on_search_text_validate)
        quantite_input.bind(text=update_total_ligne)
        prix_input.bind(text=update_total_ligne)
        ajouter_panier_btn.bind(on_press=ajouter_au_panier)

        # --- Popup ---
        popup = Popup(title='Nouvelle Vente', content=ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True, bar_width=dp(10)), size_hint=(0.9, 0.9), auto_dismiss=False)
        popup.content.add_widget(popup_main_layout)
        annuler_btn.bind(on_press=popup.dismiss)
        valider_btn.bind(on_press=lambda x: self.valider_panier(popup))
        popup.open()

    def valider_panier(self, popup):
        if not self.panier:
            self.show_message('Erreur', 'Le panier est vide.')
            return
        try:
            from kivy.app import App
            app = App.get_running_app()
            utilisateur_id = app.current_user['id']
            ventes_ids = [Vente.creer(item['produit']['id'], item['quantite'], item['prix_unitaire'], utilisateur_id) for item in self.panier]
            popup.dismiss()
            total_panier = sum(item['total'] for item in self.panier)
            self.show_message('Succès', f'Vente enregistrée!\n{len(self.panier)} article(s) - Total: {total_panier:.2f}', lambda: self.export_ticket_panier(ventes_ids))
            self.refresh_list()
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la validation: {str(e)}')

    def export_ticket(self, vente_id):
        try:
            chemin = ExportManager.generer_ticket_vente(vente_id)
            self.show_message('Succès', f'Ticket exporté:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export: {str(e)}')

    def export_ticket_panier(self, ventes_ids):
        try:
            chemin = ExportManager.generer_ticket_panier(ventes_ids)
            self.show_message('Succès', f'Ticket exporté:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export: {str(e)}')

    def show_message(self, titre, message, callback=None):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(MDLabel(text=message, adaptive_height=True))
        buttons_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        ok_btn = MDFlatButton(text='OK')
        buttons_layout.add_widget(ok_btn)
        if callback:
            yes_btn = MDRaisedButton(text='Oui')
            buttons_layout.add_widget(yes_btn)
        content.add_widget(buttons_layout)
        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        ok_btn.bind(on_press=popup.dismiss)
        if callback:
            yes_btn.bind(on_press=lambda x: (callback(), popup.dismiss()))
        popup.open()
