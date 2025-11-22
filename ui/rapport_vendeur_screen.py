"""
Écran de rapport journalier pour les vendeurs
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from utils.export import ExportManager
from datetime import datetime


class RapportVendeurScreen(Screen):
    """Écran de rapport journalier simplifié pour les vendeurs"""

    def __init__(self, **kwargs):
        super(RapportVendeurScreen, self).__init__(**kwargs)
        self.name = 'rapport_vendeur'
        self.build_ui()

    def build_ui(self):
        """Construire l'interface"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Barre supérieure
        top_bar = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        titre = Label(
            text='Rapport Journalier',
            font_size='20sp',
            bold=True,
            size_hint=(0.7, 1),
            color=(1, 1, 1, 1)
        )
        top_bar.add_widget(titre)

        retour_btn = Button(
            text='Retour',
            size_hint=(0.3, 1),
            background_color=(0.4, 0.4, 0.45, 1),
            color=(1, 1, 1, 1)
        )
        retour_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        top_bar.add_widget(retour_btn)

        main_layout.add_widget(top_bar)

        # Informations
        info_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.3))

        info_titre = Label(
            text='Imprimer le rapport des ventes du jour',
            font_size='18sp',
            bold=True,
            color=(0.4, 1, 0.6, 1)
        )
        info_layout.add_widget(info_titre)

        date_label = Label(
            text=f"Date: {datetime.now().strftime('%d/%m/%Y')}",
            font_size='16sp',
            color=(0.9, 0.9, 0.9, 1)
        )
        info_layout.add_widget(date_label)

        description = Label(
            text='Ce rapport contient toutes les ventes effectuées aujourd\'hui\navec le détail des produits vendus et le total.',
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='middle'
        )
        description.bind(size=description.setter('text_size'))
        info_layout.add_widget(description)

        main_layout.add_widget(info_layout)

        # Bouton d'export
        export_layout = BoxLayout(orientation='vertical', spacing=dp(20), size_hint=(1, 0.7))

        # Icône
        icon_label = Label(
            text='📄',
            font_size='80sp',
            size_hint=(1, 0.5)
        )
        export_layout.add_widget(icon_label)

        # Bouton
        export_btn = Button(
            text='🖨️ Imprimer le Rapport du Jour',
            font_size='20sp',
            bold=True,
            size_hint=(0.8, None),
            height=dp(80),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        export_btn.bind(on_press=self.export_rapport_jour)
        export_layout.add_widget(export_btn)

        main_layout.add_widget(export_layout)

        self.add_widget(main_layout)

    def export_rapport_jour(self, instance):
        """Exporter le rapport des ventes du jour"""
        try:
            chemin = ExportManager.exporter_ventes_journalieres()
            self.show_message(
                'Succès',
                f'Rapport du jour exporté avec succès!\n\nFichier:\n{chemin}'
            )
        except Exception as e:
            self.show_message('Erreur', f'Erreur lors de l\'export:\n{str(e)}')

    def show_message(self, titre, message):
        """Afficher un message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        message_label = Label(
            text=message,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        message_label.bind(size=message_label.setter('text_size'))
        content.add_widget(message_label)

        ok_btn = Button(
            text='OK',
            size_hint=(1, None),
            height=dp(40),
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(ok_btn)

        popup = Popup(title=titre, content=content, size_hint=(0.8, 0.4))
        ok_btn.bind(on_press=popup.dismiss)
        popup.open()
