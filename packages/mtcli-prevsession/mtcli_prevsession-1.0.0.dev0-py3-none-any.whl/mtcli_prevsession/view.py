"""
View em texto puro, acessível a leitores de tela.

- Usa formatação numérica padronizada
- Respeita a constante DIGITOS definida em conf.py
- Não aplica lógica de negócio (somente apresentação)
"""

from typing import List, Dict
from .model import SessionPrices
from .conf import DIGITOS


class PrevSessionTextView:
    def __init__(self):
        self.fmt = f"{{:.{DIGITOS}f}}"

    def _fmt_price(self, value: float) -> str:
        return self.fmt.format(value)

    def render(
        self,
        symbol: str,
        prices: SessionPrices,
        variations: List[Dict[str, float]],
    ) -> None:
        print(f"Ativo: {symbol}")
        print("-" * 60)

        print("Pregão anterior:")
        print(f"Preço de ajuste:      {self._fmt_price(prices.ajuste)}")
        print(f"Preço de fechamento: {self._fmt_price(prices.fechamento)}")
        print(f"VWAP do dia:          {self._fmt_price(prices.vwap)}")
        print(f"Preço mínimo:         {self._fmt_price(prices.minimo)}")
        print(f"Preço máximo:         {self._fmt_price(prices.maximo)}")

        print("-" * 60)
        print("Pregão atual:")
        print(f"Preço de abertura:    {self._fmt_price(prices.abertura_atual)}")

        print("-" * 60)
        print("Variações percentuais em relação ao ajuste:")

        for v in variations:
            pct = f"{v['percent']:.1f}%"
            alta = self._fmt_price(v["alta"])
            baixa = self._fmt_price(v["baixa"])

            print(f"{pct} acima: {alta} | {pct} abaixo: {baixa}")
