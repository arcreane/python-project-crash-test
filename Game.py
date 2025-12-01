from PySide6.QtCore import QTimer


class GameEngine:
    """
    Gère :
    - score
    - temps sans crash
    - +1 point toutes les 10 s
    """

    def __init__(self, sim):
        self.sim = sim
        self.score = 0
        self.managed_planes = 0
        self.survival_time = 0

        # Timer 1s → temps sans crash
        self.survival_timer = QTimer(sim)
        self.survival_timer.timeout.connect(self._on_survival_tick)
        self.survival_timer.start(1000)

        # Timer 10s → +1 point
        self.score_timer = QTimer(sim)
        self.score_timer.timeout.connect(self._on_score_tick)
        self.score_timer.start(10000)

        # Initialisation label
        if hasattr(self.sim.ui, "labelScore"):
            self.sim.ui.labelScore.setText("Score : 0")
        if hasattr(self.sim.ui, "labelTimer"):
            self.update_timer_label()

    # ---------- Ticks ----------

    def _on_survival_tick(self):
        if not self.sim.game_over:
            self.survival_time += 1
            self.update_timer_label()

    def _on_score_tick(self):
        if not self.sim.game_over:
            self.score += 1
            self.update_score_label()

    def update_timer_label(self):
        minutes = self.survival_time // 60
        seconds = self.survival_time % 60
        text = f"⏱ {minutes:02d}:{seconds:02d}"

        if hasattr(self.sim.ui, "labelTimer"):
            self.sim.ui.labelTimer.setText(text)

    # ---------- API ----------

    def add_managed_plane(self):
        self.managed_planes += 1
        self.update_score_label()

    def update_score_label(self):
        if hasattr(self.sim.ui, "labelScore"):
            self.sim.ui.labelScore.setText(
                f"Score : {self.score}\n\n"
                f"Avions gérés : {self.managed_planes}"
            )

    def stop_all(self):
        """Appelé sur collision pour couper les timers de jeu."""
        self.survival_timer.stop()
        self.score_timer.stop()
