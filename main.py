"""
Application AGIB - Gestion d'Inventaire pour Boutique
Point d'entrée principal de l'application
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

# Import des écrans
from ui.login_screen import LoginScreen
from ui.dashboard import DashboardScreen
from ui.produits_screen import ProduitsScreen
from ui.ventes_screen import VentesScreen
from ui.achats_screen import AchatsScreen
from ui.rapports_screen import RapportsScreen
from ui.utilisateurs_screen import UtilisateursScreen
from ui.rapport_vendeur_screen import RapportVendeurScreen


class AGIBApp(App):
    """Application principale AGIB"""

    def __init__(self, **kwargs):
        super(AGIBApp, self).__init__(**kwargs)
        self.current_user = None

    def build(self):
        """Construire l'application"""
        # Configurer la fenêtre avec un fond sombre agréable
        Window.clearcolor = (0.15, 0.15, 0.18, 1)  # Gris foncé bleuté
        Window.size = (800, 600)

        # Créer le gestionnaire d'écrans
        sm = ScreenManager(transition=NoTransition())

        # Ajouter tous les écrans
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        sm.add_widget(ProduitsScreen())
        sm.add_widget(VentesScreen())
        sm.add_widget(AchatsScreen())
        sm.add_widget(RapportsScreen())
        sm.add_widget(UtilisateursScreen())
        sm.add_widget(RapportVendeurScreen())

        # Démarrer sur l'écran de connexion
        sm.current = 'login'

        return sm

    def on_stop(self):
        """Appelé lors de la fermeture de l'application"""
        # Nettoyer les ressources si nécessaire
        pass


if __name__ == '__main__':
    AGIBApp().run()
