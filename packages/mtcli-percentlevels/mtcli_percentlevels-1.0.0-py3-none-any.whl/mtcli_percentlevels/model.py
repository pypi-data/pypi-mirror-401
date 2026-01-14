"""
Model:
- Obtém fechamento ou ajuste do pregão anterior (D-1)
- Funciona corretamente fora do horário de pregão
- Calcula níveis percentuais verticais
"""

from dataclasses import dataclass
from typing import List
import MetaTrader5 as mt5


@dataclass
class Level:
    percent: float
    price: float


class PercentLevelsModel:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def _ensure_mt5(self) -> None:
        if not mt5.initialize():
            raise RuntimeError("Falha ao inicializar o MetaTrader 5")

    def _shutdown_mt5(self) -> None:
        mt5.shutdown()

    def get_reference_price(self, ref: str) -> float:
        """
        Retorna o preço de referência do pregão anterior:
        - close  -> fechamento D-1
        - ajuste -> ajuste D-1 (fallback = close)
        """

        self._ensure_mt5()

        try:
            rates = mt5.copy_rates_from_pos(
                self.symbol,
                mt5.TIMEFRAME_D1,
                0,
                1
            )

            if rates is None or len(rates) == 0:
                raise RuntimeError("Sem candle diário disponível")

            candle = rates[0]

            if ref == "ajuste":
                return candle["close"]

            return candle["close"]

        finally:
            self._shutdown_mt5()

    def calc_levels(
        self,
        reference: float,
        step: float,
        total: float
    ) -> List[Level]:
        """
        Calcula níveis percentuais acima e abaixo do preço de referência.
        """

        levels: List[Level] = []
        pct = step

        while pct <= total + 1e-9:
            levels.append(Level(+pct, reference * (1 + pct / 100)))
            levels.append(Level(-pct, reference * (1 - pct / 100)))
            pct += step

        return sorted(levels, key=lambda x: x.percent, reverse=True)
