from PySide6.QtCore import QTimer


class GameEngine:
    """
    Gère :
    - le score
    - le temps sans crash
    """

    def __init__(self, sim):
        self.sim = sim
        self.score = 0
        self.survival_time = 0

        # Timer 1s → temps sans crash
        self.survival_timer = QTimer(sim)
        self.survival_timer.timeout.connect(self._on_survival_tick)
        self.survival_timer.start(1000)

        # Timer 10s → +1 point
        self.score_timer = QTimer(sim)
        self.score_timer.timeout.connect(self._on_score_tick)
        self.score_timer.start(10000)

    def _on_survival_tick(self):
        if not self.sim.game_over:
            self.survival_time += 1

    def _on_score_tick(self):
        if not self.sim.game_over:
            self.score += 1

    def stop_all(self):
        """Appelé sur collision pour stop les timers"""
        self.survival_timer.stop()
        self.score_timer.stop()
