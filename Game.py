from PySide6.QtCore import QTimer


class GameEngine:
    """
    Gère :
    - score
    - temps sans crash
    - bonus atterrissage / malus avion perdu
    - +1 point toutes les 10 s
    """

    def __init__(self, sim):
        self.sim = sim
        self.score = 0
        self.managed_planes = 0
        self.survival_time = 0
        self.selected_planes = set()

        # Timer 1s → temps sans crash
        self.survival_timer = QTimer(sim)
        self.survival_timer.timeout.connect(self.survival_tick)
        self.survival_timer.start(1000)

        # Timer 10s → +1 point
        self.score_timer = QTimer(sim)
        self.score_timer.timeout.connect(self.score_tick)
        self.score_timer.start(10000)


        self.sim.ui.labelScore.setText("Score : 0")


    def survival_tick(self):
        if not self.sim.game_over:
            self.survival_time += 1
            self.timer_label()
            self.sim.update_info_label()  # met à jour label avion si sélectionné

    def score_tick(self):
        if not self.sim.game_over:
            self.score += 1
            self.update_score_label()

    def timer_label(self):
        """Affiche le timer"""
        minutes = self.survival_time // 60
        seconds = self.survival_time % 60
        text = f"⏱ {minutes:02d}:{seconds:02d}"

        self.sim.ui.labelTimer.setText(text)


    def register_click(self, plane):
        """Appelé quand on clique sur un avion pour ajouter dans les avions gérer."""
        self.selected_planes.add(plane)

    def add_landing_score(self, plane):
        """Bonus quand un avion atterrit correctement."""
        self.score += 5
        self.update_score_label()

    def add_missed_penalty(self, plane):
        """Malus si avion quitte l'écran sans avoir été cliqué."""
        if plane not in self.selected_planes and not self.sim.game_over:
            self.score -= 3
            self.update_score_label()

    def add_managed_plane(self, plane):
        """Compteur d’avions gérés correctement."""
        self.managed_planes += 1
        self.update_score_label()

    def update_score_label(self):
        self.sim.ui.labelScore.setText(
            f"Score : {self.score}\n"
            f"\n"
            f"\n"
            f"Avions gérés : {self.managed_planes}\n"
        )

    def stop_all(self):
        """Appelé sur collision pour couper les timers."""
        self.survival_timer.stop()
        self.score_timer.stop()
