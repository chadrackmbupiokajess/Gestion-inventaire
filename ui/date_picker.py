"""
Widget de sélection de date (calendrier)
"""
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from datetime import datetime, timedelta
import calendar


class DatePicker(Popup):
    """Widget de sélection de date avec calendrier"""

    def __init__(self, callback=None, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.callback = callback
        self.selected_date = datetime.now()
        self.title = 'Sélectionner une date'
        self.size_hint = (0.9, 0.8)
        self.build_ui()

    def build_ui(self):
        """Construire l'interface du calendrier"""
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Navigation mois/année
        nav_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        prev_btn = Button(
            text='<',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        prev_btn.bind(on_press=self.prev_month)
        nav_layout.add_widget(prev_btn)

        self.month_label = Label(
            text=self.selected_date.strftime('%B %Y'),
            font_size='18sp',
            bold=True,
            size_hint=(0.6, 1),
            color=(1, 1, 1, 1)
        )
        nav_layout.add_widget(self.month_label)

        next_btn = Button(
            text='>',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.5, 0.9, 1),
            color=(1, 1, 1, 1)
        )
        next_btn.bind(on_press=self.next_month)
        nav_layout.add_widget(next_btn)

        main_layout.add_widget(nav_layout)

        # Jours de la semaine
        days_header = GridLayout(cols=7, size_hint=(1, None), height=dp(40), spacing=dp(2))
        for day in ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']:
            days_header.add_widget(Label(
                text=day,
                bold=True,
                color=(0.5, 0.8, 1, 1)
            ))
        main_layout.add_widget(days_header)

        # Grille du calendrier
        self.calendar_grid = GridLayout(cols=7, spacing=dp(2), size_hint=(1, 1))
        main_layout.add_widget(self.calendar_grid)

        # Boutons d'action
        buttons_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        today_btn = Button(
            text='Aujourd\'hui',
            background_color=(0.2, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        today_btn.bind(on_press=self.select_today)
        buttons_layout.add_widget(today_btn)

        cancel_btn = Button(
            text='Annuler',
            background_color=(0.4, 0.4, 0.45, 1),
            color=(1, 1, 1, 1)
        )
        cancel_btn.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_btn)

        main_layout.add_widget(buttons_layout)

        self.content = main_layout
        self.update_calendar()

    def update_calendar(self):
        """Mettre à jour l'affichage du calendrier"""
        self.calendar_grid.clear_widgets()
        self.month_label.text = self.selected_date.strftime('%B %Y')

        # Obtenir le calendrier du mois
        year = self.selected_date.year
        month = self.selected_date.month
        cal = calendar.monthcalendar(year, month)

        # Remplir la grille
        for week in cal:
            for day in week:
                if day == 0:
                    # Jour vide
                    self.calendar_grid.add_widget(Label(text=''))
                else:
                    # Créer un bouton pour le jour
                    date_obj = datetime(year, month, day)
                    is_today = date_obj.date() == datetime.now().date()

                    day_btn = Button(
                        text=str(day),
                        background_color=(0.2, 0.8, 0.4, 1) if is_today else (0.25, 0.25, 0.28, 1),
                        color=(1, 1, 1, 1)
                    )
                    day_btn.bind(on_press=lambda x, d=date_obj: self.select_date(d))
                    self.calendar_grid.add_widget(day_btn)

    def prev_month(self, instance):
        """Mois précédent"""
        # Aller au premier jour du mois actuel, puis reculer d'un jour
        first_day = self.selected_date.replace(day=1)
        self.selected_date = first_day - timedelta(days=1)
        self.update_calendar()

    def next_month(self, instance):
        """Mois suivant"""
        # Aller au dernier jour du mois actuel, puis avancer d'un jour
        if self.selected_date.month == 12:
            self.selected_date = self.selected_date.replace(year=self.selected_date.year + 1, month=1)
        else:
            self.selected_date = self.selected_date.replace(month=self.selected_date.month + 1)
        self.update_calendar()

    def select_today(self, instance):
        """Sélectionner aujourd'hui"""
        self.select_date(datetime.now())

    def select_date(self, date):
        """Sélectionner une date"""
        if self.callback:
            self.callback(date.strftime('%Y-%m-%d'))
        self.dismiss()
