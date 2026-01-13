"""
Model responsável por:
- Identificar corretamente o pregão anterior na B3
- Funcionar em dias úteis, finais de semana e feriados
- Extrair preços estruturais do D1 via MetaTrader 5
- Calcular variações percentuais a partir do preço de ajuste

Regras:
- Nunca usar datas para identificar pregão
- Sempre usar posição dos candles (copy_rates_from_pos)
"""

from dataclasses import dataclass

import MetaTrader5 as mt5


@dataclass
class SessionPrices:
    ajuste: float
    fechamento: float
    vwap: float
    minimo: float
    maximo: float
    abertura_atual: float


class PrevSessionModel:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def _ensure_mt5(self) -> None:
        if not mt5.initialize():
            raise RuntimeError("Falha ao inicializar o MetaTrader 5")

    def _shutdown_mt5(self) -> None:
        mt5.shutdown()

    def get_session_prices(self) -> SessionPrices:
        """
        Retorna preços estruturais do pregão anterior e
        abertura do pregão atual (quando existir).

        Funciona corretamente:
        - Durante o pregão
        - Após o fechamento
        - Em sábado, domingo e feriados
        """

        self._ensure_mt5()

        try:
            # Tenta obter até 2 candles diários
            rates = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_D1, 0, 2)

            if rates is None or len(rates) == 0:
                raise RuntimeError("Sem candles diários disponíveis no MT5")

            # Caso normal: pregão em andamento ou candle atual criado
            if len(rates) == 2:
                current = rates[0]
                prev = rates[1]
                abertura_atual = current["open"]

            # Caso sábado / domingo / feriado
            else:
                prev = rates[0]
                abertura_atual = prev["open"]

            ajuste = prev["close"]
            fechamento = prev["close"]
            minimo = prev["low"]
            maximo = prev["high"]

            volume = prev["tick_volume"]
            vwap = (
                (prev["high"] + prev["low"] + prev["close"]) / 3
                if volume > 0
                else ajuste
            )

            return SessionPrices(
                ajuste=ajuste,
                fechamento=fechamento,
                vwap=vwap,
                minimo=minimo,
                maximo=maximo,
                abertura_atual=abertura_atual,
            )

        finally:
            self._shutdown_mt5()

    def calc_variations(
        self, ajuste: float, step: float = 0.5, limit: float = 3.0
    ) -> list[dict[str, float]]:
        """
        Calcula níveis percentuais simétricos acima e abaixo
        do preço de ajuste.

        Padrão:
        - De 0,5% até 3,0%
        """

        variations: list[dict[str, float]] = []
        pct = step

        while pct <= limit + 1e-9:
            variations.append(
                {
                    "percent": pct,
                    "alta": ajuste * (1 + pct / 100),
                    "baixa": ajuste * (1 - pct / 100),
                }
            )
            pct += step

        return variations
