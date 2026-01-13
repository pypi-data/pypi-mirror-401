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
        print(f"Ativo {symbol}")
        print("-" * 60)

        print("Pregao anterior")
        print(f"Ajuste      {self._fmt_price(prices.ajuste)}")
        print(f"Fechamento {self._fmt_price(prices.fechamento)}")
        print(f"VWAP          {self._fmt_price(prices.vwap)}")
        print(f"Minima         {self._fmt_price(prices.minimo)}")
        print(f"Maxima         {self._fmt_price(prices.maximo)}")

        print("-" * 60)
        print("Pregao atual")
        print(f"Abertura    {self._fmt_price(prices.abertura_atual)}")

        print("-" * 60)
        print("Variacoes percentuais do ajuste")

        for v in variations:
            pct = f"{v['percent']:.1f}%"
            alta = self._fmt_price(v["alta"])
            baixa = self._fmt_price(v["baixa"])

            print(f"+{pct} {alta} | -{pct} {baixa}")
