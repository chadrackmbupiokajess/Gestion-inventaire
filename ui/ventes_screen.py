"""
Écran de gestion des ventes
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

        titre = Label(text='Gestion des Ventes', font_size='20sp', bold=True, size_hint=(0.5, 1), color=(1, 1, 1, 1))
        top_bar.add_widget(titre)

        retour_btn = Button(text='Retour', size_hint=(0.25, 1), background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        nouvelle_vente_btn = Button(text='Nouvelle Vente', size_hint=(0.25, 1), background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1))
        nouvelle_vente_btn.bind(on_press=self.show_nouvelle_vente_popup)
        top_bar.add_widget(nouvelle_vente_btn)

        main_layout.add_widget(top_bar)

        # Statistiques du jour
        stats_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))

        self.total_jour_label = Label(
            text='Total du jour: 0.00',
            font_size='16sp',
            bold=True,
            color=(0.4, 1, 0.6, 1)
        )
        stats_layout.add_widget(self.total_jour_label)

        self.nb_ventes_label = Label(
            text='Nombre de ventes: 0',
            font_size='16sp',
            color=(0.9, 0.9, 0.9, 1)
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
        layout = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(5), padding=dp(5))

        # Informations de la vente
        info_layout = BoxLayout(orientation='vertical', size_hint=(0.8, 1))

        dt = datetime.fromisoformat(vente['date'])
        heure = dt.strftime("%H:%M:%S")

        produit_label = Label(
            text=f"{vente['produit_nom']} ({vente['produit_code']}) - {heure}",
            font_size='16sp',
            bold=True,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        produit_label.bind(size=produit_label.setter('text_size'))
        info_layout.add_widget(produit_label)

        details_label = Label(
            text=f"Qté: {vente['quantite']} x {vente['prix_unitaire']:.2f} = {vente['montant_total']:.2f} | Vendeur: {vente['utilisateur_nom']}",
            font_size='14sp',
            halign='left',
            valign='middle',
            color=(0.8, 0.8, 0.8, 1)
        )
        details_label.bind(size=details_label.setter('text_size'))
        info_layout.add_widget(details_label)

        layout.add_widget(info_layout)

        # Bouton d'export du ticket
        ticket_btn = Button(
            text='Ticket',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        ticket_btn.bind(on_press=lambda x: self.export_ticket(vente['id']))
        layout.add_widget(ticket_btn)

        return layout

    def show_nouvelle_vente_popup(self, instance):
        """Afficher le popup de nouvelle vente avec panier"""
        self.panier = []  # Réinitialiser le panier

        # Layout principal qui contiendra tout le contenu du popup
        # Il est dimensionné verticalement pour s'adapter à son contenu
        popup_content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5), size_hint_y=None)
        popup_content_layout.bind(minimum_height=popup_content_layout.setter('height'))

        # === SECTION 1: FORMULAIRE DE SAISIE ===
        # Cette section s'adapte maintenant à la hauteur de son contenu
        form_section = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        form_section.bind(minimum_height=form_section.setter('height'))

        # Titre de la section
        form_titre = Label(
            text='📝 Ajouter un produit',
            size_hint=(1, None),
            height=dp(30),
            font_size='16sp',
            bold=True,
            color=(0.4, 0.8, 1, 1)
        )
        form_section.add_widget(form_titre)

        # Formulaire d'ajout de produit
        form = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))

        # Recherche du produit
        form.add_widget(Label(text='Rechercher produit:', color=(1, 1, 1, 1)))
        self.produit_search_input = TextInput(
            multiline=False,
            hint_text='Tapez le nom ou code...',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(self.produit_search_input)

        # Produit sélectionné
        form.add_widget(Label(text='Produit sélectionné:', color=(1, 1, 1, 1)))
        self.produit_selected_label = Label(
            text='Aucun produit sélectionné',
            color=(1, 0.6, 0.3, 1),
            halign='left',
            valign='middle'
        )
        self.produit_selected_label.bind(size=self.produit_selected_label.setter('text_size'))
        form.add_widget(self.produit_selected_label)

        # Quantité
        form.add_widget(Label(text='Quantité:', color=(1, 1, 1, 1)))
        quantite_input = TextInput(
            multiline=False,
            input_filter='int',
            text='1',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(quantite_input)

        # Prix unitaire
        form.add_widget(Label(text='Prix unitaire:', color=(1, 1, 1, 1)))
        prix_input = TextInput(
            multiline=False,
            input_filter='float',
            text='0.00',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1)
        )
        form.add_widget(prix_input)

        # Total de la ligne
        form.add_widget(Label(text='Total ligne:', color=(1, 1, 1, 1)))
        total_ligne_label = Label(text='0.00', font_size='18sp', bold=True, color=(0.4, 1, 0.6, 1))
        form.add_widget(total_ligne_label)

        form_section.add_widget(form)

        # Bouton pour ajouter au panier
        ajouter_panier_btn = Button(
            text='➕ Ajouter au panier',
            size_hint=(1, None),
            height=dp(45),
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True
        )
        form_section.add_widget(ajouter_panier_btn)

        popup_content_layout.add_widget(form_section)

        # Séparateur
        popup_content_layout.add_widget(Label(text='─' * 50, size_hint=(1, None), height=dp(20), color=(0.5, 0.5, 0.5, 1)))

        # === SECTION 2: RÉSULTATS DE RECHERCHE ===
        search_results_label = Label(
            text='🔍 Résultats de recherche:',
            size_hint=(1, None),
            height=dp(25),
            color=(0.9, 0.9, 0.9, 1),
            font_size='14sp'
        )
        popup_content_layout.add_widget(search_results_label)

        # ScrollView pour les résultats
        self.search_results_layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.search_results_layout.bind(minimum_height=self.search_results_layout.setter('height'))

        search_scroll = ScrollView(size_hint=(1, None), height=dp(120))
        search_scroll.add_widget(self.search_results_layout)
        popup_content_layout.add_widget(search_scroll)

        # Séparateur
        popup_content_layout.add_widget(Label(text='─' * 50, size_hint=(1, None), height=dp(20), color=(0.5, 0.5, 0.5, 1)))

        # === SECTION 3: PANIER ===
        panier_label = Label(
            text='🛒 Panier (0 articles):',
            size_hint=(1, None),
            height=dp(25),
            color=(0.4, 1, 0.6, 1),
            font_size='16sp',
            bold=True
        )
        popup_content_layout.add_widget(panier_label)

        # ScrollView pour le panier
        self.panier_layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.panier_layout.bind(minimum_height=self.panier_layout.setter('height'))

        panier_scroll = ScrollView(size_hint=(1, None), height=dp(120))
        panier_scroll.add_widget(self.panier_layout)
        popup_content_layout.add_widget(panier_scroll)

        # Total du panier
        total_panier_layout = BoxLayout(size_hint=(1, None), height=dp(35), spacing=dp(10))
        total_panier_layout.add_widget(Label(
            text='TOTAL PANIER:',
            font_size='18sp',
            bold=True,
            color=(1, 1, 1, 1)
        ))
        self.total_panier_label = Label(
            text='0.00',
            font_size='20sp',
            bold=True,
            color=(0.4, 1, 0.6, 1)
        )
        total_panier_layout.add_widget(self.total_panier_label)
        popup_content_layout.add_widget(total_panier_layout)

        # Variable pour stocker le produit sélectionné
        self.selected_produit = None

        # Fonction pour rechercher les produits
        def search_produits(instance, value):
            self.search_results_layout.clear_widgets()
            self.selected_produit = None
            self.produit_selected_label.text = 'Aucun produit sélectionné'
            self.produit_selected_label.color = (1, 0.6, 0.3, 1)
            prix_input.text = '0.00'

            if len(value) < 2:
                return

            # Rechercher les produits correspondants
            results = [p for p in self.produits if
                      value.lower() in p['nom'].lower() or
                      value.lower() in p['code'].lower()]

            if not results:
                self.search_results_layout.add_widget(Label(
                    text='Aucun produit trouvé',
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.7, 0.7, 0.7, 1)
                ))
            else:
                for p in results[:10]:  # Limiter à 10 résultats
                    # Afficher la catégorie ou "Non catégorisé"
                    categorie_text = p['categorie_nom'] if p['categorie_nom'] else 'Non catégorisé'
                    result_btn = Button(
                        text=f"{p['nom']} ({p['code']}) - {categorie_text} - Stock: {p['quantite']} - Prix: {p['prix_vente']:.2f}",
                        size_hint_y=None,
                        height=dp(40),
                        background_color=(0.25, 0.25, 0.28, 1),
                        color=(1, 1, 1, 1)
                    )
                    result_btn.bind(on_press=lambda x, prod=p: select_produit(prod))
                    self.search_results_layout.add_widget(result_btn)

        def select_produit(produit):
            self.selected_produit = produit
            self.produit_selected_label.text = f"{produit['nom']} ({produit['code']})"
            self.produit_selected_label.color = (0.4, 1, 0.6, 1)
            prix_input.text = str(produit['prix_vente'])
            self.search_results_layout.clear_widgets()
            update_total_ligne(None, None)

        def update_total_ligne(instance, value):
            try:
                qte = int(quantite_input.text) if quantite_input.text else 0
                prix = float(prix_input.text) if prix_input.text else 0.0
                total_ligne_label.text = f"{qte * prix:.2f}"
            except:
                total_ligne_label.text = "0.00"

        def ajouter_au_panier(instance):
            """Ajouter le produit au panier"""
            if not self.selected_produit:
                self.show_message('Erreur', 'Veuillez sélectionner un produit')
                return

            try:
                quantite = int(quantite_input.text) if quantite_input.text else 0
                prix_unitaire = float(prix_input.text) if prix_input.text else 0.0

                if quantite <= 0:
                    self.show_message('Erreur', 'La quantité doit être supérieure à 0')
                    return

                if prix_unitaire <= 0:
                    self.show_message('Erreur', 'Le prix doit être supérieur à 0')
                    return

                # Vérifier le stock
                if self.selected_produit['quantite'] < quantite:
                    self.show_message('Erreur', f"Stock insuffisant. Disponible: {self.selected_produit['quantite']}")
                    return

                # Ajouter au panier
                self.panier.append({
                    'produit': self.selected_produit,
                    'quantite': quantite,
                    'prix_unitaire': prix_unitaire,
                    'total': quantite * prix_unitaire
                })

                # Réinitialiser le formulaire
                self.produit_search_input.text = ''
                quantite_input.text = '1'
                prix_input.text = '0.00'
                self.selected_produit = None
                self.produit_selected_label.text = 'Aucun produit sélectionné'
                self.produit_selected_label.color = (1, 0.6, 0.3, 1)

                # Mettre à jour l'affichage du panier
                update_panier_display()

            except Exception as e:
                self.show_message('Erreur', f'Erreur: {str(e)}')

        def update_panier_display():
            """Mettre à jour l'affichage du panier"""
            self.panier_layout.clear_widgets()
            panier_label.text = f'🛒 Panier ({len(self.panier)} articles):'

            total_panier = 0
            for idx, item in enumerate(self.panier):
                item_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))

                # Info produit avec catégorie
                categorie_text = item['produit']['categorie_nom'] if item['produit']['categorie_nom'] else 'Non catégorisé'
                info_label = Label(
                    text=f"{item['produit']['nom']} ({categorie_text}) - Qté: {item['quantite']} x {item['prix_unitaire']:.2f} = {item['total']:.2f}",
                    size_hint=(0.8, 1),
                    color=(1, 1, 1, 1),
                    halign='left',
                    valign='middle'
                )
                info_label.bind(size=info_label.setter('text_size'))
                item_layout.add_widget(info_label)

                # Bouton supprimer
                del_btn = Button(
                    text='❌',
                    size_hint=(0.2, 1),
                    background_color=(0.9, 0.3, 0.3, 1),
                    color=(1, 1, 1, 1)
                )
                del_btn.bind(on_press=lambda x, i=idx: supprimer_du_panier(i))
                item_layout.add_widget(del_btn)

                self.panier_layout.add_widget(item_layout)
                total_panier += item['total']

            self.total_panier_label.text = f"{total_panier:.2f}"

        def supprimer_du_panier(index):
            """Supprimer un article du panier"""
            if 0 <= index < len(self.panier):
                self.panier.pop(index)
                update_panier_display()

        self.produit_search_input.bind(text=search_produits)
        quantite_input.bind(text=update_total_ligne)
        prix_input.bind(text=update_total_ligne)
        ajouter_panier_btn.bind(on_press=ajouter_au_panier)

        # Boutons
        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        annuler_btn = Button(text='Annuler', background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        buttons_layout.add_widget(annuler_btn)

        valider_btn = Button(text='✓ Valider la vente', background_color=(0.2, 0.8, 0.4, 1), color=(1, 1, 1, 1), font_size='16sp', bold=True)
        buttons_layout.add_widget(valider_btn)

        popup_content_layout.add_widget(buttons_layout)

        # Créer un ScrollView et y ajouter le layout principal
        root_scroll = ScrollView(size_hint=(1, 1))
        root_scroll.add_widget(popup_content_layout)

        popup = Popup(
            title='Nouvelle Vente - Panier',
            content=root_scroll,  # Le contenu du popup est maintenant le ScrollView
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        annuler_btn.bind(on_press=popup.dismiss)
        valider_btn.bind(on_press=lambda x: self.valider_panier(popup))

        popup.open()

    def valider_panier(self, popup):
        """Valider et enregistrer toutes les ventes du panier"""
        try:
            # Vérifier que le panier n'est pas vide
            if not self.panier:
                self.show_message('Erreur', 'Le panier est vide. Ajoutez au moins un produit.')
                return

            # Obtenir l'utilisateur actuel
            from kivy.app import App
            app = App.get_running_app()
            if not hasattr(app, 'current_user') or not app.current_user:
                self.show_message('Erreur', 'Utilisateur non connecté')
                return

            utilisateur_id = app.current_user['id']

            # Enregistrer chaque vente du panier
            ventes_ids = []
            for item in self.panier:
                vente_id = Vente.creer(
                    item['produit']['id'],
                    item['quantite'],
                    item['prix_unitaire'],
                    utilisateur_id
                )
                ventes_ids.append(vente_id)

            popup.dismiss()

            # Proposer d'imprimer le ticket global
            total_panier = sum(item['total'] for item in self.panier)
            nb_articles = len(self.panier)
            self.show_message(
                'Succès',
                f'Vente enregistrée avec succès!\n{nb_articles} article(s) - Total: {total_panier:.2f}\n\nVoulez-vous imprimer le ticket?',
                lambda: self.export_ticket_panier(ventes_ids)
            )
            self.refresh_list()

        except ValueError as e:
            self.show_message('Erreur', str(e))
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de la vente: {str(e)}')

    def export_ticket(self, vente_id):
        """Exporter le ticket de vente"""
        try:
            chemin = ExportManager.generer_ticket_vente(vente_id)
            self.show_message('Succès', f'Ticket exporté:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export: {str(e)}')

    def export_ticket_panier(self, ventes_ids):
        """Exporter un ticket pour plusieurs ventes (panier)"""
        try:
            chemin = ExportManager.generer_ticket_panier(ventes_ids)
            self.show_message('Succès', f'Ticket exporté:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export: {str(e)}')

    def show_message(self, titre, message, callback=None):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message))

        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(40), spacing=dp(10))

        ok_btn = Button(text='OK')
        buttons_layout.add_widget(ok_btn)

        if callback:
            yes_btn = Button(text='Oui', background_color=(0.2, 0.8, 0.4, 1))
            buttons_layout.add_widget(yes_btn)

        content.add_widget(buttons_layout)

        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.3))

        if callback:
            ok_btn.bind(on_press=popup.dismiss)
            yes_btn.bind(on_press=lambda x: (callback(), popup.dismiss()))
        else:
            ok_btn.bind(on_press=popup.dismiss)

        popup.open()
