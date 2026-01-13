"""
Controller que orquestra model e view.
"""

from .model import PrevSessionModel


class PrevSessionController:
    def __init__(self, symbol: str):
        self.model = PrevSessionModel(symbol)

    def run(self):
        prices = self.model.get_session_prices()
        variations = self.model.calc_variations(prices.ajuste)
        return prices, variations
