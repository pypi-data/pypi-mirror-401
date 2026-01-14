"""
Controller do plugin prevsession.
Responsável apenas por obter os preços estruturais do pregão.
"""

from .model import PrevSessionModel


class PrevSessionController:
    def __init__(self, symbol: str):
        self.model = PrevSessionModel(symbol)

    def run(self):
        return self.model.get_session_prices()
