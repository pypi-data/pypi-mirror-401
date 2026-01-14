"""
View:
- Saída vertical
- Preço de referência centralizado
- Percentuais positivos e negativos em ordem decrescente
- Compatível com leitores de tela
"""

from typing import List
from .model import Level
from .conf import DIGITOS


class PercentLevelsTextView:
    def __init__(self):
        self.fmt = f"{{:.{DIGITOS}f}}"

    def _fmt(self, value: float) -> str:
        return self.fmt.format(value)

    def render(
        self,
        symbol: str,
        reference: float,
        ref_name: str,
        levels: List[Level],
    ) -> None:
        print(f"Ativo: {symbol}")
        print("-" * 40)

        # Positivos: ordem decrescente (+3 → +0.5)
        positivos = sorted(
            (l for l in levels if l.percent > 0),
            key=lambda x: x.percent,
            reverse=True,
        )

        for lvl in positivos:
            print(f"+{lvl.percent:.1f}%  {self._fmt(lvl.price)}")

        print("-" * 40)
        print(f"{ref_name.upper():<6} {self._fmt(reference)}")
        print("-" * 40)

        # Negativos: ordem decrescente (-0.5 → -3)
        negativos = sorted(
            (l for l in levels if l.percent < 0),
            key=lambda x: x.percent,
            reverse=True,
        )

        for lvl in negativos:
            print(f"{lvl.percent:.1f}%  {self._fmt(lvl.price)}")
