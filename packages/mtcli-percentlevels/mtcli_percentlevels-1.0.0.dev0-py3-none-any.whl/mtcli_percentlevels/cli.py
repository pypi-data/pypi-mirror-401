"""
Comando mtcli: percentlevels
"""

import click
from .controller import PercentLevelsController
from .view import PercentLevelsTextView
from .conf import (
    PERCENT_STEP,
    PERCENT_TOTAL,
    PERCENT_REF,
    SYMBOL,
)


@click.command()
@click.version_option(package_name="mtcli-percentlevels")
@click.option(
    "--symbol",
    "-s",
    default=SYMBOL,
    show_default=True,
    help="Ativo negociado no MT5.",
)
@click.option(
    "--ref",
    "-r",
    type=click.Choice(["close", "ajuste"]),
    default=PERCENT_REF,
    show_default=True,
    help="Preço de referência (fechamento ou ajuste D-1).",
)
@click.option(
    "--step",
    "-st",
    type=float,
    default=PERCENT_STEP,
    show_default=True,
    help="Passo percentual.",
)
@click.option(
    "--total",
    "-t",
    type=float,
    default=PERCENT_TOTAL,
    show_default=True,
    help="Variação percentual total.",
)
def percentlevels(symbol: str, ref: str, step: float, total: float):
    """
    Exibe níveis percentuais verticais em relação
    ao fechamento ou ajuste do pregão anterior.
    """

    controller = PercentLevelsController(symbol, ref, step, total)
    view = PercentLevelsTextView()

    reference, levels = controller.run()
    view.render(symbol, reference, ref, levels)
