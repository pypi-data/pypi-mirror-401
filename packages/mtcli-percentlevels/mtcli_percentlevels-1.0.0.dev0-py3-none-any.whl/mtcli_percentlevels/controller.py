"""
Controller:
- Orquestra obtenção do preço de referência
- Calcula níveis percentuais
"""

from .model import PercentLevelsModel


class PercentLevelsController:
    def __init__(
        self,
        symbol: str,
        ref: str,
        step: float,
        total: float,
    ):
        self.model = PercentLevelsModel(symbol)
        self.ref = ref
        self.step = step
        self.total = total

    def run(self):
        reference = self.model.get_reference_price(self.ref)
        levels = self.model.calc_levels(reference, self.step, self.total)
        return reference, levels
