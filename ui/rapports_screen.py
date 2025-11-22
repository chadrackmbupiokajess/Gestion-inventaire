"""
Écran de gestion des rapports et exports
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from utils.export import ExportManager
from config import SEUIL_STOCK_FAIBLE
from datetime import datetime
from ui.date_picker import DatePicker


class RapportsScreen(Screen):
    """Écran de gestion des rapports et exports"""

    def __init__(self, **kwargs):
        super(RapportsScreen, self).__init__(**kwargs)
        self.name = 'rapports'
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = Label(text='Rapports & Exports', font_size='20sp', bold=True, size_hint=(0.7, 1), color=(1, 1, 1, 1))
        top_bar.add_widget(titre)

        retour_btn = Button(text='Retour', size_hint=(0.3, 1), background_color=(0.4, 0.4, 0.45, 1), color=(1, 1, 1, 1))
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        main_layout.add_widget(top_bar)

        # Section des exports rapides
        exports_layout = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.5))

        # Export inventaire complet
        inventaire_btn = Button(
            text='Exporter\nInventaire Complet',
            font_size='16sp',
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        inventaire_btn.bind(on_press=self.export_inventaire)
        exports_layout.add_widget(inventaire_btn)

        # Export ventes du jour
        ventes_jour_btn = Button(
            text='Exporter\nVentes du Jour',
            font_size='16sp',
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        ventes_jour_btn.bind(on_press=self.export_ventes_jour)
        exports_layout.add_widget(ventes_jour_btn)

        # Export produits en rupture
        rupture_btn = Button(
            text='Exporter\nProduits en Rupture',
            font_size='16sp',
            background_color=(1, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        rupture_btn.bind(on_press=self.export_rupture)
        exports_layout.add_widget(rupture_btn)

        # Export journal
        journal_btn = Button(
            text='Exporter\nJournal des Opérations',
            font_size='16sp',
            background_color=(0.7, 0.3, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        journal_btn.bind(on_press=self.export_journal)
        exports_layout.add_widget(journal_btn)

        main_layout.add_widget(exports_layout)

        # Section des exports personnalisés
        custom_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.5))

        custom_titre = Label(
            text='Exports Personnalisés',
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=dp(40),
            color=(1, 1, 1, 1)
        )
        custom_layout.add_widget(custom_titre)

        # Export ventes par date
        ventes_date_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        ventes_date_layout.add_widget(Label(text='Ventes du:', size_hint=(0.2, 1), color=(0.9, 0.9, 0.9, 1)))

        self.date_input = TextInput(
            multiline=False,
            text=datetime.now().strftime("%Y-%m-%d"),
            size_hint=(0.3, 1),
            hint_text='YYYY-MM-DD',
            background_color=(0.25, 0.25, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            readonly=True
        )
        ventes_date_layout.add_widget(self.date_input)

        calendar_btn = Button(
            text='📅',
            size_hint=(0.15, 1),
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        calendar_btn.bind(on_press=self.show_date_picker)
        ventes_date_layout.add_widget(calendar_btn)

        export_date_btn = Button(
            text='Exporter',
            size_hint=(0.35, 1),
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        export_date_btn.bind(on_press=self.export_ventes_date)
        ventes_date_layout.add_widget(export_date_btn)

        custom_layout.add_widget(ventes_date_layout)

        # Informations
        info_label = Label(
            text='Les fichiers exportés sont sauvegardés dans le dossier "exports"',
            font_size='14sp',
            italic=True,
            size_hint=(1, None),
            height=dp(40),
            color=(0.7, 0.7, 0.7, 1)
        )
        custom_layout.add_widget(info_label)

        main_layout.add_widget(custom_layout)

        self.add_widget(main_layout)

    def on_enter(self):
        """Appelé quand l'écran devient actif"""
        # Vérifier que l'utilisateur est admin (les vendeurs ne peuvent pas accéder aux rapports)
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            if app.current_user['role'] != 'Administrateur':
                self.show_message('Accès refusé', 'Seuls les administrateurs peuvent accéder aux rapports')
                self.manager.current = 'dashboard'
                return

    def export_inventaire(self, instance):
        """Exporter l'inventaire complet"""
        try:
            chemin = ExportManager.exporter_inventaire()
            self.show_message('Succès', f'Inventaire exporté avec succès!\n\nFichier:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def export_ventes_jour(self, instance):
        """Exporter les ventes du jour"""
        try:
            chemin = ExportManager.exporter_ventes_journalieres()
            self.show_message('Succès', f'Ventes du jour exportées avec succès!\n\nFichier:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def export_ventes_date(self, instance):
        """Exporter les ventes pour une date spécifique"""
        try:
            date = self.date_input.text.strip()
            if not date:
                self.show_message('Erreur', 'Veuillez entrer une date')
                return

            # Valider le format de la date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.show_message('Erreur', 'Format de date invalide.\nUtilisez le format YYYY-MM-DD')
                return

            chemin = ExportManager.exporter_ventes_journalieres(date)
            self.show_message('Succès', f'Ventes exportées avec succès!\n\nFichier:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def export_rupture(self, instance):
        """Exporter les produits en rupture de stock"""
        try:
            chemin = ExportManager.exporter_produits_rupture(SEUIL_STOCK_FAIBLE)
            self.show_message('Succès', f'Produits en rupture exportés avec succès!\n\nFichier:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def export_journal(self, instance):
        """Exporter le journal des opérations"""
        try:
            chemin = ExportManager.exporter_journal()
            self.show_message('Succès', f'Journal exporté avec succès!\n\nFichier:\n{chemin}')
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def show_date_picker(self, instance):
        """Afficher le sélecteur de date"""
        picker = DatePicker(callback=self.on_date_selected)
        picker.open()

    def on_date_selected(self, date_str):
        """Callback quand une date est sélectionnée"""
        self.date_input.text = date_str

    def show_message(self, titre, message):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        message_label = Label(text=message, halign='center', valign='middle', color=(1, 1, 1, 1))
        message_label.bind(size=message_label.setter('text_size'))
        content.add_widget(message_label)

        ok_btn = Button(text='OK', size_hint=(1, None), height=dp(40), background_color=(0.2, 0.5, 0.9, 1), color=(1, 1, 1, 1))
        content.add_widget(ok_btn)

        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.4))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
